"""FastAPI templates for code generation."""

FASTAPI_MAIN_TEMPLATE = '''"""
FastAPI Application - {project_name}
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="{project_name}", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
{models}

# In-memory database (replace with real DB later)
database = []

@app.get("/")
def read_root():
    """Root endpoint."""
    return {{"message": "Welcome to {project_name} API", "version": "1.0.0"}}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {{"status": "healthy"}}

{endpoints}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

FASTAPI_MODEL_TEMPLATE = '''
class {model_name}(BaseModel):
    """Model for {model_name}."""
{fields}
'''

FASTAPI_CRUD_ENDPOINTS_TEMPLATE = '''
@app.get("/{resource_plural}")
def get_{resource_plural}():
    """Get all {resource_plural}."""
    return {{"data": database, "count": len(database)}}

@app.get("/{resource_plural}/{{item_id}}")
def get_{resource_singular}(item_id: int):
    """Get a single {resource_singular} by ID."""
    if item_id < len(database):
        return database[item_id]
    raise HTTPException(status_code=404, detail="{resource_singular} not found")

@app.post("/{resource_plural}")
def create_{resource_singular}(item: {model_name}):
    """Create a new {resource_singular}."""
    database.append(item.dict())
    return {{"message": "{resource_singular} created", "id": len(database) - 1}}

@app.put("/{resource_plural}/{{item_id}}")
def update_{resource_singular}(item_id: int, item: {model_name}):
    """Update a {resource_singular}."""
    if item_id < len(database):
        database[item_id] = item.dict()
        return {{"message": "{resource_singular} updated"}}
    raise HTTPException(status_code=404, detail="{resource_singular} not found")

@app.delete("/{resource_plural}/{{item_id}}")
def delete_{resource_singular}(item_id: int):
    """Delete a {resource_singular}."""
    if item_id < len(database):
        database.pop(item_id)
        return {{"message": "{resource_singular} deleted"}}
    raise HTTPException(status_code=404, detail="{resource_singular} not found")
'''

FASTAPI_REQUIREMENTS = '''fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
python-multipart>=0.0.6
'''

FASTAPI_DOCKERFILE = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
