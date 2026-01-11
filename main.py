from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from api.endpoints import router as blog_router

# Get the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title='My Blog')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include blog API routes
app.include_router(blog_router)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse(str(BASE_DIR / "static" / "index.html"))