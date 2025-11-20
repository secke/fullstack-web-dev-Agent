# Changelog - Full-Stack Multi-Agent System

## Version 2.0.0 - Architecture majeure mise à jour (Date actuelle)

### 🎉 Nouvelles Fonctionnalités

#### Mode Autonome
- **PlannerAgent**: Nouveau agent qui analyse les descriptions en langage naturel
- **create_from_description()**: Créez des applications complètes à partir d'une simple description
- Plus besoin de spécifier manuellement project_name, resources, fields
- Le système extrait automatiquement toutes les informations nécessaires

**Exemple:**
```python
orchestrator = OrchestratorAgent()
result = orchestrator.create_from_description(
    "Je veux créer une plateforme de blog où les utilisateurs peuvent créer, "
    "modifier et supprimer des articles."
)
```

### 🔧 Améliorations Architecturales

#### BaseAgent
- Nouvelle classe de base pour tous les agents spécialisés
- Élimine la duplication de code (~80 lignes de code dupliqué supprimées)
- Partage d'instance du modèle entre tous les agents (optimisation mémoire)
- Gestion centralisée de l'initialisation

#### Optimisation des Performances
- **Modèle partagé**: Une seule instance de InferenceClientModel pour tous les agents
- Réduction de l'utilisation mémoire
- Initialisation plus rapide

#### Paramètre verbose activé
- Le paramètre `verbose` fonctionne maintenant correctement
- Contrôle de la verbosité de la sortie pour tous les agents

### 🐛 Corrections de Bugs

1. **Chemins hardcodés corrigés** (`src/tools/code_generation.py`)
   - Utilise maintenant `settings.OUTPUTS_DIR` au lieu de chemins en dur
   - Fonctionne depuis n'importe quel répertoire

2. **Bug d'authentification corrigé** (`src/agents/backend_agent.py`)
   - Correction du mot "password" coupé en deux lignes
   - JWT authentication fonctionne correctement maintenant

3. **Imports inutilisés nettoyés**
   - Suppression des imports non utilisés
   - Code plus propre et maintenable

### 📝 Structure des Agents

```
BaseAgent (nouveau)
    ├── PlannerAgent (nouveau)
    ├── BackendAgent (mis à jour)
    ├── FrontendAgent (mis à jour)
    ├── DockerAgent (mis à jour)
    └── TestAgent (mis à jour)
```

### 📚 Nouvelle Documentation

- `examples/autonomous_mode.py`: Exemples d'utilisation du mode autonome
- `CHANGELOG.md`: Ce fichier
- Documentation mise à jour dans tous les agents

### 🔄 Migration depuis v1.x

**Ancien code (v1.x):**
```python
orchestrator = OrchestratorAgent()
result = orchestrator.create_fullstack_app(
    project_name="blog-platform",
    resource_name="Post",
    fields=[
        {"name": "title", "type": "str"},
        {"name": "content", "type": "str"},
        {"name": "author", "type": "str"},
    ]
)
```

**Nouveau code (v2.0) - Toujours supporté:**
```python
orchestrator = OrchestratorAgent()
# Mode manuel (rétrocompatible)
result = orchestrator.create_fullstack_app(
    project_name="blog-platform",
    resource_name="Post",
    fields=[...]
)

# OU Mode autonome (nouveau!)
result = orchestrator.create_from_description(
    "Créer une plateforme de blog avec des articles"
)
```

### 🎯 Améliorations Futures (v2.1+)

- [ ] TemplateManager pour utiliser réellement les templates Jinja2
- [ ] Tests unitaires complets du système
- [ ] Support multi-ressources (plusieurs entités dans une app)
- [ ] Interface de raffinement interactive
- [ ] Cache des analyses PlannerAgent
- [ ] Support des frameworks alternatifs (Vue, Django, etc.)

---

## Version 1.0.0 - Version initiale

### Fonctionnalités
- Génération d'applications full-stack (FastAPI + React)
- Agents spécialisés: Backend, Frontend, Docker, Test
- Mode manuel avec paramètres structurés
- Support Docker et docker-compose
- Génération de tests pytest et Jest
