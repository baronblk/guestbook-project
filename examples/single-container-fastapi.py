from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# API Routes
@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/admin/login")
async def login():
    # Your login logic here
    pass

# Mount static files (React build)
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Serve React App for all other routes
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """
    Serve React app for all non-API routes
    This handles React Router client-side routing
    """
    # Check if file exists in build directory
    file_path = f"frontend/build/{full_path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    # For all other routes, serve index.html (React will handle routing)
    return FileResponse("frontend/build/index.html")

# Alternative: Explicit root route
@app.get("/")
async def read_root():
    return FileResponse("frontend/build/index.html")
