import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import axios from 'axios'

function DocumentUpload({ onDocumentUploaded }) {
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState(null)

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return

    setUploading(true)
    setUploadStatus(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setUploadStatus({ type: 'success', message: 'Document uploaded successfully!' })
      onDocumentUploaded(response.data)
    } catch (error) {
      console.error('Upload error:', error)
      setUploadStatus({ 
        type: 'error', 
        message: error.response?.data?.error || 'Failed to upload document' 
      })
    } finally {
      setUploading(false)
    }
  }, [onDocumentUploaded])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/markdown': ['.md'],
      'text/html': ['.html'],
      'text/plain': ['.txt']
    },
    maxFiles: 1,
    disabled: uploading
  })

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Upload Document</h2>
      
      <div
        {...getRootProps()}
        className={`upload-zone ${isDragActive ? 'active' : ''} ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center">
          {uploading ? (
            <Loader2 className="w-8 h-8 text-primary-600 animate-spin mb-3" />
          ) : (
            <Upload className="w-8 h-8 text-gray-400 mb-3" />
          )}
          
          <div className="text-center">
            {uploading ? (
              <p className="text-sm text-gray-600">Processing document...</p>
            ) : isDragActive ? (
              <p className="text-sm text-primary-600 font-medium">Drop the file here</p>
            ) : (
              <>
                <p className="text-sm text-gray-600 mb-1">
                  <span className="font-medium text-primary-600">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-gray-500">
                  PDF, Markdown, HTML, or TXT files
                </p>
              </>
            )}
          </div>
        </div>
      </div>

      {uploadStatus && (
        <div className={`mt-4 p-3 rounded-md flex items-center space-x-2 ${
          uploadStatus.type === 'success' 
            ? 'bg-green-50 text-green-800' 
            : 'bg-red-50 text-red-800'
        }`}>
          {uploadStatus.type === 'success' ? (
            <CheckCircle className="w-4 h-4" />
          ) : (
            <AlertCircle className="w-4 h-4" />
          )}
          <span className="text-sm">{uploadStatus.message}</span>
        </div>
      )}
    </div>
  )
}

export default DocumentUpload