# RAG POC Backend

Simple FastAPI backend with MongoDB for RAG (Retrieval Augmented Generation) functionality.

## Architecture

- **FastAPI**: Modern async web framework
- **MongoDB**: Document database for storing users, documents metadata, and RAG settings
- **LangChain + MongoDB Atlas**: Vector store for document embeddings and RAG
- **OpenAI**: LLM for chat and embeddings
- **Motor**: Async MongoDB driver

## Project Structure

```
Backend/
├── app/
│   ├── api/              # API endpoints
│   │   └── api_v1/
│   │       └── endpoints/  # Route handlers (auth, users, documents, chat, settings)
│   ├── core/             # Core config and security
│   ├── db/               # Database connection
│   ├── models/           # Pydantic models for MongoDB
│   ├── schemas/          # Request/Response schemas
│   └── services/         # Business logic (user_service, rag_service)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── create_admin.py      # Script to create admin user
```

## Quick Setup

### 1. Prerequisites
- Python 3.9+
- MongoDB Atlas account (free tier works)
- OpenAI API key

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Edit `.env` with your values:
- `MONGODB_URI`: Your MongoDB Atlas connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `SECRET_KEY`: Random secret for JWT tokens

### 4. Create Admin User

```bash
python create_admin.py
```

Default credentials:
- Email: admin@example.com
- Password: admin123

### 5. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login and get JWT token

### Users
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/{id}` - Get user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Documents
- `POST /api/v1/documents/upload` - Upload document for RAG
- `GET /api/v1/documents/` - List documents
- `GET /api/v1/documents/{id}` - Get document
- `DELETE /api/v1/documents/{id}` - Delete document

### Chat
- `POST /api/v1/chat/` - Chat with documents using RAG

### Settings
- `GET /api/v1/settings/` - Get RAG settings
- `PUT /api/v1/settings/` - Update RAG settings (admin only)

## MongoDB Collections

- `users` - User accounts
- `documents` - Document metadata
- `rag_settings` - RAG configuration
- `documents_collection` - Vector embeddings (managed by LangChain)

## Development

The project uses:
- Async/await for all database and API operations
- Pydantic for data validation
- JWT for authentication
- Simple service layer pattern

## Environment Variables

See `.env.example` for all available configuration options.

Required:
- `MONGODB_URI`
- `OPENAI_API_KEY`

Optional (have defaults):
- `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TEMPERATURE`, `MODEL_NAME`, etc.
