from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing bank accounts and payments",
    version=settings.VERSION
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from app.api import accounts, payments, plaid

app.include_router(accounts.router, prefix=settings.API_V1_STR, tags=["accounts"])
app.include_router(payments.router, prefix=settings.API_V1_STR, tags=["payments"])
app.include_router(plaid.router, prefix=settings.API_V1_STR, tags=["plaid"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Jawnt Banking API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 