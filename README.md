# SafeTrack WA — Mine Safety Incident Migration Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-Containerised-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![License](https://img.shields.io/badge/Licence-CC--BY--4.0-green)

## Overview

SafeTrack WA is an end-to-end data migration and analytics platform simulating a real-world enterprise scenario: transforming legacy mine safety records from multiple Western Australian operations into a modern, structured, and scalable system.

The project covers the complete pipeline — from raw data ingestion and ETL processing, through relational schema design and REST API development, to containerised deployment and Power BI analytics.

---

## Problem Statement

Mining operations across Western Australia generate vast volumes of safety data every day — incident reports, near-miss logs, inspection findings, and corrective action records. In many operations, this data remains locked in disconnected spreadsheets and legacy systems that cannot communicate with each other.

This fragmentation creates serious operational and regulatory risk:

- Safety managers cannot calculate TRIFR (Total Recordable Injury Frequency Rate) in real time
- Near-miss data sits in shift supervisor notebooks and never reaches decision makers
- Corrective actions from inspections go untracked, leaving compliance gaps
- Site managers have no cross-site visibility into hazard patterns

SafeTrack WA addresses this by migrating legacy safety data into a normalised PostgreSQL schema, exposing KPIs via a Flask REST API, and delivering real-time insights through a Power BI dashboard.

---

## System Architecture
```text
Raw Data (CSV)
        │
        ▼
Python / Pandas (ETL & Data Generation)
        │
        ▼
PostgreSQL (Normalised Relational Schema)
        │
        ▼
Flask API (REST Endpoints)
        │
        ▼
Docker / Kubernetes (Containerisation & Orchestration)
        │
        ▼
Power BI (Analytics Dashboard)
```
---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Data Processing | Pandas, NumPy, Faker |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy |
| Backend API | Flask 3.1 |
| Containerisation | Docker, Docker Compose |
| Orchestration | Kubernetes |
| Visualisation | Power BI |

---

## Data Sources

- **Mine site data:** WA Mining Tenements (DMIRS-003) — [data.wa.gov.au](https://catalogue.data.wa.gov.au/dataset/mining-tenements-dmirs-003) — Licensed under Creative Commons Attribution 4.0
- **Safety data:** Synthetically generated using Python Faker, calibrated against publicly available WA DMIRS safety statistics from WorkSafe WA annual reports

---

## Data Pipeline

### Step 1 — Extract
Raw mining tenement data downloaded from the WA Government open data portal (DMIRS-003).
30,375 tenement records loaded into pandas with latin-1 encoding.

### Step 2 — Transform
- Filtered to 6,066 active Mining Leases
- Commodity inferred from operator name (Gold, Iron Ore, Nickel, Lithium)
- WA region inferred from operator name (Pilbara, Goldfields, Midwest, Kimberley)
- Aggregated to 20 distinct mine site operators
- Synthetic safety data generated using Python Faker calibrated to WA DMIRS statistics

### Step 3 — Load
- 6 normalised tables loaded into PostgreSQL via SQLAlchemy
- 8,172 total rows across all tables
- Foreign key relationships enforced at database level

---

## Data Model

| Table | Rows | Description |
|---|---|---|
| `sites` | 20 | WA mine site operators filtered from DMIRS tenement data |
| `workers` | 3,616 | Synthetic workforce records per site |
| `incidents` | 567 | Safety incidents (LTI, MTI, FAI, Fatality) |
| `near_miss` | 1,518 | Near-miss reports by hazard category and shift |
| `inspections` | 296 | Regulatory inspection records with pass/fail scores |
| `compliance_actions` | 2,175 | Corrective actions from inspections with RAG status |

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Health check |
| `GET /summary` | Row counts across all tables |
| `GET /incidents/by-type` | Incident breakdown by type |
| `GET /incidents/by-site` | Incident count per site |
| `GET /incidents/trifr` | TRIFR calculation per operator |
| `GET /nearmiss/trend` | Near-miss counts by month |
| `GET /inspections/compliance-rate` | Pass rate and average score per site |
| `GET /compliance/overdue` | List of overdue corrective actions |

---

## API Demo

Health check:
```json
GET http://localhost:5000
{"project": "SafeTrack WA", "status": "ok"}
```

Database summary:
```json
GET http://localhost:5000/summary
{
  "compliance_actions": 2175,
  "incidents": 567,
  "inspections": 296,
  "near_miss": 1518,
  "sites": 20,
  "workers": 3616
}
```

---

## Power BI Dashboard

Five dashboard pages:

| Page | Description |
|---|---|
| Executive Overview | TRIFR gauge, total incidents, near-miss count, compliance score |
| Incident Analysis | Breakdown by type, monthly trend, site vs severity |
| Near-Miss Analysis | By WA region, hazard category, shift, and location |
| Compliance Tracker | Inspection pass rate, overdue actions, findings trend |
| Site Deep-Dive | Single-site slicer filtering all visuals |

---

## Project Structure
```text
safetrack-wa/
├── data/
│   ├── raw/                          # Source data (not committed)
│   └── processed/                    # Cleaned and generated CSVs
│
├── notebooks/
│   ├── 01_eda.ipynb                  # Exploratory data analysis
│   └── 02_data_generation.ipynb      # Synthetic data generation
│
├── app/
│   ├── __init__.py
│   ├── models.py                     # SQLAlchemy models
│   └── routes/
│       ├── incidents.py
│       └── safety.py
│
├── kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
│
├── dashboard/
│   └── SafeTrackWA.pbix              # Power BI dashboard
│
├── app.py                            # Flask application entry point
├── load_data.py                      # Loads processed data into PostgreSQL
├── Dockerfile                        # Docker image configuration
├── docker-compose.yml                # Local multi-container setup
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## Getting Started

### Prerequisites
- Docker Desktop
- Python 3.11
- Power BI Desktop

### Run with Docker

```bash
git clone https://github.com/areeshamajid/safetrack-wa.git
cd safetrack-wa
docker-compose up --build
```

### Load data into PostgreSQL

```bash
docker exec safetrack_app python load_data.py
```

### Access the API
http://localhost:5000
http://localhost:5000/summary
http://localhost:5000/incidents/by-type

### Download raw data

Download `CurrentTenements_GDA2020_csv.zip` from:
[catalogue.data.wa.gov.au/dataset/mining-tenements-dmirs-003](https://catalogue.data.wa.gov.au/dataset/mining-tenements-dmirs-003)

Extract and place `CurrentTenements.csv` in `data/raw/`.

---

## Key Learnings

- Designing normalised relational schemas with foreign key constraints
- Building ETL pipelines with Pandas for real government datasets
- Developing REST APIs with Flask and SQLAlchemy
- Understanding container networking with Docker Compose
- Deploying applications with Kubernetes
- Building operational analytics dashboards in Power BI
- Working with WA mining industry data and DMIRS safety taxonomy

---

## Author

**Areesha Majid**

- GitHub: [github.com/areeshamajid](https://github.com/areeshamajid)

---

## Licence

Site data sourced from WA Government under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/).
