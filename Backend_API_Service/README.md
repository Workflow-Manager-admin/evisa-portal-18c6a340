# EVISA Portal Backend API Service

This is the backend API service for the Fiji Government's eVisa Portal project. It provides REST endpoints for core resources (users, applications, payments, notifications) and is designed to be easily integrated with Supabase and other service containers.

## Features

- FastAPI server with OpenAPI/Swagger docs
- Modular routers for users, visa applications, payments, notifications
- Environment-based configuration (`.env`)
- Ready for extension (service integrations, real DB, authentication)

## Running Locally

1. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

2. **Create a `.env` file**

   Copy `.env.example` as `.env` and configure as needed.

   ```
   cp .env.example .env
   ```

3. **Start the server**

   ```
   uvicorn main:app --reload
   ```

## Directory structure

- `main.py`: FastAPI server, registers routers
- `routers/`: Individual modules for users, applications, payments, notifications

## API Documentation

Once running, see:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Extension notes

- Replace the dummy in-memory stores with integration to Supabase or real database.
- Add authentication, authorization, and real notification sending as appropriate.
