from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid
from typing import List

from document_processor import DocumentProcessor
from vector_store import VectorStore

import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="Intelligent Document Q&A System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
document_processor = DocumentProcessor()
vector_store = VectorStore()

# In-memory storage for documents (in production, use a proper database)
documents_db = {}

class QueryRequest(BaseModel):
    document_id: str
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        allowed_types = ['.pdf', '.md', '.html', '.txt']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed types: {', '.join(allowed_types)}"
            )

        doc_id = str(uuid.uuid4())
        temp_path = f"temp_{doc_id}_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        try:
            chunks = document_processor.process_document(temp_path, file_extension)
            
            if not chunks:
                raise HTTPException(status_code=400, detail="No content could be extracted from the document")

            vector_store.add_document(doc_id, chunks)

            documents_db[doc_id] = {
                'id': doc_id,
                'filename': file.filename,
                'type': file_extension[1:].upper(),
                'chunks': len(chunks),
                'pages': getattr(chunks[0], 'page', None) and max(
                    chunk.page for chunk in chunks if hasattr(chunk, 'page')
                ) or None
            }

            return documents_db[doc_id]

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/api/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """Query a document with a question"""
    try:
        if request.document_id not in documents_db:
            raise HTTPException(status_code=404, detail="Document not found")

        relevant_chunks = vector_store.search(request.document_id, request.question, k=5)
        
        if not relevant_chunks:
            return QueryResponse(
                answer="I couldn't find relevant information in the document to answer your question.",
                sources=[]
            )

        # Combine chunks into context
        context = "\n\n".join([chunk.text for chunk, _ in relevant_chunks])

        # Build prompt for Gemini
        prompt = f"""
        You are a helpful assistant. Use ONLY the following document content to answer.

        Document:
        {context}

        Question: {request.question}
        """

        response = gemini_model.generate_content(prompt)

        sources = []
        for chunk, score in relevant_chunks:
            source = {
                'text': chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text,
                'score': float(score),
                'chunk_id': getattr(chunk, 'chunk_id', 'unknown')
            }
            if hasattr(chunk, 'page'):
                source['page'] = chunk.page
            sources.append(source)

        return QueryResponse(answer=response.text, sources=sources)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/api/documents")
async def list_documents():
    """List all uploaded documents"""
    return list(documents_db.values())

@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    if document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    vector_store.remove_document(document_id)
    del documents_db[document_id]
    
    return {"message": "Document deleted successfully"}

@app.get("/")
async def root():
    return {"message": "Intelligent Document Q&A System API (Gemini-powered)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
