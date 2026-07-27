# Product Requirements Document (PRD)

## Aegis Resolve AI — Digital Arbitration Court

| Field | Value |
|-------|-------|
| **Product** | Aegis Resolve AI |
| **Version** | MVP 0.1.0 |
| **Document Owner** | Product Team |
| **Last Updated** | July 27, 2026 |
| **Status** | Approved for Demo Submission |

---

## 1. Executive Summary

Aegis Resolve AI is an explainable dispute-resolution platform that models payment and card disputes as a **Digital Arbitration Court**. The MVP demonstrates how card members, merchants, and enterprise analysts can interact with a single shared case record — complete with evidence trust scoring, policy-grounded verdicts, fairness metrics, and a replayable audit trail.

The product targets hackathon/demo submission and stakeholder validation before production investment.

---

## 2. Problem Statement

Payment disputes today suffer from:

- **Slow resolution** — weeks of back-and-forth between parties and issuers
- **Opacity** — parties rarely see how decisions are reached
- **Audit gaps** — compliance teams cannot easily replay decision logic
- **Inconsistent fairness** — manual review quality varies by analyst workload

Aegis Resolve addresses these by making every decision **evidence-led, policy-cited, and fully auditable**.

---

## 3. Product Vision

> Turn complex payment disputes into evidence-led, fair, and explainable decisions — in minutes, not weeks.

---

## 4. Target Users & Personas

| Persona | Role | Primary Goal |
|---------|------|--------------|
| **Maya (Card Member)** | Consumer disputing a charge | Understand case status, see why a verdict was reached |
| **Jordan (Merchant)** | Business responding to disputes | Submit evidence, track incoming cases, defend position |
| **Alex (Operations Analyst)** | Enterprise dispute analyst | Review edge cases, override AI recommendations, monitor fairness |

---

## 5. Product Scope — MVP (v0.1.0)

### 5.1 In Scope

| Feature | Description | Priority |
|---------|-------------|----------|
| **Landing Page** | Marketing hero, product pillars, live case preview | P0 |
| **Customer Portal** | Dashboard, case list, case detail, file-dispute flow | P0 |
| **Merchant Portal** | Incoming cases dashboard, case response view | P0 |
| **Enterprise Control Center** | Human-review queue, KPI metrics, courtroom dossier | P0 |
| **Dispute API** | CRUD, evidence submission, processing, override | P0 |
| **Evidence Trust Graph** | Evidence nodes with trust scores and relations | P0 |
| **Policy Engine** | AMEX-inspired reason codes (4512, 4544, 4553, 4554, 4763) | P0 |
| **Verdict Display** | Confidence, fairness, headline, explanation, policy citation | P0 |
| **Courtroom Replay** | Step-by-step agent activity timeline | P0 |
| **Analytics Endpoints** | Control-center KPIs and fairness distribution | P1 |
| **WebSocket Stream** | Real-time replay event streaming (API) | P1 |
| **Seeded Demo Data** | Five pre-built scenarios covering all reason codes | P0 |

### 5.2 Out of Scope (Future Releases)

- Real LLM/agent orchestration (LangGraph integration)
- Production authentication and RBAC
- Multi-tenant isolation
- Live evidence graph visualization (@xyflow/react)
- Functional file-upload evidence ingestion
- Analyst override UI wiring (API exists; UI is demo-only)
- PostgreSQL and immutable event store
- Email/SMS notifications
- Payment network integration

---

## 6. User Stories

### Card Member

| ID | Story | Acceptance Criteria |
|----|-------|-------------------|
| CM-01 | As a card member, I want to see my active disputes so I can track resolution progress | Dashboard lists cases with status badges and amounts |
| CM-02 | As a card member, I want to view verdict details so I understand the outcome | Case detail shows confidence, fairness, policy, and explanation |
| CM-03 | As a card member, I want to file a new dispute so I can initiate a claim | Three-step form captures title, merchant, amount, reason code |
| CM-04 | As a card member, I want to see evidence supporting my case | Evidence list shows type, source, trust score, and relation |

### Merchant

| ID | Story | Acceptance Criteria |
|----|-------|-------------------|
| MR-01 | As a merchant, I want to see incoming dispute cases | Merchant dashboard lists cases with readiness metrics |
| MR-02 | As a merchant, I want to review evidence and verdict for a case | Case detail mirrors shared record with merchant perspective |
| MR-03 | As a merchant, I want to submit supporting evidence | Submit button present (API endpoint available) |

### Enterprise Analyst

| ID | Story | Acceptance Criteria |
|----|-------|-------------------|
| AN-01 | As an analyst, I want a human-review queue so I can prioritize edge cases | Control Center highlights `human_review` status cases |
| AN-02 | As an analyst, I want courtroom replay so I can audit agent decisions | Timeline shows orchestrator → judge pipeline events |
| AN-03 | As an analyst, I want to override a verdict with a note | Override API accepts outcome + note; UI button present |
| AN-04 | As an analyst, I want KPI metrics for operational oversight | Control Center shows resolution rate, confidence, trust averages |

