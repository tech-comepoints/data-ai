import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def main():
    """Run the FastAPI application locally"""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,  # Enable auto-reload
        workers=1
    )

if __name__ == "__main__":
    print("Starting News Analytics Dashboard...")
    print("API Key:", os.getenv("NEWS_API_KEY", "23c3692d06d049aea56bcbd896938f4f"))
    print("Server running at http://127.0.0.1:8080")
    print("Press Ctrl+C to stop the server")
    main() 