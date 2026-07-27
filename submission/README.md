# Aegis Resolve AI — Submission Package

**Digital Arbitration Court for Explainable Payment Dispute Resolution**

| Field | Value |
|-------|-------|
| **Project** | Aegis Resolve AI |
| **Version** | MVP 0.1.0 |
| **Submission Date** | July 27, 2026 |
| **Author** | Dictatordaddy |

---

## Package Contents

```
submission/
├── BRD.pdf                    # Business Requirements Document
├── PRD.md                     # Product Requirements Document
├── Architecture.md            # Architecture overview
├── System_Architecture.md     # System architecture with diagrams
├── Technology_Stack.md        # Complete technology stack
├── README.md                  # This file — package index
├── Demo_Video.mp4             # Product demonstration video
├── UI_Screenshots/            # Application screenshots
├── Prototype_Link.txt         # Live prototype URL
├── GitHub_Link.txt            # Source code repository
└── Additional_Diagrams.md     # Supplementary architecture diagrams
```

---

## Executive Summary

Aegis Resolve AI is an explainable dispute-resolution platform that models payment and card disputes as a **Digital Arbitration Court**. The MVP demonstrates:

- **Three stakeholder portals** — Card member, merchant, and enterprise control center
- **Evidence Trust Graph** — Trust-scored evidence with confirms/contradicts/supplements relations
- **Policy-driven verdicts** — AMEX-inspired reason codes with confidence and fairness scoring
- **Courtroom Replay** — Full audit trail of agent decision pipeline
- **Human review routing** — Edge cases escalated to analyst override

---

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+ (22 recommended)
- npm

### Run Locally

**Terminal 1 — Backend API:**

```powershell
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**

```powershell
cd frontend
npm install
npm run dev
```

**Or with Docker:**

```powershell
docker-compose up
```

### Access Points

| Service | URL |
|---------|-----|
| Web Application | http://localhost:3000 |
| API Documentation | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

## Demo Walkthrough

Follow this path for the best submission demo:

1. **Landing Page** — Visit `/` to see the hero, product pillars, and live case preview
2. **Control Center** — Open `/admin` and select **AR-2026-002** from the human-review queue
3. **Case Inspection** — Review evidence, AMEX 4553 policy, confidence (61%), fairness (91%), and courtroom replay
4. **Multi-Portal View** — Open `/customer/disputes/AR-2026-002` and `/merchant/cases/AR-2026-002` to show one shared case from both sides
5. **API Demo** — Use Swagger at `/docs` to submit evidence, process a dispute, or record an analyst override

### Seeded Demo Cases

| Case ID | Scenario | Status | Outcome |
|---------|----------|--------|---------|
| AR-2026-001 | Alpine camera never arrived | Resolved | Merchant |
| AR-2026-002 | Aurora headphones differ from listing | Human Review | Human Review |
| AR-2026-003 | Duplicate ride-share charge | Resolved | Card Member |
| AR-2026-004 | Subscription charged after cancellation | Human Review | Human Review |
| AR-2026-005 | Unrecognized electronics transaction | Resolved | Card Member |

---

## Architecture at a Glance

```
Frontend (Next.js 16)  ──REST/WS──▶  Backend (FastAPI)  ──▶  SQLite
     │                                      │
     ├── /customer (Card Member)            ├── Policy Engine
     ├── /merchant (Merchant)               ├── Evidence Graph
     └── /admin (Control Center)            └── Courtroom Replay
```

See `Architecture.md` and `System_Architecture.md` for full details.

---

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| Backend | FastAPI, Python 3.12, Uvicorn, Pydantic |
| Database | SQLite (JSON document store) |
| Real-time | WebSocket (FastAPI native) |
| Containers | Docker Compose |

See `Technology_Stack.md` for the complete breakdown.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/disputes` | List all disputes |
| POST | `/v1/disputes` | Create dispute |
| GET | `/v1/disputes/{id}` | Get dispute |
| POST | `/v1/disputes/{id}/evidence` | Add evidence |
| POST | `/v1/disputes/{id}/process` | Run policy engine |
| GET | `/v1/disputes/{id}/verdict` | Get verdict |
| GET | `/v1/disputes/{id}/evidence-graph` | Evidence graph data |
| GET | `/v1/disputes/{id}/replay` | Courtroom replay |
| POST | `/v1/disputes/{id}/override` | Analyst override |
| GET | `/v1/analytics/control-center` | KPI metrics |
| GET | `/v1/analytics/fairness` | Fairness distribution |
| WS | `/v1/disputes/{id}/stream` | Real-time replay stream |

---

## Quality Checks

```powershell
# Backend syntax validation
cd backend && python -m compileall .

# Frontend production build
cd frontend && npm run build
```

---

## Production Roadmap

| Phase | Deliverable |
|-------|-------------|
| MVP 0.1.0 | Demo submission (current) |
| v0.2.0 | Wire remaining UI to API, live graph visualization |
| v0.3.0 | Authentication, PostgreSQL, immutable audit store |
| v1.0.0 | LangGraph agents, production deployment |

---

## Document Index

| Document | Description |
|----------|-------------|
| [BRD.pdf](./BRD.pdf) | Business requirements, stakeholders, success metrics |
| [PRD.md](./PRD.md) | Product requirements, user stories, functional specs |
| [Architecture.md](./Architecture.md) | Component architecture, data model, API design |
| [System_Architecture.md](./System_Architecture.md) | System context, data flows, security, scalability |
| [Technology_Stack.md](./Technology_Stack.md) | Complete technology choices and rationale |
| [Additional_Diagrams.md](./Additional_Diagrams.md) | State machines, agent pipeline, deployment topology |

---

## License

This project is submitted as an MVP demonstration. All rights reserved.

---

*Aegis Resolve AI — Disputes resolved with clarity.*
