from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from src.database.session import create_db_and_tables

# Load environment variables only in development
if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    # Add documentation URLs for production
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url=None if os.getenv("ENVIRONMENT") != "production" else None
)

# Configure allowed origins based on environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers for client-side access
    expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routes
from src.api.routes import auth, tasks

app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)