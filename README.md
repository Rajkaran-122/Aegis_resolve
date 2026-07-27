# Aegis Resolve AI

An explainable dispute-resolution MVP built around a Digital Arbitration Court: an Evidence Trust Graph, dual advocacy, policy-driven verdicts, fairness scoring, and a complete audit replay.

## Demo capabilities

- Five seeded AMEX-inspired scenarios: `4512`, `4544`, `4553`, `4554`, and `4763`.
- Customer, merchant, and enterprise-control-center experiences over one shared case record.
- Evidence nodes with trust scores and confirms / contradicts / supplements relationships.
- Verdicts with confidence, fairness, policy citation, clear rationale, human-review routing, and analyst override endpoint.
- Courtroom Replay events and a WebSocket stream for visible agent activity.

## Run locally

Open two terminals from this folder.

```powershell
# Terminal 1: API
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

```powershell
# Terminal 2: web app
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`. The API docs are at `http://localhost:8000/docs`.

## Suggested demo

1. Open the **Control Center**.
2. Select `AR-2026-002` from the human-review queue.
3. Inspect its evidence record, AMEX `4553` policy basis, confidence/fairness, and Courtroom Replay.
4. Open the customer and merchant workspaces to demonstrate one shared case from both sides.
5. Use API docs to submit evidence, process a new dispute, or record an analyst override.

## Architecture

The MVP uses an in-memory data store and deterministic policy outcomes, so it runs reliably without credentials or external services. FastAPI exposes disputes, evidence, verdicts, graph data, replay, overrides, analytics, and real-time events.

For production, replace in-memory state with PostgreSQL, persist audit events immutably, govern policy definitions under version control, add authentication/tenant isolation, and connect agent boundaries to LangGraph plus an approved model provider.

## Quality checks

```powershell
cd backend
python -m compileall .

cd ../frontend
npm run build
```
