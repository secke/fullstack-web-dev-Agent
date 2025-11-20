# 🤖 Full-Stack Multi-Agent Development System

Un système multi-agent IA qui génère automatiquement des applications full-stack complètes (Backend FastAPI + Frontend React + Tests + Docker) en utilisant des modèles open source.

## 🎯 Concept

Ce système utilise **4 agents spécialisés** qui collaborent pour créer des applications complètes :

```
┌─────────────────────────────────────────────┐
│      Orchestrator Agent (Coordinateur)      │
│     "Je veux créer une API de blog"         │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
   ┌───▼────┐      ┌───▼────┐      ┌────▼────┐      ┌────▼────┐
   │Backend │      │Frontend│      │  Test   │      │ Docker  │
   │ Agent  │─────▶│ Agent  │─────▶│  Agent  │─────▶│  Agent  │
   │FastAPI │      │ React  │      │ Pytest  │      │Container│
   └────────┘      └────────┘      └─────────┘      └─────────┘
```

## 🏗️ Architecture

### Agents Spécialisés

1. **Backend Agent** 🔧
   - Génère du code FastAPI
   - Crée les modèles Pydantic
   - Implémente les endpoints CRUD
   - Ajoute authentification JWT (optionnel)
   - Intègre SQLAlchemy (optionnel)

2. **Frontend Agent** 🎨
   - Génère du code React
   - Crée les composants UI
   - Implémente la logique d'état
   - Gère les appels API
   - Ajoute React Router (optionnel)

3. **Test Agent** 🧪
   - Génère tests pytest pour backend
   - Génère tests Jest/RTL pour frontend
   - Crée des tests d'intégration
   - Configure le coverage

4. **Docker Agent** 🐳
   - Génère docker-compose.yml
   - Crée les Dockerfiles
   - Configure les réseaux
   - Génère README et documentation

5. **Orchestrator Agent** 🎭
   - Coordonne tous les agents
   - Comprend les besoins de haut niveau
   - Délègue les tâches
   - Assemble le projet final

## ✨ Fonctionnalités

✅ **Génération Automatique** : Créer une app complète en une commande
✅ **Multi-Agent** : Chaque agent est expert dans son domaine
✅ **Full-Stack** : Backend + Frontend + Tests + Docker
✅ **Personnalisable** : Définir ressources, champs, options
✅ **Production-Ready** : Code structuré et testé
✅ **Open Source** : Utilise des modèles gratuits (HuggingFace)

## 🚀 Installation

### Prérequis

- Python 3.9+
- pip
- Compte HuggingFace (gratuit)
- Docker (optionnel, pour lancer les apps générées)

### Setup

```bash
# 1. Cloner/naviguer vers le projet
cd fullstack-agent

# 2. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer .env
cp .env.example .env
nano .env  # Ajouter ton HF_TOKEN
```

### Obtenir un Token HuggingFace

1. Créer un compte sur https://huggingface.co
2. Aller dans Settings → Access Tokens
3. Créer un token (type: Read)
4. Le copier dans `.env`

## 📖 Utilisation

### Exemple Basique

```python
from src.agents.orchestrator import create_orchestrator

# Créer l'orchestrateur
orchestrator = create_orchestrator()

# Définir l'application
results = orchestrator.create_fullstack_app(
    project_name="Blog Platform",
    resource_name="Post",
    fields=[
        {"name": "title", "type": "str"},
        {"name": "content", "type": "str"},
        {"name": "author", "type": "str"},
    ],
    include_tests=True,
    include_docker=True
)
```

### Lancer l'Exemple

```bash
python examples/basic_usage.py
```

### Ce Qui Est Généré

```
outputs/
├── backend/
│   ├── main.py              # FastAPI app with CRUD
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       └── test_main.py
├── frontend/
│   ├── src/
│   │   ├── App.js          # React component
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml       # Orchestration
├── README.md               # Documentation
└── .gitignore
```

### Lancer l'Application Générée

```bash
cd outputs/
docker-compose up --build

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🎓 Exemples Avancés

### 1. Application avec Base de Données

```python
orchestrator.create_fullstack_app(
    project_name="Todo App",
    resource_name="Task",
    fields=[
        {"name": "title", "type": "str"},
        {"name": "completed", "type": "bool"},
    ],
    include_tests=True,
    include_docker=True,
    add_database=True  # Ajoute SQLite + SQLAlchemy
)
```

### 2. Étendre une Application Existante

```python
# Ajouter l'authentification
orchestrator.extend_application(
    project_path="outputs/backend",
    extension_type="auth"
)

