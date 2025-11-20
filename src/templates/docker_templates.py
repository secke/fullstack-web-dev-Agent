"""Docker templates for deployment."""

DOCKER_COMPOSE_TEMPLATE = '''version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./app.db
    volumes:
      - ./backend:/app
    networks:
      - app-network

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
'''

README_TEMPLATE = '''# {project_name}

Full-stack application with FastAPI backend and React frontend.

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

Backend will run on http://localhost:8000

#### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend will run on http://localhost:3000

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Project Structure

```
{project_name_lower}/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js      # Main React component
│   │   └── App.css
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📝 Development

### Adding New Endpoints

Edit `backend/main.py` to add new API endpoints.

### Modifying Frontend

Edit files in `frontend/src/` to modify the UI.

## 🐳 Docker Commands

```bash
# Build and start
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose build backend
docker-compose up backend
```

## 📄 License

MIT
'''

GITIGNORE_TEMPLATE = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Node
node_modules/
build/
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite

# Docker
.dockerignore
'''