---

## 7. Functional Requirements

### 7.1 Dispute Lifecycle

```
Create → Add Evidence → Process → Verdict → (Optional) Analyst Override → Resolved
```

1. **Create** — POST `/v1/disputes` with title, parties, amount, reason code
2. **Evidence** — POST `/v1/disputes/{id}/evidence` appends trust-scored nodes
3. **Process** — POST `/v1/disputes/{id}/process` runs policy engine
4. **Verdict** — GET `/v1/disputes/{id}/verdict` returns structured outcome
5. **Override** — POST `/v1/disputes/{id}/override?outcome=&note=` records analyst decision

### 7.2 Evidence Model

Each evidence item includes:

- **Type** — Transaction, Shipment, Document, Communication, Device, Receipt, Invoice
- **Trust Score** — 0–100 confidence in evidence reliability
- **Relation** — `confirms`, `contradicts`, or `supplements` the case narrative
- **Source** — Originating system or party

### 7.3 Verdict Model

Every verdict includes:

- **Outcome** — `card_member`, `merchant`, or `human_review`
- **Confidence** — 0–100 model certainty
- **Fairness** — 0–100 parity score across both parties
- **Policy Code & Title** — AMEX-inspired reason code citation
- **Headline & Explanation** — Human-readable rationale

### 7.4 Policy Codes (MVP)

| Code | Title | Use Case |
|------|-------|----------|
| 4512 | Multiple Processing | Duplicate charges |
| 4544 | Cancellation of Recurring Goods / Services | Subscription disputes |
| 4553 | Not as Described or Defective Merchandise | Product mismatch |
| 4554 | Goods and Services Not Received | Non-delivery |
| 4763 | Fraud Full Recourse | Unauthorized transactions |

---

## 8. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Performance** | API responses < 200ms for seeded data |
| **Availability** | Runs locally without external dependencies |
| **Usability** | Three portals accessible from single navigation |
| **Accessibility** | Responsive layout; dark theme with high-contrast accents |
| **Security** | CORS restricted to localhost:3000 (MVP); auth planned for production |
| **Auditability** | Every case stores immutable event timeline |
| **Reliability** | Frontend degrades gracefully with hardcoded fallback data |

---

## 9. Demo Scenarios

| Case ID | Scenario | Code | Status | Outcome |
|---------|----------|------|--------|---------|
| AR-2026-001 | Alpine camera never arrived | 4554 | Resolved | Merchant |
| AR-2026-002 | Aurora headphones differ from listing | 4553 | Human Review | Human Review |
| AR-2026-003 | Duplicate ride-share charge | 4512 | Resolved | Card Member |
| AR-2026-004 | Subscription charged after cancellation | 4544 | Human Review | Human Review |
| AR-2026-005 | Unrecognized electronics transaction | 4763 | Resolved | Card Member |

**Recommended demo path:**

1. Open Control Center → select AR-2026-002
2. Inspect evidence, AMEX 4553 policy, confidence/fairness, replay
3. Open customer and merchant views for the same case
4. Use Swagger UI to submit evidence, process, or override

---

## 10. Success Metrics

| Metric | MVP Target | Measurement |
|--------|------------|-------------|
| Average resolution time | ≤ 8 minutes (demo) | Control Center analytics |
| Fairness index | ≥ 90 average | `/v1/analytics/fairness` |
| Confidence calibration | Visible on every verdict | Verdict model field |
| Human-review routing | Edge cases flagged correctly | AR-2026-002, AR-2026-004 |
| Audit completeness | 100% cases have replay events | `/v1/disputes/{id}/replay` |
| API coverage | All CRUD + process + override | OpenAPI at `/docs` |

---

## 11. Dependencies & Assumptions

- Users run backend (Python 3.12) and frontend (Node.js) locally or via Docker Compose
- No external API keys or cloud services required for MVP
- AMEX reason codes used as policy proxy; not affiliated with American Express
- Agent pipeline is conceptual (replay narrative); real LLM integration is post-MVP

---

## 12. Release Plan

| Phase | Deliverable | Timeline |
|-------|-------------|----------|
| **MVP 0.1.0** | Demo submission — 3 portals, API, 5 seeded cases | Current |
| **v0.2.0** | Wire remaining UI to API; live graph viz | Q3 2026 |
| **v0.3.0** | Auth, PostgreSQL, immutable audit store | Q4 2026 |
| **v1.0.0** | LangGraph agents, production deployment | Q1 2027 |

---

## 13. Open Questions

1. Which LLM provider will be approved for production agent orchestration?
2. Will policy definitions be governed by compliance team or engineering?
3. What SLA targets apply for human-review queue escalation?
4. Is multi-currency support required for initial production launch?

---

*End of PRD*
