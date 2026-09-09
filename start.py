"""
Entry point for Render deployment.
Adds backend/ to sys.path so all imports resolve correctly.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

# Now import and run the app
from main import app  # noqa: F401 - imported for uvicorn to find

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("start:app", host="0.0.0.0", port=port)
