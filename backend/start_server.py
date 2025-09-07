"""
Start script for the Intelligent Document Q&A System backend
"""

import uvicorn
import os
import sys

def main():
    """Start the FastAPI server"""
    try:
        print("🚀 Starting Intelligent Document Q&A System Backend with Gemini...")
        print("🤖 Using Google Gemini API for answering questions")
        print("🌐 Server will be available at: http://localhost:8000")
        print("📖 API documentation at: http://localhost:8000/docs")
        print("\n" + "="*50)

        # Check Gemini API Key
        if not os.getenv("GEMINI_API_KEY"):
            print("❌ Error: GEMINI_API_KEY not found in environment variables.")
            print("👉 Please set it before starting: export GEMINI_API_KEY='your_api_key'")
            sys.exit(1)

        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
