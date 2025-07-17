# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a full-stack DTSMS (Digital Transformation Service Management System) web application with a clear separation between frontend and backend:

- **Backend**: FastAPI-based REST API with PostgreSQL database
  - Located in `backend/app/`
  - Uses SQLAlchemy ORM with Alembic for database migrations
  - Implements JWT authentication and role-based access control
  - Modular router structure for different API endpoints (auth, users, roles, web-settings, libraries, tickets, uploaded-files)

- **Frontend**: Vue 3 + TypeScript + Vite application
  - Located in `frontend/app/vite-project/`
  - Uses Tailwind CSS for styling
  - Chart.js for data visualization
  - Drawflow for flowchart functionality
  - Vue Router for navigation

## Development Commands

### Backend (FastAPI)
```bash
# Start backend with Docker
cd backend
docker-compose up -d

# Database migrations
cd backend/app
alembic revision --autogenerate -m "migration_description"
alembic upgrade head
alembic downgrade -1
```

### Frontend (Vue 3)
```bash
# Development server (via Docker)
docker exec -ti frontend-pnpm-app-1 /bin/sh
cd vite-project/
pnpm run dev

# Build for production
pnpm run build

# Preview production build
pnpm run preview
```

## Database Schema

The application uses PostgreSQL with these main entities:
- Users (with role-based permissions)
- Roles
- Tickets
- Libraries
- Web Settings
- Uploaded Files
- File Tracking
- Processing Steps

## Key Configuration

- Backend runs on port 8000
- Frontend dev server on port 5173
- PostgreSQL on port 5432
- Database credentials: `dtsms_user:dtsms_password@db:5432/dtsms_db`
- Adminer (database UI) available on port 8080

## File Structure Notes

- Backend models in `backend/app/models/`
- API routes in `backend/app/routers/`
- Pydantic schemas in `backend/app/schemas/`
- Vue components in `frontend/app/vite-project/src/components/`
- Vue views in `frontend/app/vite-project/src/views/`
- Alembic migrations in `backend/app/alembic/versions/`