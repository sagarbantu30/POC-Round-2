# RAG POC - Retrieval Augmented Generation

Simple POC for RAG (Retrieval Augmented Generation) with document chat functionality.

## Overview

This is a simplified POC that demonstrates:
- Document upload and processing
- Vector embeddings storage in MongoDB Atlas
- RAG-based chat with uploaded documents
- User authentication and management
- Settings configuration

## Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **MongoDB** - Document database (using MongoDB Atlas)
- **LangChain** - RAG framework
- **OpenAI** - LLM and embeddings
- **Motor** - Async MongoDB driver

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling

## Project Structure

```
POC-Round-2/
├── Backend/          # FastAPI backend
│   ├── app/         # Application code
│   ├── requirements.txt
│   └── README.md    # Backend setup instructions
├── Frontend/         # Next.js frontend
│   ├── app/         # App router pages
│   ├── components/  # React components
│   └── README.md    # Frontend setup instructions
└── README.md        # This file
```

## Quick Start

### Prerequisites
- Python 3.14
- Node.js 18+
- MongoDB Atlas account (free tier)
- OpenAI API key

### 1. Backend Setup

```bash
cd Backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and OpenAI API key

# Create admin user
python create_admin.py

# Run server
uvicorn app.main:app --reload --port 8000
```

Backend will run at http://localhost:8000

### 2. Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run at http://localhost:3000

## Features

- **Authentication** - Login system with JWT tokens
- **Document Upload** - Upload PDFs, DOCX, TXT files
- **RAG Chat** - Chat with uploaded documents
- **Company Policy** - Flag documents as company policies
- **Settings Management** - Configure RAG parameters
- **User Management** - Admin can manage users

## MongoDB Collections

- `users` - User accounts
- `documents` - Document metadata
- `rag_settings` - RAG configuration
- `documents_collection` - Vector embeddings

## Default Admin Credentials

After running `create_admin.py`:
- Email: admin@example.com
- Password: admin123

**Change these in production!**

## API Documentation

Access interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

### Backend (.env)
- `MONGODB_URI` - MongoDB Atlas connection string
- `OPENAI_API_KEY` - OpenAI API key
- `SECRET_KEY` - JWT secret key

See `Backend/.env.example` for all options.

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

## Development Notes

This is a **simplified POC** designed for easy review:
- Uses MongoDB for all data storage (no SQL)
- Async/await throughout
- Simple service layer pattern
- Minimal dependencies
- Clear project structure

## License

MIT
