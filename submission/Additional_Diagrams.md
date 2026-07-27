# Additional Diagrams

## Aegis Resolve AI — Digital Arbitration Court

Supplementary architecture and flow diagrams for submission review.

---

## 1. High-Level System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AEGIS RESOLVE AI                                │
│                    Digital Arbitration Court                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                  │
│   │   CARD      │   │  MERCHANT   │   │ ENTERPRISE  │                  │
│   │   MEMBER    │   │   PORTAL    │   │   CONTROL   │                  │
│   │   PORTAL    │   │             │   │   CENTER    │                  │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                  │
│          │                 │                 │                          │
│          └─────────────────┼─────────────────┘                          │
│                            │                                            │
│                   ┌────────▼────────┐                                   │
│                   │   Next.js 16    │                                   │
│                   │   Frontend      │                                   │
│                   │   (Port 3000)   │                                   │
│                   └────────┬────────┘                                   │
│                            │ REST + WebSocket                           │
│                   ┌────────▼────────┐                                   │
│                   │   FastAPI       │                                   │
│                   │   Backend       │                                   │
│                   │   (Port 8000)   │                                   │
│                   └────────┬────────┘                                   │
│                            │                                            │
│              ┌─────────────┼─────────────┐                              │
│              │             │             │                              │
│     ┌────────▼───┐  ┌─────▼─────┐  ┌───▼──────────┐                   │
│     │  Policy    │  │  SQLite   │  │  WebSocket   │                   │
│     │  Engine    │  │  Database │  │  Stream      │                   │
│     └────────────┘  └───────────┘  └──────────────┘                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Dispute Lifecycle State Machine

```
                    ┌──────────┐
                    │   OPEN   │
                    └────┬─────┘
                         │ Evidence submitted
                         ▼
                 ┌───────────────┐
                 │  PROCESSING   │
                 └───────┬───────┘
                         │ Policy engine runs
                         │
            ┌────────────┼────────────┐
            │                         │
            ▼                         ▼
    ┌───────────────┐         ┌──────────────┐
    │   RESOLVED    │         │ HUMAN REVIEW │
    │ (card_member  │         │              │
    │  or merchant) │         └──────┬───────┘
    └───────────────┘                │
                                     │ Analyst override
                                     ▼
                              ┌──────────────┐
                              │   RESOLVED   │
                              └──────────────┘
```

---

## 3. Agent Pipeline (Target Architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                     AGENT ORCHESTRATION                          │
│                                                                  │
│  ┌──────────────┐                                               │
│  │ Orchestrator │ ─── Case intake, SLA timer, routing           │
│  └──────┬───────┘                                               │
│         │                                                        │
│  ┌──────▼───────────────┐                                       │
│  │ Evidence Collection  │ ─── Gather receipts, shipments, msgs  │
│  │ Agent                │                                       │
│  └──────┬───────────────┘                                       │
│         │                                                        │
│  ┌──────▼───────────────┐                                       │
│  │ Document Intelligence│ ─── OCR, NLP, fact extraction         │
│  │ Agent                │                                       │
│  └──────┬───────────────┘                                       │
│         │                                                        │
│  ┌──────┴───────────────┐                                       │
│  │                      │                                       │
│  ▼                      ▼                                       │
│ ┌────────────┐   ┌────────────┐                                 │
│ │ Customer   │   │ Merchant   │ ─── Dual advocacy               │
│ │ Advocate   │   │ Advocate   │                                 │
│ └─────┬──────┘   └─────┬──────┘                                 │
│       └────────┬───────┘                                        │
│                │                                                 │
│  ┌─────────────▼────────────┐                                   │
│  │ Policy & Compliance Agent│ ─── AMEX code application         │
│  └─────────────┬────────────┘                                   │
│                │                                                 │
│  ┌─────────────▼────────────┐                                   │
│  │ Financial Risk & Fairness│ ─── Confidence + fairness scoring │
│  │ Engine                   │                                   │
│  └─────────────┬────────────┘                                   │
│                │                                                 │
│  ┌─────────────▼────────────┐                                   │
│  │ Neutral Judge Agent      │ ─── Final verdict                 │
│  └─────────────┬────────────┘                                   │
│                │                                                 │
│  ┌─────────────▼────────────┐                                   │
│  │ Explainability & Audit   │ ─── Rationale + immutable log     │
│  │ Agents                   │                                   │
│  └──────────────────────────┘                                   │
│                                                                  │
│  ┌──────────────────────────┐                                   │
│  │ Operations Analyst       │ ─── Human override (edge cases)   │
│  └──────────────────────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Evidence Trust Graph — Example (AR-2026-002)

```
                         ┌─────────────────────┐
                         │  Aurora Headphones  │
                         │  Case (trust: 100)  │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │ Order Invoice   │  │ Product Photos  │  │ Merchant Reply  │
    │ trust: 94       │  │ trust: 70       │  │ trust: 72       │
    │ confirms        │  │ contradicts     │  │ supplements     │
    └─────────────────┘  └─────────────────┘  └─────────────────┘

    Verdict: HUMAN REVIEW
    Confidence: 61%  |  Fairness: 91/100
    Policy: AMEX 4553 — Not as Described
```

