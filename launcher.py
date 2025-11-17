import os
import sys
import webbrowser
import time
import threading

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting Omar's Tools Backend...")
    print("📡 Server will run on http://localhost:8000")
    print("🌐 Browser will open automatically...")
    print()
    
    # Add backend to path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    # Import and run
    try:
        from main import app
        import uvicorn
        
        config = uvicorn.Config(
            app=app,
            host="127.0.0.1",
            port=8000,
            log_level="info"
        )
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        input("Press Enter to exit...")

def open_browser():
    """Open the frontend in default browser"""
    time.sleep(3)  # Wait for backend to start
    
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend', 'index.html')
    
    if os.path.exists(frontend_path):
        print("🌐 Opening browser...")
        webbrowser.open(f'file:///{os.path.abspath(frontend_path).replace(os.sep, "/")}')
    else:
        print(f"❌ Frontend file not found at: {frontend_path}")

if __name__ == "__main__":
    print("=" * 60)
    print("                  🎵 Omar's Tools 🎥                    ")
    print("         YouTube Downloader & Converter Suite           ")
    print("=" * 60)
    print()
    print("📝 Instructions:")
    print("   - Browser will open automatically")
    print("   - Keep this window open while using the app")
    print("   - Press Ctrl+C to stop the server")
    print()
    
    # Start browser in separate thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start backend (blocks)
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("              👋 Shutting down Omar's Tools...")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")