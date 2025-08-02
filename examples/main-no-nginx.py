from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# ... (existing imports)

app = FastAPI(
    title="Gästebuch API",
    description="Vollständiges Gästebuch-System mit Admin-Panel",
    version="1.0.0"
)

# CORS Configuration (nicht mehr nötig wenn alles auf einem Port läuft)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for CSS, JS, images etc.
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Your existing API routes here
# @app.post("/api/admin/login")
# @app.get("/api/reviews")
# etc...

# Catch-all route for React Router (MUST be last!)
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve React frontend for all non-API routes
    This handles client-side routing
    """
    # If it's an API route, let it be handled by actual API endpoints
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")

    # Check if it's a static file request
    file_path = f"static/{full_path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    # For all other routes, serve React's index.html
    # React Router will handle the routing client-side
    index_path = "static/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        raise HTTPException(status_code=404, detail="Frontend not found")

# Root route
@app.get("/")
async def read_root():
    """Serve React app at root"""
    return FileResponse("static/index.html")
