# 🐾 Reactive Dog Tracker 🐾

Application de suivi des chiens réactifs, permettant de centraliser les déclencheurs, réactions, observations et progressions comportementales, à des fins d’analyse et de visualisation.

---

## Objectifs

### V1 – Projet local :
- Backend API REST avec **FastAPI**
- Frontend web simple avec **Streamlit**
- Base de données **SQLite**
- Visualisation des données avec **Matplotlib / Plotly**
- Authentification simplifiée (JWT)
- Tests unitaires avec **Pytest**
- Conteneurisation du backend et frontend avec **Docker**
- OWASP ZAP et Trivy pour l'application des bonnes pratiques de sécurisation

### V2 – Extension cloud native (non déployée mais préparée)
- Infrastructure as Code avec **Terraform** dans `/infra`
- Orchestration avec **K3s** (Kubernetes léger)
- Secrets Management avec **Vault**
- CI/CD avec **GitHub Actions**
- Dockerisation complète via **Docker Compose**
- Base de données Cloud (Oracle Autonomous Database)
- Déploiement dans un environnement cloud (Oracle) ou Cloud privé avec Raspberry Pi
- Monitoring avec Prometheus et Grafana
- Intégration ElasticSearch et Kibana

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
├── README.md
├── Cahier des charges.md
├── .gitignore
```
---

## Lancement local (V1)

```bash
# Lancer l'application complète
docker-compose up --build
```

## Technologies utilisées

| **Type**          | **Stack**                                                |
|-------------------|----------------------------------------------------------|
| **Backend**       | FastAPI, Pydantic, Pandas, SQLite                        |
| **Frontend**      | Streamlit, Matplotlib / Plotly                           |
| **Tests**         | Pytest                                                   |
| **DevOps**        | Docker, GitHub Actions                                   |
| **Observabilité** | Elasticsearch, Kibana (v2)                                |
| **Cloud readiness**| Terraform, Vault, Oracle, K3s, Prometheus, Grafana (v2) |

---

## Expansion (V2 – cloud ready)

Voir /infra/README.md pour le diagramme de l’architecture cible et les premiers fichiers Terraform.
