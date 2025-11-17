# FastAPI Todo Application

A simple and efficient Todo API built with FastAPI and SQLite, providing full CRUD operations for managing todo items.

## Features

- Create new todo items
- Read all todos or a specific todo
- Update existing todos
- Delete todos
- Mark todos as complete/incomplete
- Filter todos by completion status
- Automatic API documentation with Swagger UI and ReDoc

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLite**: Lightweight database for data persistence
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-to-do
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server with:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Create a Todo
```http
POST /todos/
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```

### Get All Todos
```http
GET /todos/
```

Query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)
- `completed`: Filter by completion status (true/false)

Example:
```http
GET /todos/?completed=false&limit=10
```

### Get a Specific Todo
```http
GET /todos/{todo_id}
```

### Update a Todo
```http
PUT /todos/{todo_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

Note: All fields in the update request are optional.

### Delete a Todo
```http
DELETE /todos/{todo_id}
```

### Mark Todo as Complete
```http
PATCH /todos/{todo_id}/complete
```

### Mark Todo as Incomplete
```http
PATCH /todos/{todo_id}/incomplete
```

## Example Usage with cURL

Create a todo:
```bash
curl -X POST "http://localhost:8000/todos/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI","description":"Complete the tutorial","completed":false}'
```

Get all todos:
```bash
curl -X GET "http://localhost:8000/todos/"
```

Update a todo:
```bash
curl -X PUT "http://localhost:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn FastAPI","completed":true}'
```

Delete a todo:
```bash
curl -X DELETE "http://localhost:8000/todos/1"
```

## Project Structure

```
fastapi-to-do/
├── main.py           # FastAPI application and route handlers
├── models.py         # SQLAlchemy database models
├── schemas.py        # Pydantic schemas for validation
├── database.py       # Database configuration and connection
├── requirements.txt  # Python dependencies
├── .gitignore       # Git ignore file
└── README.md        # This file
```

## Database Schema

### Todo Table
- `id`: Integer (Primary Key)
- `title`: String (Required)
- `description`: String (Optional)
- `completed`: Boolean (Default: False)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-updated)

## Development

The application uses SQLite as the database, which will be created automatically as `todos.db` when you first run the application.

To reset the database, simply delete the `todos.db` file and restart the application.

## License

MIT License
