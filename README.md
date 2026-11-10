# SupportFlow AI — Plateforme intelligente d'automatisation du support client

## Présentation de l'application

**SupportFlow AI** est une application web intelligente conçue pour automatiser et optimiser la gestion des demandes de support client grâce à l'intelligence artificielle et à l'intégration des systèmes d'information.

La plateforme permet aux entreprises de centraliser les demandes provenant de différents canaux, notamment les emails, d'analyser automatiquement leur contenu, de les classifier selon leur nature et leur priorité, puis de générer des propositions de réponses pertinentes à partir d'une base de connaissances.

Grâce à l'intégration avec des outils professionnels tels que **Gmail, Notion et HubSpot**, SupportFlow AI facilite la circulation des informations entre les différentes applications utilisées par l'entreprise.

L'objectif est de **réduire les tâches répétitives, accélérer le traitement des demandes, améliorer la qualité des réponses et permettre aux équipes de support de se concentrer sur les situations complexes.**

## Fonctionnalités principales

1. **Centralisation des demandes :** récupération automatique des emails clients et transformation en tickets de support.

2. **Classification intelligente :** analyse des demandes par intelligence artificielle afin d'identifier leur catégorie, leur niveau de priorité et leur degré d'urgence.

3. **Assistant basé sur une base de connaissances (RAG) :** recherche des informations pertinentes dans les documents, procédures et FAQ de l'entreprise afin de produire des réponses contextualisées et appuyées sur des sources.

4. **Génération automatique de réponses :** proposition de réponses personnalisées aux demandes clients, avec validation humaine avant tout envoi.

5. **Gestion des tickets :** création, consultation, affectation, suivi et mise à jour des tickets via une interface centralisée.

6. **Escalade intelligente :** identification des demandes complexes, sensibles ou nécessitant une intervention humaine.

7. **Intégration des applications métiers :** connexion aux outils de messagerie, CRM et plateformes documentaires à travers leurs API.

8. **Tableau de bord et suivi des performances :** visualisation des demandes, des priorités, des délais de traitement et des indicateurs de performance du support.

## Architecture technique

L'application repose sur une architecture moderne et modulaire :

- **Frontend :** Next.js, React, TypeScript et Tailwind CSS.
- **Backend :** Python et FastAPI.
- **Base de données :** PostgreSQL.
- **Intelligence artificielle :** API de modèles de langage (LLM).
- **Recherche documentaire :** RAG (Retrieval-Augmented Generation).
- **Intégrations :** Gmail API, Notion API et HubSpot API.
- **Sécurité :** authentification, gestion des rôles, protection des API, journalisation et validation humaine des actions sensibles.

## Public cible

SupportFlow AI s'adresse principalement aux startups SaaS, aux entreprises de commerce électronique, aux agences de services numériques et aux PME souhaitant moderniser leur service client.

## Valeur ajoutée

SupportFlow AI ne se limite pas à un simple chatbot conversationnel. Il constitue une **solution métier intégrée** combinant intelligence artificielle, automatisation des processus, gestion des tickets et interconnexion des applications.

La plateforme vise à améliorer la productivité des équipes, réduire les interventions manuelles et offrir une meilleure expérience aux clients, tout en maintenant un contrôle humain sur les décisions importantes.

## État du projet

**Projet en cours de développement — MVP.**

La première version vise à mettre en place la gestion des tickets, leur classification automatique, la génération de réponses assistée par IA et l'intégration progressive de Gmail et Notion. Les fonctionnalités avancées seront ajoutées et validées au cours des prochaines phases.

## Structure initiale du backend

Le backend actuel fournit la création et la consultation des tickets avec PostgreSQL. Les fonctionnalités IA et les intégrations décrites ci-dessus constituent la cible du produit.

```text
SupportFlowAI/
├── app/
│   ├── main.py              # Application FastAPI
│   ├── api/                 # Routes HTTP : tickets et santé
│   ├── core/config.py       # Configuration depuis les variables d'environnement
│   ├── db/                  # Base SQLAlchemy et sessions PostgreSQL
│   ├── models/              # Modèles de tables
│   ├── schemas/             # Validation et réponses Pydantic
│   └── repositories/        # Accès aux données
├── migrations/             # Migrations Alembic versionnées
├── tests/                  # Tests API et intégration PostgreSQL
├── main.py                 # Point d'entrée compatible avec main:app
├── alembic.ini
├── compose.yaml            # PostgreSQL local avec volume persistant
├── .env.example            # Exemple de configuration
├── requirements.txt
├── requirements-dev.txt
└── test_main.http
```

### Installation locale (PowerShell)

Prérequis : Python 3.10 ou supérieur et PostgreSQL, ou Docker Desktop pour démarrer PostgreSQL avec Compose.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Si `.env` existe déjà, le conserver et adapter ses valeurs. Ce fichier est ignoré par Git.

### Connexion à PostgreSQL

Pour démarrer une nouvelle base locale avec Docker Desktop :

```powershell
docker compose up -d --wait db
```

`POSTGRES_IMAGE` permet de choisir l'image PostgreSQL. L'exemple utilise `postgres:17` ; la configuration locale peut sélectionner une version déjà disponible sur votre machine.

Pour utiliser un serveur PostgreSQL existant, créer une base et un utilisateur autorisé à y créer des tables, puis modifier `DATABASE_URL` dans `.env` :

```dotenv
DATABASE_URL=postgresql+psycopg://UTILISATEUR:MOT_DE_PASSE@localhost:5432/NOM_BASE
```

Encoder les caractères spéciaux du nom d'utilisateur et du mot de passe dans l'URL. Les identifiants fournis dans `.env.example` sont uniquement destinés au développement local. Pour Docker, garder les valeurs `POSTGRES_*` et `DATABASE_URL` cohérentes ; si le port change, modifier aussi le port dans l'URL. Les variables `POSTGRES_*` initialisent uniquement un volume neuf.

Appliquer les migrations avant de lancer l'API :

```powershell
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

Documentation interactive : <http://127.0.0.1:8000/docs>.

| Méthode | Route | Description |
| --- | --- | --- |
| GET | `/health` | État de l'API |
| GET | `/health/db` | Connexion PostgreSQL : 200 si disponible, 503 sinon |
| POST | `/tickets` | Création d'un ticket avec titre et description |
| GET | `/tickets` | Liste des tickets |
| GET | `/tickets/{ticket_id}` | Consultation d'un ticket par UUID |

Les tickets sont conservés dans PostgreSQL après le redémarrage de l'API. Le serveur ne crée pas automatiquement les tables : leur évolution passe par Alembic.

### Tests et évolution du schéma

```powershell
python -m pytest -q
```

Pour exécuter aussi le test d'intégration, utiliser une base PostgreSQL dédiée aux tests et appliquer les migrations dessus :

```powershell
$env:DATABASE_URL = "postgresql+psycopg://UTILISATEUR:MOT_DE_PASSE@localhost:5432/supportflow_test"
python -m alembic upgrade head
$env:TEST_DATABASE_URL = $env:DATABASE_URL
python -m pytest -q
Remove-Item Env:TEST_DATABASE_URL
Remove-Item Env:DATABASE_URL
```

Le test d'intégration annule ses écritures après son exécution. Sans `TEST_DATABASE_URL`, il est ignoré.

Après une modification des modèles, générer une migration, vérifier son contenu, puis l'appliquer :

```powershell
python -m alembic revision --autogenerate -m "description du changement"
python -m alembic upgrade head
```

Références : [PostgreSQL avec SQLAlchemy et psycopg](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg), [sessions avec les dépendances FastAPI](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).
