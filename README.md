# 🐾 Reactive Dog Tracker 🐾

Application de suivi des chiens réactifs, permettant de centraliser les déclencheurs, réactions, observations et progressions comportementales, à des fins d’analyse et de visualisation.

---

## Objectifs

### V1 – Projet local démontrant mes compétences :
- Backend API REST avec **FastAPI**
- Frontend web simple avec **Streamlit**
- Base de données **SQLite**
- Visualisation des données avec **Matplotlib / Plotly**
- Dashboard Power BI intégré (lien dans l'application)
- Authentification simplifiée (JWT)
- Tests unitaires avec **Pytest**
- CI/CD avec **GitHub Actions**
- Dockerisation complète via **Docker Compose**
- OWASP pour l'application des bonnes pratiques de sécurisation
- Bonus : Intégration Elasticsearch pour montrer mes compétences en recherche full-text

### V2 – Extension cloud native (non déployée mais préparée)
- Infrastructure as Code avec **Terraform** dans `/infra`
- Orchestration avec **K3s** (Kubernetes léger)
- Secrets Management avec **Vault**
- Base de données Cloud (Oracle Autonomous Database)
- Déploiement dans un environnement cloud (Oracle)
- Monitoring avec Prometheus et Grafana

---

## Arborescence du projet

```bash
├── app/                  # Backend FastAPI
├── streamlit_app/        # Frontend Streamlit
├── infra/                # Infra as Code
├── tests/                # Tests unitaires
├── data/                 # Fichiers de données (SQLite)
├── sql/                  # Fichiers de données MySQL
├── .github/workflows/    # CI/CD GitHub Actions
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.streamlit
├── README.md
├── main.py               # Point d'entrée de l'API FastAPI
├── requirements.txt      # Dépendances Python de l'application
├── Cahier des charges.md
├── .gitignore
```

## Fichiers importants

- main.py : point d’entrée de l’API FastAPI. Il initialise l’application, crée la base de données via SQLAlchemy et monte les routes principales (users, triggers, reactions, entries).
- requirements.txt : contient toutes les dépendances nécessaires à l’exécution de l’application (FastAPI, SQLAlchemy, Streamlit, Plotly, etc.).

---

## Lancement local (V1)

```bash
# Lancer l'application complète
docker-compose up --build
```

## Dashboard Power BI

L'application propose un lien vers un tableau de bord Power BI interactif permettant de suivre :
- La fréquence des déclencheurs
- L’évolution des réactions
- Des statistiques comportementales dans le temps

## Tests

```bash
pytest tests/
```

## Technologies utilisées

| **Type**          | **Stack**                                                |
|-------------------|----------------------------------------------------------|
| **Backend**       | FastAPI, Pydantic, Pandas, SQLite                        |
| **Frontend**      | Streamlit, Matplotlib / Plotly                           |
| **BI**            | Power BI                                                 |
| **Tests**         | Pytest                                                   |
| **DevOps**        | Docker, GitHub Actions                                   |
| **Observabilité** | Elasticsearch (optionnel)                                |
| **Cloud readiness**| Terraform, Vault, Oracle, K3s, Prometheus, Grafana (V2) |

---

## Expansion (V2 – cloud ready)

Voir /infra/README.md pour le diagramme de l’architecture cible et les premiers fichiers Terraform.
