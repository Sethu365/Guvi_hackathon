import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict, Any
import pickle
import os
from document_processor import DocumentChunk

class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize vector store with sentence transformer model"""
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        
        # Storage for document chunks and metadata
        self.chunks_storage: Dict[str, List[DocumentChunk]] = {}
        self.chunk_to_doc_map: List[str] = []  # Maps index position to document_id
        self.chunk_to_chunk_map: List[int] = []  # Maps index position to chunk index within document

    def add_document(self, document_id: str, chunks: List[DocumentChunk]):
        """Add document chunks to the vector store"""
        if not chunks:
            return

        # Store chunks
        self.chunks_storage[document_id] = chunks

        # Generate embeddings
        texts = [chunk.text for chunk in chunks]
        embeddings = self._generate_embeddings(texts)

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)

        # Add to FAISS index
        self.index.add(embeddings)

        # Update mapping
        for i, chunk in enumerate(chunks):
            self.chunk_to_doc_map.append(document_id)
            self.chunk_to_chunk_map.append(i)

    def search(self, document_id: str, query: str, k: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """Search for relevant chunks in a specific document"""
        if document_id not in self.chunks_storage:
            return []

        # Generate query embedding
        query_embedding = self._generate_embeddings([query])
        faiss.normalize_L2(query_embedding)

        # Search in FAISS index
        scores, indices = self.index.search(query_embedding, min(k * 3, self.index.ntotal))  # Get more results to filter

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for invalid indices
                continue
                
            # Check if this chunk belongs to the target document
            if self.chunk_to_doc_map[idx] == document_id:
                chunk_idx = self.chunk_to_chunk_map[idx]
                chunk = self.chunks_storage[document_id][chunk_idx]
                results.append((chunk, float(score)))

        # Return top k results
        return results[:k]

    def search_all_documents(self, query: str, k: int = 5) -> List[Tuple[DocumentChunk, float, str]]:
        """Search across all documents"""
        if self.index.ntotal == 0:
            return []

        # Generate query embedding
        query_embedding = self._generate_embeddings([query])
        faiss.normalize_L2(query_embedding)

        # Search in FAISS index
        scores, indices = self.index.search(query_embedding, min(k, self.index.ntotal))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
                
            doc_id = self.chunk_to_doc_map[idx]
            chunk_idx = self.chunk_to_chunk_map[idx]
            chunk = self.chunks_storage[doc_id][chunk_idx]
            results.append((chunk, float(score), doc_id))

        return results

    def remove_document(self, document_id: str):
        """Remove a document from the vector store"""
        if document_id not in self.chunks_storage:
            return

        # Find indices to remove
        indices_to_remove = []
        for i, doc_id in enumerate(self.chunk_to_doc_map):
            if doc_id == document_id:
                indices_to_remove.append(i)

        # Remove from storage
        del self.chunks_storage[document_id]

        # For FAISS, we need to rebuild the index without the removed vectors
        # This is because FAISS doesn't support efficient removal of specific vectors
        if indices_to_remove:
            self._rebuild_index_without_indices(indices_to_remove)

    def _rebuild_index_without_indices(self, indices_to_remove: List[int]):
        """Rebuild FAISS index without specified indices"""
        indices_to_remove = set(indices_to_remove)
        
        # Collect remaining chunks and their embeddings
        remaining_texts = []
        new_chunk_to_doc_map = []
        new_chunk_to_chunk_map = []

        for i, (doc_id, chunk_idx) in enumerate(zip(self.chunk_to_doc_map, self.chunk_to_chunk_map)):
            if i not in indices_to_remove:
                if doc_id in self.chunks_storage:  # Make sure document still exists
                    chunk = self.chunks_storage[doc_id][chunk_idx]
                    remaining_texts.append(chunk.text)
                    new_chunk_to_doc_map.append(doc_id)
                    new_chunk_to_chunk_map.append(chunk_idx)

        # Rebuild index
        self.index = faiss.IndexFlatIP(self.dimension)
        self.chunk_to_doc_map = new_chunk_to_doc_map
        self.chunk_to_chunk_map = new_chunk_to_chunk_map

        if remaining_texts:
            embeddings = self._generate_embeddings(remaining_texts)
            faiss.normalize_L2(embeddings)
            self.index.add(embeddings)

    def _generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.astype('float32')

    def get_document_stats(self, document_id: str) -> Dict[str, Any]:
        """Get statistics for a document"""
        if document_id not in self.chunks_storage:
            return {}

        chunks = self.chunks_storage[document_id]
        return {
            'total_chunks': len(chunks),
            'avg_chunk_length': np.mean([len(chunk.text) for chunk in chunks]),
            'total_characters': sum(len(chunk.text) for chunk in chunks)
        }

    def save_index(self, filepath: str):
        """Save the vector store to disk"""
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.faiss")
        
        # Save metadata
        metadata = {
            'chunks_storage': self.chunks_storage,
            'chunk_to_doc_map': self.chunk_to_doc_map,
            'chunk_to_chunk_map': self.chunk_to_chunk_map,
            'dimension': self.dimension
        }
        
        with open(f"{filepath}.pkl", 'wb') as f:
            pickle.dump(metadata, f)

    def load_index(self, filepath: str):
        """Load the vector store from disk"""
        # Load FAISS index
        self.index = faiss.read_index(f"{filepath}.faiss")
        
        # Load metadata
        with open(f"{filepath}.pkl", 'rb') as f:
            metadata = pickle.load(f)
            
        self.chunks_storage = metadata['chunks_storage']
        self.chunk_to_doc_map = metadata['chunk_to_doc_map']
        self.chunk_to_chunk_map = metadata['chunk_to_chunk_map']
        self.dimension = metadata['dimension']