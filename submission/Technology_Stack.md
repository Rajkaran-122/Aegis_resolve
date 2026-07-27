# Technology Stack

## Aegis Resolve AI — Digital Arbitration Court

| Field | Value |
|-------|-------|
| **Version** | MVP 0.1.0 |
| **Last Updated** | July 27, 2026 |

---

## 1. Stack Overview

```
┌────────────────────────────────────────────────────────────┐
│  FRONTEND          Next.js 16 · React 19 · TypeScript 5    │
│  STYLING           Tailwind CSS 4 · Custom dark theme      │
│  BACKEND           FastAPI 0.115 · Python 3.12 · Uvicorn   │
│  DATABASE          SQLite 3 (JSON document store)            │
│  CONTAINERS        Docker Compose · Node 22 · Python slim  │
│  REAL-TIME         WebSocket (FastAPI native)                │
└────────────────────────────────────────────────────────────┘
```

---

## 2. Frontend Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Framework** | Next.js | 16.2.12 | App Router, SSR/SSG, routing |
| **UI Library** | React | 19.2.4 | Component rendering |
| **Language** | TypeScript | 5.x | Type safety |
| **Styling** | Tailwind CSS | 4.x | Utility-first CSS |
| **Icons** | Lucide React | Latest | Consistent icon set |
| **UI Primitives** | Radix Slot | Latest | Accessible component base |
| **Class Utilities** | clsx, tailwind-merge, CVA | Latest | Conditional/dynamic classes |
| **Fonts** | IBM Plex Sans/Mono, Fraunces | Google Fonts | Enterprise typography |

### Installed (Future Use)

| Package | Planned Purpose |
|---------|-----------------|
| `@xyflow/react` | Interactive evidence trust graph visualization |
| `recharts` | Analytics charts in Control Center |
| `framer-motion` | Page transitions and micro-animations |
| `date-fns` | Date formatting for case timelines |

### Frontend Structure

```
frontend/
├── src/app/           # Next.js App Router pages
├── src/components/    # Shared UI (dispute-views.tsx)
├── src/lib/           # API client, utilities
├── package.json       # Dependencies
└── tsconfig.json      # TypeScript config
```

**Dev server:** `npm run dev` → `http://localhost:3000`

---

## 3. Backend Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Framework** | FastAPI | 0.115.6 | REST + WebSocket API |
| **Server** | Uvicorn | 0.34.0 | ASGI server |
| **Language** | Python | 3.12 | Application logic |
| **Validation** | Pydantic | 2.x | Request/response models |
| **Database Driver** | sqlite3 (stdlib) | Built-in | SQLite access |
| **API Docs** | OpenAPI (auto) | 3.x | Swagger UI at `/docs` |

### Backend Structure

```
backend/
├── main.py              # Monolithic API (models, DB, endpoints)
├── requirements.txt     # pip dependencies
├── Dockerfile           # Container image
├── aegis_resolve.db     # Runtime database
├── agents/              # (Planned) Agent services
├── core/                # (Planned) Business logic
├── data/                # (Planned) Data access
└── models/              # (Planned) Pydantic modules
```

**API server:** `uvicorn main:app --reload --port 8000` → `http://localhost:8000`

---

## 4. Database Stack

| Aspect | MVP | Production Target |
|--------|-----|-------------------|
| **Engine** | SQLite 3 | PostgreSQL 16+ |
| **Schema** | Single table, JSON blob | Normalized relational + JSONB |
| **Pattern** | Document store | Hybrid relational + event sourcing |
| **Migrations** | None (seed on boot) | Alembic / Flyway |
| **Backup** | File copy | Automated PITR |

### MVP Schema

```sql
CREATE TABLE disputes (
    id TEXT PRIMARY KEY,
    payload TEXT NOT NULL
);
```

Each `payload` is a serialized `Dispute` JSON document containing nested evidence, verdict, and events.

---

## 5. Infrastructure & DevOps

| Category | Technology | Purpose |
|----------|------------|---------|
| **Containerization** | Docker | Backend + frontend images |
| **Orchestration** | Docker Compose | Local multi-service startup |
| **Backend Image** | `python:3.12-slim` | Minimal Python runtime |
| **Frontend Image** | `node:22` | Node.js build + serve |
| **Environment** | `.env` file | API URL, environment flag |

### Docker Compose Services

```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000/v1
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000/v1` | Frontend API base URL |
| `AEGIS_ENV` | `development` | Environment identifier |

---

## 6. API & Communication

| Protocol | Usage | Format |
|----------|-------|--------|
| **REST** | CRUD, process, override, analytics | JSON over HTTP |
| **WebSocket** | Real-time replay streaming | JSON messages |
| **OpenAPI** | Auto-generated API documentation | Swagger UI |

### CORS Configuration

```python
allow_origins=["http://localhost:3000"]
allow_methods=["*"]
allow_headers=["*"]
```

---

## 7. AI / Agent Stack

| Component | MVP Status | Production Target |
|-----------|------------|---------------------|
| **Agent Orchestration** | Simulated (replay events) | LangGraph |
| **LLM Provider** | None | Approved enterprise provider |
| **Policy Engine** | Deterministic Python dict | LLM + rule-based hybrid |
| **Document Intelligence** | Pre-seeded evidence | OCR + NLP pipeline |
| **Advocacy Agents** | Narrative only | Dual LLM advocates |
| **Fairness Engine** | Fixed scores | ML fairness model |

---

## 8. Development Tools

| Tool | Purpose |
|------|---------|
| **npm** | Frontend package management |
| **pip** | Backend dependency management |
| **TypeScript Compiler** | Frontend type checking |
| **Python compileall** | Backend syntax validation |
| **FastAPI /docs** | Interactive API testing |
| **Git** | Version control (recommended) |

### Quality Checks

```powershell
# Backend
cd backend && python -m compileall .

# Frontend
cd frontend && npm run build
```

---

## 9. Design System

| Element | Value |
|---------|-------|
| **Primary Background** | `#06182c` (dark navy) |
| **Accent Color** | `#00a6e8` (cyan) |
| **Heading Font** | Fraunces (serif) |
| **Body Font** | IBM Plex Sans |
| **Mono Font** | IBM Plex Mono |
| **Panel Style** | Glass morphism with backdrop blur |
| **Status Colors** | Emerald (resolved), Cyan (review/open) |

---

## 10. Technology Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| **Next.js over CRA** | App Router, built-in routing, production-ready SSR |
| **FastAPI over Flask** | Auto OpenAPI docs, Pydantic validation, WebSocket support |
| **SQLite over PostgreSQL** | Zero-config demo; no external DB required |
| **Monolith over microservices** | Faster MVP; empty folders preserve future boundaries |
| **JSON document store** | Flexible schema for nested evidence/verdict/events |
| **Deterministic policy engine** | Reliable demo outcomes without LLM API keys |
| **Tailwind CSS 4** | Rapid UI development with consistent design tokens |

---

## 11. Production Technology Roadmap

| Layer | Current | Target |
|-------|---------|--------|
| Database | SQLite | PostgreSQL + Redis cache |
| Auth | None | OAuth2/OIDC (Auth0, Okta) |
| Agents | Simulated | LangGraph + approved LLM |
| File Storage | None | AWS S3 / Azure Blob |
| Message Queue | None | Kafka / AWS SQS |
| Monitoring | None | Datadog / Prometheus |
| CI/CD | None | GitHub Actions |
| Hosting | Local/Docker | Kubernetes / AWS ECS |

---

*End of Technology Stack Document*
