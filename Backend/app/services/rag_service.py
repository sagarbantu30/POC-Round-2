"""
RAG Service for MongoDB
Handles document processing and RAG-based chat
"""
import os
import tempfile
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from app.core.config import settings
from app.db.session import get_database


class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        
        # PGVector connection for vector store
        if not settings.PGVECTOR_CONNECTION or not settings.PGVECTOR_COLLECTION:
            raise ValueError("PGVECTOR_CONNECTION and PGVECTOR_COLLECTION must be set in .env")
        self.vector_store = PGVector(
            connection=settings.PGVECTOR_CONNECTION,
            collection_name=settings.PGVECTOR_COLLECTION,
            embeddings=self.embeddings,
        )
        
        # Create LLM instance
        self.llm = None
        self._initialize_llm()
        # Keep last retrieved docs for debugging/inspection (not returned in API response)
        self.last_retrieved_docs = []
    
    def _initialize_llm(self, model_name: str = None, temperature: float = None, top_p: float = None):
        """Initialize the LLM with specified settings"""
        model_name = model_name or settings.MODEL_NAME
        temperature = temperature if temperature is not None else settings.TEMPERATURE
        top_p = top_p if top_p is not None else settings.TOP_P
        
        # Log the LLM initialization with parameters
        print(f"\n[LLM INIT] Initializing ChatOpenAI with:")
        print(f"  - model_name: {model_name}")
        print(f"  - temperature: {temperature}")
        print(f"  - top_p: {top_p}")
        
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            top_p=top_p,
            openai_api_key=settings.OPENAI_API_KEY
        )
        print(f"[LLM INIT] ChatOpenAI initialized successfully\n")
        
    async def get_settings(self) -> dict:
        """Get current RAG settings or return defaults"""
        db = get_database()
        rag_settings = await db.rag_settings.find_one()
        
        if not rag_settings:
            # Return default settings
            return {
                "chunk_size": settings.CHUNK_SIZE,
                "chunk_overlap": settings.CHUNK_OVERLAP,
                "temperature": settings.TEMPERATURE,
                "top_p": settings.TOP_P,
                "top_k": settings.TOP_K,
                "model_name": settings.MODEL_NAME
            }
        return rag_settings
    
    def _create_retriever(self, top_k: int, filter_dict: Optional[dict] = None):
        """Create a retriever with optional filtering"""
        print(f"\n[RETRIEVER] Creating retriever with:")
        print(f"  - top_k (num documents to retrieve): {top_k}")
        if filter_dict:
            print(f"  - filter: {filter_dict}")
        
        if filter_dict:
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": top_k,
                    "filter": filter_dict
                }
            )
        else:
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": top_k}
            )
        print(f"[RETRIEVER] Retriever created successfully\n")
        return retriever
    
    def _create_rag_chain(self, retriever, llm_instance):
        """Create a RAG chain using LCEL (LangChain Expression Language)"""
        # Define the prompt template
        template = """You are a helpful AI assistant that answers questions based on provided documents.

Use the following context to answer the user's question. If the context doesn't contain relevant information, say so clearly.

Context:
{context}

Question: {question}

Answer:"""
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_template(template)
        
        # Format documents function
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        # Create LCEL chain
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm_instance
            | StrOutputParser()
        )
        
        return rag_chain, retriever
    
    async def process_document(
        self, 
        file_content: bytes, 
        filename: str, 
        document_id: str,
        is_company_policy: bool = False
    ) -> bool:
        """Process and embed a document into the vector store"""
        try:
            # Get current settings from database for dynamic chunk configuration
            rag_settings = await self.get_settings()
            chunk_size = rag_settings.get("chunk_size", settings.CHUNK_SIZE)
            chunk_overlap = rag_settings.get("chunk_overlap", settings.CHUNK_OVERLAP)
            
            print(f"\n[DOCUMENT PROCESSING] Processing: {filename}")
            print(f"  - document_id: {document_id}")
            print(f"  - chunk_size (from DB): {chunk_size}")
            print(f"  - chunk_overlap (from DB): {chunk_overlap}")
            print(f"  - is_company_policy: {is_company_policy}")
            
            # Save file temporarily
            file_extension = os.path.splitext(filename)[1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name
            
            # Load document based on file type
            if file_extension == '.pdf':
                loader = PyPDFLoader(tmp_path)
            elif file_extension in ['.docx', '.doc']:
                loader = Docx2txtLoader(tmp_path)
            elif file_extension == '.txt':
                loader = TextLoader(tmp_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            documents = loader.load()
            print(f"  - loaded {len(documents)} pages/sections")
            
            # Split documents into chunks using settings from database
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            splits = text_splitter.split_documents(documents)
            print(f"  - created {len(splits)} chunks with chunk_size={chunk_size}, overlap={chunk_overlap}")
            
            # Add metadata to each chunk
            for split in splits:
                split.metadata.update({
                    "document_id": document_id,
                    "filename": filename,
                    "is_company_policy": is_company_policy
                })
            
            # Add to vector store
            self.vector_store.add_documents(splits)
            print(f"[DOCUMENT PROCESSING] Successfully added {len(splits)} chunks to vector store\n")
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            return True
        except Exception as e:
            print(f"[DOCUMENT PROCESSING] Error processing document: {e}\n")
            return False
    
    async def chat(
        self, 
        query: str, 
        document_id: Optional[str] = None,
        use_company_policy: bool = False
    ) -> tuple[str, List[str]]:
        """Chat with documents using RAG chain - LCEL approach"""
        try:
            print(f"\n{'='*70}")
            print(f"[CHAT REQUEST] Received query: {query[:100]}...")
            print(f"{'='*70}")
            
            # Get latest settings from database
            rag_settings = await self.get_settings()
            
            print(f"\n[SETTINGS LOADED FROM DB]")
            print(f"  - chunk_size: {rag_settings.get('chunk_size')}")
            print(f"  - chunk_overlap: {rag_settings.get('chunk_overlap')}")
            print(f"  - temperature: {rag_settings.get('temperature')}")
            print(f"  - top_p: {rag_settings.get('top_p')}")
            print(f"  - top_k: {rag_settings.get('top_k')}")
            print(f"  - model_name: {rag_settings.get('model_name')}")
            
            top_k = rag_settings.get("top_k", settings.TOP_K)
            
            # Reinitialize LLM with latest settings to ensure model and parameters are up-to-date
            self._initialize_llm(
                model_name=rag_settings.get("model_name"),
                temperature=rag_settings.get("temperature"),
                top_p=rag_settings.get("top_p")
            )

            # Create retriever with top_k from settings
            retriever = self._create_retriever(top_k, None)
            
            # Retrieve relevant documents
            retrieved_docs = retriever.invoke(query)
            self.last_retrieved_docs = retrieved_docs
            
            print(f"\n[RETRIEVAL RESULTS]")
            print(f"  - Retrieved {len(retrieved_docs)} documents with top_k={top_k}")
            if retrieved_docs:
                sample = retrieved_docs[0]
                print(f"  - Sample metadata: {sample.metadata}")
                print(f"  - Sample content (first 100 chars): {sample.page_content[:100]}...")

            # Create RAG chain with the selected retriever
            print(f"\n[RAG CHAIN] Building RAG chain with LLM parameters:")
            print(f"  - LLM Model: {self.llm.model_name}")
            print(f"  - Temperature: {self.llm.temperature}")
            print(f"  - Top P: {self.llm.top_p}")
            
            rag_chain, retriever_obj = self._create_rag_chain(retriever, self.llm)

            # Invoke the RAG chain
            print(f"\n[INVOKING RAG CHAIN] Processing query with LLM...")
            answer = rag_chain.invoke(query)
            print(f"[RAG CHAIN] Response received (length: {len(answer)} chars)\n")

            # Extract source documents
            source_docs = []
            for doc in retrieved_docs:
                filename = doc.metadata.get("filename", "Unknown")
                if filename not in source_docs:
                    source_docs.append(filename)

            print(f"[CHAT COMPLETE] Sources: {source_docs}")
            print(f"{'='*70}\n")
            
            return answer, source_docs

        except Exception as e:
            print(f"\n[CHAT ERROR] {str(e)}")
            import traceback
            traceback.print_exc()
            print(f"{'='*70}\n")
            return f"Error: {str(e)}", []
    
    async def delete_document_embeddings(self, document_id: str) -> bool:
        """Delete document embeddings from vector store"""
        try:
            # Pinecone delete by metadata filter
            self.vector_store.delete(
                ids=None,
                filter={"document_id": document_id}
            )
            return True
        except Exception as e:
            print(f"Error deleting document embeddings: {e}")
            return False