# Ajouter React Router
orchestrator.extend_application(
    project_path="outputs/frontend",
    extension_type="routing"
)

# Ajouter Nginx
orchestrator.extend_application(
    project_path="outputs",
    extension_type="nginx"
)
```

### 3. Utiliser des Agents Individuels

```python
from src.agents.backend_agent import BackendAgent

# Utiliser uniquement le Backend Agent
backend_agent = BackendAgent()
backend_agent.generate_backend(
    project_name="My API",
    resource_name="User",
    fields=[{"name": "username", "type": "str"}]
)
```

## 🛠️ Configuration

### Modèles Disponibles

Dans `.env`, tu peux changer le modèle :

```bash
# Par défaut (recommandé)
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct

# Alternatives
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.3
HF_MODEL=HuggingFaceH4/zephyr-7b-beta
```

### Options de l'Orchestrateur

```python
create_orchestrator(
    model_id="meta-llama/Llama-3.1-8B-Instruct",  # Modèle à utiliser
    verbose=True  # Afficher le raisonnement des agents
)
```

## 📊 Structure du Projet

```
fullstack-agent/
├── src/
│   ├── agents/                 # Agents spécialisés
│   │   ├── orchestrator.py    # Agent coordinateur
│   │   ├── backend_agent.py   # Agent FastAPI
│   │   ├── frontend_agent.py  # Agent React
│   │   ├── docker_agent.py    # Agent Docker
│   │   └── test_agent.py      # Agent Tests
│   │
│   ├── tools/                  # Outils utilisés par les agents
│   │   └── code_generation.py # Tools de génération de code
│   │
│   ├── templates/              # Templates de code
│   │   ├── fastapi_templates.py
│   │   ├── react_templates.py
│   │   └── docker_templates.py
│   │
│   └── utils/                  # Utilitaires
│       ├── config.py          # Configuration
│       └── logger.py          # Logging
│
├── outputs/                    # Applications générées
├── examples/                   # Exemples d'utilisation
└── tests/                      # Tests du système
```

## 🎯 Use Cases

1. **Prototypage Rapide** : Créer des MVPs en quelques minutes
2. **Learning** : Apprendre les patterns full-stack
3. **Boilerplate** : Générer du code de base à customiser
4. **Microservices** : Créer plusieurs services rapidement
5. **Portfolio** : Générer des projets de démonstration

## 🔧 Personnalisation

### Ajouter un Nouveau Template

Éditer `src/templates/` pour ajouter tes propres templates.

### Créer un Nouvel Agent

```python
from smolagents import CodeAgent, InferenceClientModel
from src.tools.code_generation import CODE_GENERATION_TOOLS

class MyCustomAgent:
    def __init__(self):
        self.model = InferenceClientModel(model_id="...")
        self.agent = CodeAgent(
            tools=CODE_GENERATION_TOOLS,
            model=self.model
        )
    
    def my_custom_task(self, params):
        task = f"Generate ... based on {params}"
        return self.agent.run(task)
```

## 🐛 Troubleshooting

### Problème : HuggingFace Rate Limit

**Solution** : Attendre quelques minutes ou utiliser Ollama localement

### Problème : Code Généré Incomplet

**Solution** : Augmenter `MAX_STEPS` dans `.env`

### Problème : Tests Échouent

**Solution** : Vérifier les dépendances dans requirements.txt

## 🌟 Roadmap

### Phase 1 (Actuel) ✅
- [x] Architecture multi-agent
- [x] Backend FastAPI
- [x] Frontend React
- [x] Tests automatiques
- [x] Docker deployment

### Phase 2 (À Venir) 🔄
- [ ] Support GraphQL
- [ ] Support Vue.js/Svelte
- [ ] Intégration CI/CD
- [ ] Déploiement cloud (AWS, GCP, Azure)
- [ ] Monitoring et logging avancé

### Phase 3 (Futur) 🚀
- [ ] Support microservices complexes
- [ ] WebSockets et temps réel
- [ ] AI/ML model serving
- [ ] Dashboard d'administration

## 📝 License

MIT

## 🙏 Crédits

Développé avec :
- smolagents (HuggingFace)
- FastAPI
- React
- Docker

---

**Bon développement !** 🚀

Pour questions ou suggestions, consulter la documentation ou les exemples.
