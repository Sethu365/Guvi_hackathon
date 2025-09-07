import React from 'react'
import { Brain, FileText } from 'lucide-react'

function Header() {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Intelligent Document Q&A
              </h1>
              <p className="text-sm text-gray-500">
                Ask questions about your documents
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <FileText className="w-4 h-4" />
            <span>Open-Source RAG System</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header