---

## 5. API Endpoint Map

```
/v1/
├── disputes
│   ├── GET     /                    → List all disputes
│   ├── POST    /                    → Create dispute
│   └── {id}
│       ├── GET     /                → Get dispute
│       ├── POST    /evidence        → Add evidence
│       ├── POST    /process         → Run policy engine
│       ├── GET     /verdict         → Get verdict
│       ├── GET     /evidence-graph  → Graph nodes/edges
│       ├── GET     /replay          → Courtroom replay
│       ├── POST    /override        → Analyst override
│       └── WS      /stream          → Real-time replay
│
└── analytics
    ├── GET /control-center          → KPI metrics
    └── GET /fairness                → Fairness distribution

/health                                → Service health check
/docs                                  → Swagger UI
```

---

## 6. Three-Portal User Journey

```
CARD MEMBER JOURNEY                    MERCHANT JOURNEY
─────────────────────                  ────────────────
1. Visit /customer                     1. Visit /merchant
2. View active cases                   2. View incoming cases
3. Open case detail                    3. Open case response
4. See verdict + evidence              4. Review evidence + verdict
5. File new dispute (/file-dispute)    5. Submit supporting evidence

                    ANALYST JOURNEY
                    ───────────────
                    1. Visit /admin (Control Center)
                    2. Review human-review queue
                    3. Open courtroom dossier
                    4. Inspect replay timeline
                    5. Record analyst override
                    6. Monitor KPI metrics
```

---

## 7. Data Model Entity Relationship

```
┌─────────────────────────────────────────────────────────┐
│                        DISPUTE                           │
├─────────────────────────────────────────────────────────┤
│ id (PK)          │ title           │ amount            │
│ card_member      │ merchant        │ currency          │
│ reason_code      │ reason          │ status            │
│ created_at       │ deadline        │                   │
├─────────────────────────────────────────────────────────┤
│                    1 ────── * EVIDENCE                   │
│  ┌─────────────────────────────────────────────────┐    │
│  │ id │ type │ title │ source │ trust │ relation  │    │
│  │ detail                                          │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                    1 ────── 0..1 VERDICT                 │
│  ┌─────────────────────────────────────────────────┐    │
│  │ outcome │ confidence │ fairness │ headline      │    │
│  │ explanation │ policy_code │ policy_title        │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                    1 ────── * REPLAY EVENT               │
│  ┌─────────────────────────────────────────────────┐    │
│  │ time │ title │ agent │ detail                    │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Deployment Topology

### Local Development

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Browser    │────▶│  Next.js     │────▶│  FastAPI     │
│  :3000       │     │  Dev Server  │     │  :8000       │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                           ┌──────▼───────┐
                                           │  SQLite DB   │
                                           │  (local file)│
                                           └──────────────┘
```

### Docker Compose

```
┌─────────────────────────────────────────────────────────┐
│                    docker-compose.yml                    │
│  ┌─────────────────┐       ┌─────────────────┐          │
│  │ frontend:3000   │──────▶│ backend:8000    │          │
│  │ (node:22)       │       │ (python:3.12)   │          │
│  └─────────────────┘       └────────┬────────┘          │
│                                     │                    │
│                              ┌──────▼──────┐             │
│                              │ aegis.db    │             │
│                              │ (volume)    │             │
│                              └─────────────┘             │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Production Target Architecture

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│  CDN     │───▶│  Next.js     │───▶│  API Gateway │
│          │    │  (Vercel)    │    │  (Kong/AWS)  │
└──────────┘    └──────────────┘    └──────┬───────┘
                                           │
                              ┌────────────┼────────────┐
                              │            │            │
                       ┌──────▼──┐  ┌──────▼──┐  ┌─────▼─────┐
                       │ FastAPI │  │ Agent   │  │ Auth      │
                       │ Pods    │  │ Workers │  │ Service   │
                       └────┬────┘  └────┬────┘  └───────────┘
                            │            │
                       ┌────▼────────────▼────┐
                       │   PostgreSQL        │
                       │   + Event Store     │
                       └─────────────────────┘
```

---

## 10. Fairness Scoring Model (Conceptual)

```
Fairness Score = f(evidence_parity, advocacy_balance, policy_adherence)

Components:
├── Evidence Parity     — Equal weight given to both parties' evidence
├── Advocacy Balance    — Both advocates had opportunity to present
├── Policy Adherence    — Decision follows published reason code rules
└── Confidence Weight   — Higher confidence when evidence is conclusive

Score Range: 0–100
├── 90–100: High fairness (most seeded cases)
├── 80–89:  Moderate fairness
└── < 80:   Review recommended
```

---

*End of Additional Diagrams*
