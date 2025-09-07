import React, { useState, useRef, useEffect } from 'react'
import { Send, Loader2, User, Bot, ExternalLink } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import axios from 'axios'

function ChatInterface({ document, messages, onNewMessage }) {
  const [question, setQuestion] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!question.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: question,
      timestamp: new Date()
    }

    onNewMessage(userMessage)
    setQuestion('')
    setIsLoading(true)

    try {
      const response = await axios.post('/api/query', {
        document_id: document.id,
        question: question
      })

      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.data.answer,
        sources: response.data.sources,
        timestamp: new Date()
      }

      onNewMessage(assistantMessage)
    } catch (error) {
      console.error('Query error:', error)
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
        error: true,
        timestamp: new Date()
      }
      onNewMessage(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border h-[600px] flex flex-col">
      {/* Header */}
      <div className="p-4 border-b bg-gray-50 rounded-t-lg">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
            <Bot className="w-4 h-4 text-primary-600" />
          </div>
          <div>
            <h3 className="font-medium text-gray-900">Ask about: {document.filename}</h3>
            <p className="text-sm text-gray-500">
              {document.pages ? `${document.pages} pages` : `${document.chunks} chunks`} processed
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center py-8">
            <Bot className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <h4 className="text-lg font-medium text-gray-900 mb-2">
              Ready to answer your questions
            </h4>
            <p className="text-gray-500 max-w-md mx-auto">
              Ask me anything about "{document.filename}". I'll search through the document 
              and provide you with accurate, contextual answers.
            </p>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className={`chat-message ${
            message.type === 'user' ? 'user-message' : 'assistant-message'
          }`}>
            <div className="flex items-start space-x-3">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                message.type === 'user' 
                  ? 'bg-primary-600 text-white' 
                  : message.error 
                    ? 'bg-red-100 text-red-600'
                    : 'bg-gray-100 text-gray-600'
              }`}>
                {message.type === 'user' ? (
                  <User className="w-4 h-4" />
                ) : (
                  <Bot className="w-4 h-4" />
                )}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
                
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <p className="text-xs font-medium text-gray-500 mb-2">Sources:</p>
                    <div className="space-y-1">
                      {message.sources.map((source, index) => (
                        <div key={index} className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                          <div className="flex items-center justify-between">
                            <span className="font-medium">
                              {source.page ? `Page ${source.page}` : `Chunk ${source.chunk_id}`}
                            </span>
                            <span className="text-gray-400">
                              Score: {(source.score * 100).toFixed(1)}%
                            </span>
                          </div>
                          <p className="mt-1 line-clamp-2">{source.text}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                <p className="text-xs text-gray-400 mt-2">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="chat-message assistant-message">
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                <Loader2 className="w-4 h-4 text-gray-600 animate-spin" />
              </div>
              <div className="flex-1">
                <p className="text-gray-500">Thinking...</p>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question about this document..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!question.trim() || isLoading}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  )
}

export default ChatInterface