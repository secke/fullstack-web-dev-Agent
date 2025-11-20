# 🚀 Quick Start Guide - Full-Stack Multi-Agent System

## En 5 Minutes ⏱️

### 1. Installation (2 min)

```bash
cd fullstack-agent

# Créer venv et installer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration (1 min)

```bash
# Copier le template
cp .env.example .env

# Éditer et ajouter ton token HuggingFace
nano .env
```

**Token HuggingFace** : https://huggingface.co/settings/tokens

### 3. Générer Ta Première App (2 min)

```bash
python examples/basic_usage.py
```

Ceci génère une application **Blog Platform** complète dans `outputs/`!

### 4. Lancer l'Application

```bash
cd outputs/
docker-compose up --build

# Accès :
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🎯 Ce Qui Est Généré

```
outputs/
├── backend/           ← FastAPI avec CRUD complet
├── frontend/          ← React app moderne
├── docker-compose.yml ← Orchestration
└── README.md         ← Documentation
```

## 💡 Usage Programmatique

```python
from src.agents.orchestrator import create_orchestrator

# Créer l'orchestrateur
orchestrator = create_orchestrator()

# Générer une app
results = orchestrator.create_fullstack_app(
    project_name="Mon App",
    resource_name="Item",
    fields=[
        {"name": "title", "type": "str"},
        {"name": "description", "type": "str"}
    ],
    include_tests=True,
    include_docker=True
)

# C'est tout ! 🎉
```

## 🔥 Exemples Rapides

### Todo App

```python
orchestrator.create_fullstack_app(
    project_name="Todo App",
    resource_name="Task",
    fields=[
        {"name": "title", "type": "str"},
        {"name": "completed", "type": "bool"}
    ]
)
```

### User Management

```python
orchestrator.create_fullstack_app(
    project_name="User System",
    resource_name="User",
    fields=[
        {"name": "username", "type": "str"},
        {"name": "email", "type": "str"}
    ]
)
```

### E-commerce Product

```python
orchestrator.create_fullstack_app(
    project_name="Shop",
    resource_name="Product",
    fields=[
        {"name": "name", "type": "str"},
        {"name": "price", "type": "float"},
        {"name": "stock", "type": "int"}
    ]
)
```

## 🎨 Personnaliser

### Avec Base de Données

```python
orchestrator.create_fullstack_app(
    # ... params
    add_database=True  # Ajoute SQLite + SQLAlchemy
)
```

### Sans Tests

```python
orchestrator.create_fullstack_app(
    # ... params
    include_tests=False  # Plus rapide
)
```

### Sans Docker

```python
orchestrator.create_fullstack_app(
    # ... params
    include_docker=False  # Juste le code
)
```

## 🛠️ Agents Individuels

Tu peux aussi utiliser les agents séparément :

```python
from src.agents.backend_agent import BackendAgent

# Backend uniquement
backend = BackendAgent()
backend.generate_backend(
    project_name="My API",
    resource_name="Post",
    fields=[{"name": "title", "type": "str"}]
)
```

## ⚡ Tips

### Modèle Local (Pas de Rate Limit)

Installer Ollama et utiliser :
```bash
ollama pull llama3.1:8b
```

Puis dans le code :
```python
from smolagents import LiteLLMModel

model = LiteLLMModel(model_id="ollama/llama3.1:8b")
```

### Verbose Mode

Pour voir le raisonnement des agents :
```python
orchestrator = create_orchestrator(verbose=True)
```

### Mode Non-Verbeux

Pour un output propre :
```python
orchestrator = create_orchestrator(verbose=False)
```

## 🐛 Problèmes Courants

### HuggingFace Rate Limit
**Solution** : Attendre ou utiliser Ollama localement

### Dépendances Manquantes
```bash
pip install --upgrade -r requirements.txt
```

### Docker Pas Installé
**Solution** : Générer sans Docker ou installer Docker

## 📚 Aller Plus Loin

- Lire **README.md** pour la doc complète
- Explorer `examples/` pour plus d'exemples
- Modifier `src/templates/` pour personnaliser le code généré
- Créer tes propres agents dans `src/agents/`

## 🎉 C'est Parti !

Tu es prêt à générer des applications full-stack automatiquement ! 🚀

**Questions ?** Consulter le README.md complet.
