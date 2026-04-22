# Room Editor Backend

Backend API for Room Editor - a 3D room design application that allows users to create and customize interior designs with 3D object placement.

## Table of Contents
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Database](#database)
- [API Endpoints](#api-endpoints)
- [Development](#development)

## Technologies

- **Python 3.x**
- **FastAPI** - Web framework for building APIs
- **SQLAlchemy** - ORM for database interactions
- **PostgreSQL** - Relational database
- **Docker & Docker Compose** - Containerization

## Project Structure

```
backend/
├── app/
│   ├── api/          # API route handlers
│   ├── core/         # Core application components
│   ├── models.py     # Database models
│   └── main.py       # Application entry point
├── pgdata/           # PostgreSQL data (gitignored)
├── docker-compose.yml # Docker configuration
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (not included in repo)
```

## Setup

### Prerequisites
- Python 3.x
- Docker & Docker Compose
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the database using Docker:
```bash
docker-compose up -d
```

4. Run the FastAPI application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Database

The project uses PostgreSQL as its database, configured with Docker Compose:

- **Port**: 5434 (external), 5432 (internal)
- **Database Name**: RoomEditor
- **Username**: postgres
- **Password**: StrongPassword01

Adminer interface is available at `http://localhost:8081` for database management.

### Models

The database consists of the following models:

- **User**: Application users with login credentials
- **Project**: User-created room design projects
- **ProjectItem**: Individual 3D objects placed in a project
- **Object3D**: Available 3D objects with model information
- **Object3DCategory**: Categories for organizing 3D objects

## API Endpoints

The API provides endpoints for:

- User authentication and management (`/api/users`)
- Project creation and management (`/api/projects`)
- 3D objects catalog browsing (`/api/3d-objects`)
- Health check (`/api/status`)

Detailed API documentation is available at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## Development

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=postgresql://postgres:StrongPassword01@localhost:5434/RoomEditor
```

### CORS Configuration

CORS is configured to allow requests from:
- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `http://localhost:5174`

Adjust these settings in `app/main.py` as needed for your frontend development.

### Code Structure

- `app/main.py`: Application entry point with FastAPI initialization
- `app/models.py`: Database models using SQLAlchemy
- `app/core/database.py`: Database connection configuration
- `app/api/`: API route handlers organized by resource
- `app/api/dtos.py`: Data Transfer Objects for request/response validation