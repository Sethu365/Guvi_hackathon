# Intelligent Document Q&A System (Open-Source RAG)

An intelligent Q&A system that allows users to upload documents (PDFs, Notion exports, or wiki pages) and ask natural language questions. The system provides accurate, contextual answers using Retrieval-Augmented Generation (RAG) with open-source models.

## 🌟 Features

- **Document Upload**: Support for PDFs, Markdown, HTML, and text files
- **Smart Chunking**: Intelligent text splitting with overlap for better context
- **Vector Search**: Fast similarity search using FAISS and Sentence Transformers
- **RAG System**: Retrieval-Augmented Generation for contextual answers
- **Chat Interface**: Clean, modern chat UI with source citations
- **Open Source**: No paid APIs required - runs entirely on open-source models

## 🎯 Target Users

- **Students** studying long PDFs or research papers
- **Employees** querying internal documentation or wikis
- **Customers** exploring product manuals or FAQs

## 🛠️ Tech Stack

### Frontend
- **React.js** with JavaScript
- **Tailwind CSS** for styling
- **React Dropzone** for file uploads
- **Axios** for API communication
- **Lucide React** for icons

### Backend
- **FastAPI** (Python) for the API server
- **Sentence Transformers** for embeddings (all-MiniLM-L6-v2)
- **FAISS** for vector storage and similarity search
- **pdfplumber & PyMuPDF** for PDF processing
- **BeautifulSoup & html2text** for HTML/Markdown processing

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   python start_server.py
   ```
   The backend will be available at `http://localhost:8000`

2. **Start the Frontend Development Server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 📖 How It Works

### 1. Document Processing
- Upload documents through the web interface
- Text extraction using specialized libraries for each format
- Intelligent chunking with configurable size and overlap

### 2. Vector Embeddings
- Generate embeddings using Sentence Transformers
- Store vectors in FAISS for fast similarity search
- Maintain document metadata and chunk mappings

### 3. Question Answering
- Convert user questions to embeddings
- Retrieve most relevant document chunks
- Generate contextual answers using rule-based RAG
- Provide source citations with confidence scores

## 🔧 Configuration

### Chunk Settings
- **Chunk Size**: 500 tokens (configurable in `document_processor.py`)
- **Chunk Overlap**: 50 tokens for better context preservation

### Embedding Model
- **Default**: `all-MiniLM-L6-v2` (384 dimensions, fast and accurate)
- **Alternative**: `all-mpnet-base-v2` (768 dimensions, higher quality)

### Supported File Types
- **PDF**: `.pdf` files
- **Markdown**: `.md` files
- **HTML**: `.html` files
- **Text**: `.txt` files

## 🎨 User Interface

### Main Components
- **Document Upload**: Drag-and-drop interface with progress feedback
- **Document List**: Sidebar showing all uploaded documents
- **Chat Interface**: Clean chat UI with message history
- **Source Citations**: References to original document sections

### Features
- Responsive design for all screen sizes
- Real-time upload progress
- Message timestamps
- Source highlighting with confidence scores
- Error handling and user feedback

## 🔮 Future Enhancements

### Planned Features
- **LLM Integration**: Add support for local models (Ollama, GPT4All)
- **Multi-document Q&A**: Ask questions across multiple documents
- **Advanced Chunking**: Semantic chunking based on document structure
- **Export Options**: Save Q&A sessions as PDF or Markdown
- **User Authentication**: Multi-user support with document privacy
- **Advanced Search**: Filters, sorting, and search within documents

### Model Upgrades
- **Better Embeddings**: Support for domain-specific embedding models
- **Local LLMs**: Integration with Mistral, LLaMA2, or Falcon
- **Hybrid Search**: Combine semantic and keyword search

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Sentence Transformers** for excellent embedding models
- **FAISS** for fast similarity search
- **FastAPI** for the robust backend framework
- **React** and **Tailwind CSS** for the modern frontend

---

**Built with ❤️ for the open-source community**