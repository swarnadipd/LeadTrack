# LeadTrack

A small CRM-style REST API for managing sales leads, built with **FastAPI, PostgreSQL, SQLAlchemy, Docker, and Nginx**.

LeadTrack provides CRUD operations for sales leads and demonstrates a simple multi-container backend architecture with two FastAPI instances behind an Nginx reverse proxy/load balancer.

## Overview

A lead contains:

- `name`
- `email`
- `company`
- `status`

The API supports creating, reading, updating, filtering, and deleting leads.

The application can run as a single FastAPI service locally, or as a Docker Compose setup with two API instances and an Nginx load balancer.

## Tech Stack

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| **FastAPI**        | REST API framework              |
| **Python 3.12**    | Backend language                |
| **PostgreSQL 16**  | Persistent relational database  |
| **SQLAlchemy**     | ORM and database interaction    |
| **Pydantic**       | Request/response validation     |
| **Docker**         | Containerization                |
| **Docker Compose** | Multi-container orchestration   |
| **Nginx**          | Reverse proxy and load balancer |

## Architecture

```text
                    Client
                      |
                      | HTTP
                      v
              +---------------+
              |     Nginx     |
              | Reverse Proxy |
              | Load Balancer |
              +-------+-------+
                      |
             +--------+--------+
             |                 |
             v                 v
      +-------------+   +-------------+
      |    API 1    |   |    API 2    |
      |   FastAPI   |   |   FastAPI   |
      +------+------+   +------+------+
             |                 |
             +--------+--------+
                      |
                      v
              +---------------+
              |  PostgreSQL   |
              |   Database    |
              +---------------+
```

Nginx distributes incoming requests between the two FastAPI instances using round-robin load balancing.

Each API instance connects to the same PostgreSQL database, so application state is persisted centrally rather than being stored inside an individual API container.

## Features

- Create a lead
- List all leads
- Filter leads by status
- Retrieve a lead by ID
- Update a lead using PATCH
- Delete a lead
- Health-check endpoint
- Two FastAPI application instances
- Nginx reverse proxy and round-robin load balancing
- PostgreSQL persistence
- Interactive API documentation through FastAPI Swagger UI

## API Endpoints

| Method   | Endpoint           | Description                                     |
| -------- | ------------------ | ----------------------------------------------- |
| `GET`    | `/health`          | Returns API health and the responding container |
| `POST`   | `/leads`           | Creates a new lead                              |
| `GET`    | `/leads`           | Returns all leads                               |
| `GET`    | `/leads/{lead_id}` | Returns a lead by ID                            |
| `PATCH`  | `/leads/{lead_id}` | Updates an existing lead                        |
| `DELETE` | `/leads/{lead_id}` | Deletes a lead                                  |

### Example Lead

```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "company": "Acme Corp",
  "status": "new"
}
```

## Running with Docker

The recommended way to run the complete application is Docker Compose.

### 1. Clone the repository

```bash
git clone https://github.com/swarnadipd/LeadTrack.git
cd leadtrack
```

### 2. Start the application

```bash
docker compose up --build
```

This starts four services:

- `db` — PostgreSQL
- `api1` — FastAPI instance 1
- `api2` — FastAPI instance 2
- `nginx` — reverse proxy/load balancer

### 3. Open the API documentation

Once the containers are running:

**http://localhost:8080/docs**

FastAPI provides an interactive Swagger UI where the endpoints can be tested directly from the browser.

### 4. Test the health endpoint

```bash
curl http://localhost:8080/health
```

The response includes the hostname of the FastAPI container that handled the request.

Calling the endpoint repeatedly can demonstrate requests being distributed between the two API instances.

### 5. Stop the application

Press `Control + C`, then:

```bash
docker compose down
```

> PostgreSQL data is stored in the Docker volume defined by Docker Compose.

## Project Structure

```text
leadtrack/
├── main.py               # FastAPI application and API endpoints
├── database.py           # SQLAlchemy engine, session, and database setup
├── models.py             # SQLAlchemy database models
├── schemas.py            # Pydantic request/response schemas
├── requirements.txt      # Python dependencies
├── Dockerfile            # FastAPI container image definition
├── docker-compose.yml    # Multi-container application configuration
├── nginx.conf             # Nginx reverse proxy/load-balancer configuration
├── README.md              # Project documentation
└── .gitignore
```

## Design Notes

### Separate API schemas and database models

Pydantic schemas in `schemas.py` define the data accepted and returned by the API, while SQLAlchemy models in `models.py` represent the database structure.

This keeps the API contract separate from the persistence layer.

### Multiple API instances

The same FastAPI application is run in two containers (`api1` and `api2`).

Nginx sits in front of them and distributes requests across the available instances.

### Shared database

Both API instances use the same PostgreSQL database, allowing either instance to read and write the same application data.

## What This Project Demonstrates

- Designing a REST API with FastAPI
- Request and response validation with Pydantic
- Relational data persistence with PostgreSQL
- ORM-based database interaction using SQLAlchemy
- Containerizing a Python backend with Docker
- Running multiple application instances with Docker Compose
- Reverse proxying and load balancing with Nginx
- Debugging service startup and container-to-container connectivity

## Future Improvements

Possible next steps for the project include:

- PostgreSQL health checks and more robust service startup handling
- Database migrations with Alembic
- Authentication and authorization
- Stronger validation for lead status values
- Automated tests
- Structured application logging
- CI/CD
- Production deployment

## Author

**Swarnadip Dasgupta**

GitHub: `https://github.com/swarnadipd`
