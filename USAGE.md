# Guide d'Utilisation - Full-Stack Multi-Agent System v2.0

## Table des Matières
- [Introduction](#introduction)
- [Mode Autonome (Nouveau!)](#mode-autonome)
- [Mode Manuel (Classique)](#mode-manuel)
- [Exemples Détaillés](#exemples-détaillés)
- [API Reference](#api-reference)

## Introduction

Le système Full-Stack Multi-Agent permet de générer des applications web complètes (backend + frontend + Docker + tests) de deux manières:

1. **Mode Autonome** 🆕: Décrivez simplement ce que vous voulez en langage naturel
2. **Mode Manuel**: Spécifiez précisément tous les paramètres

## Mode Autonome

### Utilisation de Base

```python
from src.agents import OrchestratorAgent

# Créer l'orchestrateur
orchestrator = OrchestratorAgent(verbose=True)

# Décrire votre application en langage naturel
description = """
Je veux créer une plateforme de blog où les utilisateurs peuvent:
- Créer de nouveaux articles avec un titre, contenu, et auteur
- Modifier leurs articles existants
- Supprimer des articles
- Voir la liste de tous les articles

Chaque article doit avoir une date de publication.
"""

# Laisser le système faire le reste!
result = orchestrator.create_from_description(description)
```

### Ce que le Système Extrait Automatiquement

Le **PlannerAgent** analyse votre description et extrait:

1. **Nom du projet**: Généré à partir de la description
2. **Resources**: Identifie les entités principales (Post, User, Product, etc.)
3. **Champs**: Détermine les champs avec leurs types appropriés
4. **Features**: Liste les fonctionnalités à implémenter
5. **Tech Stack**: Choix des technologies (FastAPI, React, base de données)
6. **Options**: Tests, Docker, base de données

### Exemples de Descriptions

#### Exemple 1: E-Commerce
```python
description = """
Construire une boutique en ligne où les clients peuvent acheter des produits.
Chaque produit a un nom, description, prix, quantité en stock, et catégorie.
"""

result = orchestrator.create_from_description(description)
```

**Extraction automatique:**
- Project name: `online-store`
- Resource: `Product`
- Fields: `id`, `name`, `description`, `price` (float), `stock` (int), `category`

#### Exemple 2: Gestionnaire de Tâches
```python
description = """
Application de gestion de tâches avec:
- Titre de la tâche
- Description
- Date limite
- Priorité (haute, moyenne, basse)
- Statut (à faire, en cours, terminé)
"""

result = orchestrator.create_from_description(description)
```

**Extraction automatique:**
- Project name: `task-manager`
- Resource: `Task`
- Fields: `id`, `title`, `description`, `due_date`, `priority`, `status`

#### Exemple 3: Réseau Social
```python
description = """
Créer un réseau social simple où les utilisateurs peuvent publier des messages.
Chaque message a un contenu, auteur, nombre de likes, et timestamp.
Les utilisateurs peuvent liker et commenter les messages.
"""

result = orchestrator.create_from_description(description)
```

## Mode Manuel

Pour un contrôle précis, utilisez le mode manuel:

```python
from src.agents import OrchestratorAgent

orchestrator = OrchestratorAgent(verbose=True)

result = orchestrator.create_fullstack_app(
    project_name="blog-platform",
    resource_name="Post",
    fields=[
        {"name": "id", "type": "int"},
        {"name": "title", "type": "str"},
        {"name": "content", "type": "str"},
        {"name": "author", "type": "str"},
        {"name": "published_at", "type": "date"},
    ],
    include_tests=True,
    include_docker=True,
    add_database=False,
)
```

### Types de Champs Supportés

- `str`: Chaînes de caractères
- `int`: Nombres entiers
- `float`: Nombres décimaux
- `bool`: Booléens (True/False)
- `date`: Dates

## Exemples Détaillés

### Exemple Complet avec Toutes les Options

```python
from src.agents import OrchestratorAgent

def create_advanced_blog():
    """Créer un blog avec toutes les fonctionnalités."""

    # 1. Initialiser l'orchestrateur
    orchestrator = OrchestratorAgent(
        model_id="meta-llama/Llama-3.1-8B-Instruct",  # Optionnel
        verbose=True  # Afficher les logs détaillés
    )

    # 2. Décrire l'application
    description = """
    Je veux construire une plateforme de blogging professionnelle avec:

    Articles:
    - Titre accrocheur
    - Contenu riche en markdown
    - Nom de l'auteur
    - Email de l'auteur
    - Date de publication
    - Catégorie (Tech, Science, Art, etc.)
    - Tags pour la recherche
    - Nombre de vues
    - Statut (brouillon, publié, archivé)

    Fonctionnalités:
    - Créer, modifier, supprimer des articles
    - Rechercher par titre ou catégorie
    - Filtrer par statut
    - Système de vues

    Technologies préférées:
    - Backend: FastAPI
    - Frontend: React
    - Base de données: SQLite pour commencer
    - Docker pour le déploiement
    - Tests complets
    """

    # 3. Générer l'application
    result = orchestrator.create_from_description(description)

    # 4. Vérifier les résultats
    print("\n📊 Résultats de la génération:")
    for component, status in result.items():
        print(f"  {component}: {'✅' if 'Error' not in str(status) else '❌'}")

    return result

if __name__ == "__main__":
    create_advanced_blog()
```

### Étendre une Application Existante

```python
from src.agents import OrchestratorAgent

orchestrator = OrchestratorAgent()

# Ajouter l'authentification JWT
orchestrator.extend_application(
    project_path="blog-platform",
    extension_type="auth"
)

# Ajouter une base de données
orchestrator.extend_application(
    project_path="blog-platform",
    extension_type="database",
    db_type="postgresql"
)

# Ajouter un routeur React
orchestrator.extend_application(
    project_path="blog-platform",
    extension_type="routing"
)

# Ajouter Nginx reverse proxy
orchestrator.extend_application(
    project_path="blog-platform",
    extension_type="nginx"
)
```

## API Reference

### OrchestratorAgent

#### `__init__(model_id=None, verbose=True)`

Initialise l'orchestrateur avec tous les agents spécialisés.

**Paramètres:**
- `model_id` (str, optional): ID du modèle HuggingFace. Default: config
- `verbose` (bool): Afficher les logs détaillés. Default: True

#### `create_from_description(description: str) -> Dict[str, str]`

**Mode Autonome**: Crée une application à partir d'une description en langage naturel.

**Paramètres:**
- `description` (str): Description textuelle de l'application

**Retourne:**
- Dict avec les résultats de chaque agent

**Exemple:**
```python
result = orchestrator.create_from_description(
    "Créer un système de réservation d'hôtel"
)
```

#### `create_fullstack_app(...) -> Dict[str, str]`

**Mode Manuel**: Crée une application avec des paramètres spécifiques.

**Paramètres:**
- `project_name` (str): Nom du projet
- `resource_name` (str): Nom de la ressource principale
- `fields` (List[Dict]): Liste des champs avec name et type
- `include_tests` (bool): Générer tests. Default: True
- `include_docker` (bool): Générer config Docker. Default: True
- `add_database` (bool): Ajouter base de données. Default: False

**Retourne:**
- Dict avec les résultats de chaque agent

#### `extend_application(project_path, extension_type, **kwargs) -> str`

Étend une application existante avec de nouvelles fonctionnalités.

**Types d'extensions:**
- `"auth"`: Ajouter authentification JWT
- `"database"`: Ajouter intégration base de données
- `"form"`: Ajouter formulaire React
- `"routing"`: Ajouter React Router
- `"nginx"`: Ajouter reverse proxy Nginx
- `"k8s"`: Générer configs Kubernetes
- `"coverage"`: Ajouter couverture de code

## Conseils et Bonnes Pratiques

### 1. Descriptions Efficaces

✅ **Bon:**
```python
description = """
Créer une application de recettes avec:
- Nom de la recette
- Ingrédients (liste)
- Instructions étape par étape
- Temps de préparation en minutes
- Niveau de difficulté (facile, moyen, difficile)
- Type de cuisine (italienne, mexicaine, chinoise)
"""
```

❌ **Moins bon:**
```python
description = "Je veux une app de recettes"
```

### 2. Spécifier les Types de Données

Le système est intelligent, mais être explicite aide:

```python
description = """
Chaque produit doit avoir:
- Prix (en euros, décimal)
- Quantité en stock (nombre entier)
- En promotion (oui/non)
- Date d'ajout (timestamp)
"""
```

### 3. Décrire les Fonctionnalités

Incluez ce que les utilisateurs peuvent faire:

```python
description = """
Les utilisateurs peuvent:
- Créer de nouveaux articles
- Modifier leurs propres articles
- Supprimer leurs articles
- Voir tous les articles publiés
- Rechercher par titre ou tag
- Filtrer par catégorie
"""
```

### 4. Préférences Techniques

Spécifiez si vous avez des préférences:

```python
description = """
Application de gestion de tâches.
Technologies: FastAPI backend, React frontend, PostgreSQL database.
Déploiement avec Docker et Kubernetes.
"""
```

## Dépannage

### Le système ne trouve pas les ressources

**Solution:** Soyez plus explicite sur les entités:
```python
description = """
L'application gère des **utilisateurs** et des **articles**.
Chaque utilisateur a un nom et email.
Chaque article a un titre et contenu.
"""
```

### Les types de champs sont incorrects

**Solution:** Spécifiez explicitement les types:
```python
description = """
Prix: nombre décimal
Quantité: nombre entier
Actif: oui/non
Date de création: date et heure
"""
```

### L'application générée ne correspond pas

**Solution:** Utilisez le mode manuel pour un contrôle précis:
```python
result = orchestrator.create_fullstack_app(
    project_name="my-app",
    resource_name="Item",
    fields=[...],
    # Paramètres précis
)
```

## Prochaines Étapes

Après génération:

1. **Naviguer vers outputs/**
   ```bash
   cd outputs/
   ```

2. **Lancer avec Docker**
   ```bash
   docker-compose up --build
   ```

3. **Accéder à l'application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - Docs API: http://localhost:8000/docs

4. **Lancer les tests**
   ```bash
   # Backend
   cd backend && pytest

   # Frontend
   cd frontend && npm test
   ```

Profitez de votre nouvelle application! 🎉
