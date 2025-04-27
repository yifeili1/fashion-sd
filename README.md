# Fashion Design System

A fashion design system built on top of Stable Diffusion, featuring a RESTful API and database backend.

## Project Structure

```
fashion-sd/
├── models/           # Database models and initialization
├── config/          # Configuration files
├── service/         # RESTful service implementation
│   ├── __init__.py
│   ├── routes.py    # API endpoints
│   ├── models.py    # Database models
│   └── static/      # Static files (images)
├── tests/           # Test files
│   ├── conftest.py  # Test configuration
│   ├── test_models.py
│   └── test_routes.py
├── inference.py     # Image generation script
└── requirements.txt # Project dependencies
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database and update the configuration in `config/database.py`

3. Run the database initialization script:
```bash
python3 -m models.init_db
```

3. Starting All Services

To start the web UI, Flask RESTful API, and Streamlit frontend together, use the provided script:

```bash
chmod +x start_all.sh
./start_all.sh
```

This script will:
- Start the Stable Diffusion web UI in the background
- Wait for the web UI to be ready
- Start the Flask RESTful service
- Wait for the RESTful service to be ready
- Start the Streamlit frontend app

You can then access the services at:
- Streamlit frontend: http://<your-server-ip>:8501
- RESTful API: http://<your-server-ip>:5000

4. Run tests:
```bash
python3 -m pytest tests/
```

## Database Implementation

The system uses SQLAlchemy with PostgreSQL for data persistence. The database schema is defined in `service/models.py`:

### Schema

```sql
CREATE TABLE fashion_designs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt TEXT NOT NULL,
    negative_prompt TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Models

The `FashionDesign` model provides:
- CRUD operations (Create, Read, Update, Delete)
- Serialization/deserialization
- Query methods for finding designs
- Validation of design data

### Testing

Database tests are implemented in `tests/test_models.py` and include:
- Model creation and validation
- CRUD operations
- Serialization/deserialization
- Query methods
- Error handling

## RESTful Service Implementation

The RESTful service is built using Flask and provides the following endpoints:

### API Endpoints

- `GET /designs` - List all designs
- `POST /designs` - Create a new design
- `GET /designs/<id>` - Get a specific design
- `DELETE /designs/<id>` - Delete a design
- `GET /designs/search` - Search designs by prompt

### Features

- JSON request/response handling
- Input validation
- Error handling with appropriate HTTP status codes
- File upload and storage
- Search functionality

### Testing

API tests are implemented in `tests/test_routes.py` and include:
- Endpoint availability
- Request/response handling
- Error cases
- File operations
- Search functionality

## Configuration

The service can be configured through environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `STATIC_DIR`: Directory for storing generated images
- `API_HOST`: Host address for the API server
- `API_PORT`: Port for the API server

## Development

1. Set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python3 service/__init__.py
```

4. Run tests:
```bash
python3 -m pytest tests/
```

## API Documentation

### List Designs
```http
GET /designs
```

Example command:
```bash
curl -X GET http://localhost:5000/designs
```

Response:
```json
[
  {
    "id": "uuid",
    "prompt": "string",
    "negative_prompt": "string",
    "width": 512,
    "height": 512,
    "file_path": "string",
    "created_at": "timestamp"
  }
]
```

### Create Design
```http
POST /designs
Content-Type: application/json
```

Example command:
```bash
curl -X POST http://localhost:5000/designs \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "female, long dress, red dress, high-heeled shoes",
    "width": 512,
    "height": 1024
  }'
```

Response:
```json
{
  "id": "uuid",
  "prompt": "string",
  "negative_prompt": "string",
  "width": 512,
  "height": 512,
  "file_path": "string",
  "created_at": "timestamp"
}
```

### Get Design
```http
GET /designs/{id}
```

Example command:
```bash
curl -X GET http://localhost:5000/designs/123e4567-e89b-12d3-a456-426614174000
```

Response:
```json
{
  "id": "uuid",
  "prompt": "string",
  "negative_prompt": "string",
  "width": 512,
  "height": 512,
  "file_path": "string",
  "created_at": "timestamp"
}
```

### Delete Design
```http
DELETE /designs/{id}
```

Example command:
```bash
curl -X DELETE http://localhost:5000/designs/123e4567-e89b-12d3-a456-426614174000
```

Response: 204 No Content

### Search Designs
```http
GET /designs/search?prompt={query}
```

Example command:
```bash
curl -X GET "http://localhost:5000/designs/search?prompt=modern%20dress"
```

Response:
```json
[
  {
    "id": "uuid",
    "prompt": "string",
    "negative_prompt": "string",
    "width": 512,
    "height": 512,
    "file_path": "string",
    "created_at": "timestamp"
  }
]
```

### Download Design Image
```http
GET /designs/{id}/image
```

Example command:
```bash
curl -X GET http://localhost:5000/designs/123e4567-e89b-12d3-a456-426614174000/image \
  --output design_image.png
```

Response: Binary image data

### Error Responses

The API returns appropriate HTTP status codes and error messages:

```bash
# Example of a 400 Bad Request
curl -X POST http://localhost:5000/designs \
  -H "Content-Type: application/json" \
  -d '{"prompt": ""}'

# Response:
{
  "error": "Prompt cannot be empty"
}

# Example of a 404 Not Found
curl -X GET http://localhost:5000/designs/nonexistent-id

# Response:
{
  "error": "Design not found"
}
```

### Testing API Endpoints

You can use the following commands to test all endpoints:

```bash
# List all designs
curl -X GET http://localhost:5000/designs

# Create a new design
curl -X POST http://localhost:5000/designs \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "modern dress, floral pattern, elegant",
    "negative_prompt": "ugly, blurry, low quality",
    "width": 512,
    "height": 512
  }'

# Get a specific design (replace {id} with actual UUID)
curl -X GET http://localhost:5000/designs/{id}

# Search designs
curl -X GET "http://localhost:5000/designs/search?prompt=modern%20dress"

# Delete a design (replace {id} with actual UUID)
curl -X DELETE http://localhost:5000/designs/{id}

# Download design image (replace {id} with actual UUID)
curl -X GET http://localhost:5000/designs/{id}/image --output design_image.png
```

## Frontend Implementation

The project includes a modern Streamlit-based frontend for interacting with the Fashion Design RESTful API. The frontend provides:
- A gallery page to browse generated designs
- A creation page to generate new designs using text prompts
- A details page to view, download, or delete a design
- An about page with project information

The frontend communicates with the backend RESTful API and displays images and metadata in a user-friendly interface.

