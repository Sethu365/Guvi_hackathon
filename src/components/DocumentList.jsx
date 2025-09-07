import React from 'react'
import { FileText, File } from 'lucide-react'

function DocumentList({ documents, selectedDocument, onDocumentSelect }) {
  if (documents.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Documents</h2>
        <div className="text-center py-8">
          <File className="w-8 h-8 text-gray-300 mx-auto mb-2" />
          <p className="text-sm text-gray-500">No documents uploaded yet</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Documents</h2>
      
      <div className="space-y-2">
        {documents.map((doc) => (
          <button
            key={doc.id}
            onClick={() => onDocumentSelect(doc)}
            className={`w-full text-left p-3 rounded-lg border transition-colors ${
              selectedDocument?.id === doc.id
                ? 'bg-primary-50 border-primary-200 text-primary-900'
                : 'bg-gray-50 border-gray-200 hover:bg-gray-100 text-gray-700'
            }`}
          >
            <div className="flex items-start space-x-3">
              <FileText className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                selectedDocument?.id === doc.id ? 'text-primary-600' : 'text-gray-400'
              }`} />
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium truncate">{doc.filename}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {doc.pages ? `${doc.pages} pages` : `${doc.chunks} chunks`} • {doc.type}
                </p>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default DocumentList