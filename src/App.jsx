import React, { useState } from 'react'
import Header from './components/Header'
import DocumentUpload from './components/DocumentUpload'
import ChatInterface from './components/ChatInterface'
import DocumentList from './components/DocumentList'

function App() {
  const [documents, setDocuments] = useState([])
  const [selectedDocument, setSelectedDocument] = useState(null)
  const [messages, setMessages] = useState([])

  const handleDocumentUploaded = (document) => {
    setDocuments(prev => [...prev, document])
    if (!selectedDocument) {
      setSelectedDocument(document)
    }
  }

  const handleDocumentSelect = (document) => {
    setSelectedDocument(document)
    setMessages([]) // Clear chat when switching documents
  }

  const handleNewMessage = (message) => {
    setMessages(prev => [...prev, message])
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <DocumentUpload onDocumentUploaded={handleDocumentUploaded} />
            <DocumentList 
              documents={documents}
              selectedDocument={selectedDocument}
              onDocumentSelect={handleDocumentSelect}
            />
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {selectedDocument ? (
              <ChatInterface 
                document={selectedDocument}
                messages={messages}
                onNewMessage={handleNewMessage}
              />
            ) : (
              <div className="bg-white rounded-lg shadow-sm border p-12 text-center">
                <div className="max-w-md mx-auto">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Upload a Document to Get Started
                  </h3>
                  <p className="text-gray-500">
                    Upload PDFs, Notion exports, or wiki pages to start asking questions and get intelligent answers.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App