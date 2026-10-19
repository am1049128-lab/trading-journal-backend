from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base
from routes import auth, trades, analytics

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trading Journal API",
    description="Stock Portfolio Tracker with Trading Journal and Analytics",
    version="1.0.0"
)

# CORS middleware - allow frontend origin
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "https://*.vercel.app",  # Vercel preview & production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(trades.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {
        "message": "Trading Journal API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
