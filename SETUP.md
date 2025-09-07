# 🚀 Setup Guide - Intelligent Document Q&A System

## Prerequisites

Before starting, make sure you have:
- **Node.js 18+** and npm installed
- **Python 3.8+** installed
- **pip** (Python package manager)

## Quick Setup (5 minutes)

### Step 1: Install Frontend Dependencies
```bash
npm install
```

### Step 2: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### Step 3: Start the Backend Server
```bash
cd backend
python start_server.py
```
Keep this terminal open - the backend will run on `http://localhost:8000`

### Step 4: Start the Frontend (New Terminal)
```bash
npm run dev
```
The frontend will be available at `http://localhost:5173`

## 🎉 You're Ready!

1. Open your browser to `http://localhost:5173`
2. Upload a PDF, Markdown, HTML, or text file
3. Start asking questions about your document!

## Troubleshooting

### Python Dependencies Issues
If you encounter issues installing Python packages:

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Port Conflicts
If ports 8000 or 5173 are in use:
- Backend: Edit `backend/start_server.py` and change the port
- Frontend: Vite will automatically suggest an alternative port

### Model Download
The first time you run the system, it will download the Sentence Transformer model (~90MB). This is normal and only happens once.

## System Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free space for models and documents
- **Internet**: Required for initial model download only

## What's Included

✅ **Document Processing**: PDFs, Markdown, HTML, Text files  
✅ **Vector Search**: FAISS with Sentence Transformers  
✅ **Smart Q&A**: Rule-based RAG system  
✅ **Modern UI**: React with Tailwind CSS  
✅ **Source Citations**: References with confidence scores  
✅ **No API Keys**: 100% open-source and local  

## Next Steps

1. Try uploading different document types
2. Ask various question types (what, how, why, when, where, who)
3. Check the source citations for answer verification
4. Explore the API documentation at `http://localhost:8000/docs`

Need help? Check the README.md for detailed documentation!