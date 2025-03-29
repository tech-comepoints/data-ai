import uvicorn
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import subprocess

# Get the current directory (data-ai)
CURRENT_DIR = Path(__file__).parent

# Load environment variables from .env file if it exists
load_dotenv(CURRENT_DIR / '.env')

def kill_port(port):
    """Kill any process using the specified port"""
    try:
        if sys.platform == 'darwin':  # macOS
            cmd = f"lsof -ti:{port} | xargs kill -9"
        elif sys.platform == 'win32':  # Windows
            cmd = f"for /f \"tokens=5\" %a in ('netstat -aon ^| findstr :{port}') do taskkill /F /PID %a"
        else:  # Linux and others
            cmd = f"fuser -k {port}/tcp"
        
        subprocess.run(cmd, shell=True, check=True)
        print(f"Successfully killed process on port {port}")
    except subprocess.CalledProcessError:
        print(f"No process found on port {port}")
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")

def check_api_key():
    """Check if the NEWS_API_KEY environment variable is set"""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("Error: NEWS_API_KEY environment variable is not set")
        print("Please check that:")
        print("1. The .env file exists in the data-ai directory")
        print("2. The .env file contains: NEWS_API_KEY=your_api_key_here")
        print(f"3. The .env file is being read from: {CURRENT_DIR / '.env'}")
        sys.exit(1)
    return api_key

def main():
    """Run the FastAPI application locally"""
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", "8080"))
    
    try:
        print("Starting News Analytics Dashboard...")
        print("Server running at http://127.0.0.1:{port}".format(port=port))
        print("Press Ctrl+C to stop the server")
        
        # Try to kill any existing process on the port
        kill_port(port)
        
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=port,
            reload=True,  # Enable auto-reload
            workers=1
        )
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Error: Port {port} is still in use after attempting to kill the process.")
            print("Please try a different port using the PORT environment variable")
            sys.exit(1)
        else:
            raise e

if __name__ == "__main__":
    check_api_key()
    main() 