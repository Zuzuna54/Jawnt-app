from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Jawnt Banking API",
    description="API for managing bank accounts and payments",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api import accounts, payments

app.include_router(accounts.router, prefix="/api/v1", tags=["accounts"])
app.include_router(payments.router, prefix="/api/v1", tags=["payments"])

@app.get("/")
async def root():
    return {"message": "Welcome to Jawnt Banking API"} 