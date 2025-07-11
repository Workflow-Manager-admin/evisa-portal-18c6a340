import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from routers import users, applications, payments, notifications

# Load environment variables from .env (so devs can configure service without code changes)
load_dotenv()

# OpenAPI tag metadata for grouping endpoints
openapi_tags = [
    {"name": "Users", "description": "User operations (registration, profiles)"},
    {"name": "Applications", "description": "Visa Application management"},
    {"name": "Payments", "description": "eVisa payment processing"},
    {"name": "Notifications", "description": "Email/SMS notification operations"},
]

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""
    app = FastAPI(
        title="EVISA Portal Backend API",
        description=(
            "API for managing users, applications, payments, notifications for the Fiji eVisa Portal."
            " Provides core platform features with OpenAPI and Swagger documentation."
        ),
        version="1.0.0",
        openapi_tags=openapi_tags,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS setup (update allowed origins as needed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this to trusted origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(users.router)
    app.include_router(applications.router)
    app.include_router(payments.router)
    app.include_router(notifications.router)

    return app

app = create_app()

# PUBLIC_INTERFACE
@app.get("/", tags=["Root"])
async def root():
    """
    Healthcheck and welcome endpoint.
    Returns a welcome message.
    """
    return {
        "message": "Welcome to the Fiji eVisa Portal Backend API",
        "status": "ok"
    }
