from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(title="Aegis Resolve AI", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Evidence(BaseModel):
    id: str
    type: str
    title: str
    source: str
    trust: int = Field(ge=0, le=100)
    relation: Literal["confirms", "contradicts", "supplements"]
    detail: str


class Verdict(BaseModel):
    outcome: Literal["card_member", "merchant", "human_review"]
    confidence: int = Field(ge=0, le=100)
    fairness: int = Field(ge=0, le=100)
    headline: str
    explanation: str
    policy_code: str
    policy_title: str


class Dispute(BaseModel):
    id: str
    title: str
    card_member: str
    merchant: str
    amount: float
    currency: str = "USD"
    reason_code: str
    reason: str
    status: Literal["open", "processing", "resolved", "human_review"]
    created_at: str
    deadline: str
    evidence: list[Evidence]
    verdict: Verdict | None = None
    events: list[dict[str, str]]


class CreateDispute(BaseModel):
    title: str
    card_member: str
    merchant: str
    amount: float = Field(gt=0)
    reason_code: str


class EvidenceInput(BaseModel):
    title: str
    type: str = "Document"
    detail: str


POLICIES = {
    "4512": ("Multiple Processing", "A card member may dispute a transaction processed more than once."),
    "4544": ("Cancellation of Recurring Goods / Services", "Cancellation evidence and merchant notice are required."),
    "4553": ("Not as Described or Defective Merchandise", "Compare the merchant representation with objective product evidence."),
    "4554": ("Goods and Services Not Received", "Proof of delivery, service completion, or a refund determines the outcome."),
    "4763": ("Fraud Full Recourse", "Assess account takeover signals and transaction authentication evidence."),
}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def evidence(identifier: str, evidence_type: str, title: str, source: str, trust: int, relation: str, detail: str) -> Evidence:
    return Evidence(id=identifier, type=evidence_type, title=title, source=source, trust=trust, relation=relation, detail=detail)


def seeded_disputes() -> dict[str, Dispute]:
    cases = [
        Dispute(id="AR-2026-001", title="Alpine camera never arrived", card_member="Maya Chen", merchant="Alpine Outfitters", amount=348.00, reason_code="4554", reason="Goods not received", status="resolved", created_at="2026-07-21 10:14 UTC", deadline="2026-08-10", evidence=[evidence("ev-1", "Transaction", "Card transaction", "Amex network", 100, "confirms", "Captured payment for $348.00."), evidence("ev-2", "Shipment", "Carrier delivery proof", "Nimbus Logistics", 96, "confirms", "Signed delivery and GPS scan at the card member address."), evidence("ev-3", "Communication", "Customer contact", "Support desk", 76, "supplements", "Card member reported non-receipt before the delivery scan was reviewed.")], verdict=Verdict(outcome="merchant", confidence=94, fairness=97, headline="Merchant position upheld", explanation="Independent delivery proof directly confirms fulfillment. The customer report was considered but is not supported by contradictory evidence.", policy_code="4554", policy_title="Goods and Services Not Received"), events=[]),
        Dispute(id="AR-2026-002", title="Aurora headphones differ from listing", card_member="Noah Williams", merchant="Aurora Audio", amount=189.99, reason_code="4553", reason="Not as described", status="human_review", created_at="2026-07-22 08:45 UTC", deadline="2026-08-11", evidence=[evidence("ev-4", "Invoice", "Order invoice", "Aurora Audio", 94, "confirms", "Confirms model number purchased."), evidence("ev-5", "Document", "Product photographs", "Card member", 70, "contradicts", "Photos suggest a finish different from the product page."), evidence("ev-6", "Communication", "Merchant response", "Aurora Audio", 72, "supplements", "Merchant states the finish is a permitted production variation.")], verdict=Verdict(outcome="human_review", confidence=61, fairness=91, headline="Human review required", explanation="Both advocates present credible, conflicting product-description evidence. A specialist should compare the original listing archive.", policy_code="4553", policy_title="Not as Described or Defective Merchandise"), events=[]),
        Dispute(id="AR-2026-003", title="Duplicate ride-share charge", card_member="Aisha Patel", merchant="CityRide", amount=42.50, reason_code="4512", reason="Multiple processing", status="resolved", created_at="2026-07-23 15:30 UTC", deadline="2026-08-12", evidence=[evidence("ev-7", "Transaction", "Duplicate authorizations", "Amex network", 100, "confirms", "Two matching charges share an identical trip and timestamp."), evidence("ev-8", "Receipt", "Ride receipt", "CityRide", 98, "confirms", "Only one completed ride is recorded.")], verdict=Verdict(outcome="card_member", confidence=99, fairness=99, headline="Card member claim upheld", explanation="The payment record and merchant receipt both establish duplicate processing. A credit is due.", policy_code="4512", policy_title="Multiple Processing"), events=[]),
        Dispute(id="AR-2026-004", title="Subscription charged after cancellation", card_member="Elias Morgan", merchant="Streamline Fitness", amount=79.00, reason_code="4544", reason="Recurring cancellation", status="human_review", created_at="2026-07-24 12:10 UTC", deadline="2026-08-13", evidence=[evidence("ev-9", "Communication", "Cancellation email", "Card member", 88, "confirms", "Email requests cancellation before the renewal date."), evidence("ev-10", "Document", "Membership terms", "Streamline Fitness", 80, "contradicts", "Terms require notice through the account portal."), evidence("ev-11", "Transaction", "Renewal charge", "Amex network", 100, "confirms", "Charge posted after the cancellation email.")], verdict=Verdict(outcome="human_review", confidence=58, fairness=92, headline="Human review required", explanation="The cancellation channel is disputed. A reviewer should verify whether email was accepted as notice under the applicable agreement.", policy_code="4544", policy_title="Cancellation of Recurring Goods / Services"), events=[]),
        Dispute(id="AR-2026-005", title="Unrecognized electronics transaction", card_member="Sofia Reyes", merchant="Nova Electronics", amount=619.00, reason_code="4763", reason="Unauthorized transaction", status="resolved", created_at="2026-07-25 09:02 UTC", deadline="2026-08-14", evidence=[evidence("ev-12", "Device", "Device mismatch", "Fraud signals", 93, "confirms", "Purchase device differs materially from established account behavior."), evidence("ev-13", "Transaction", "Authentication trace", "Amex network", 90, "confirms", "No successful step-up authentication was recorded."), evidence("ev-14", "Shipment", "Delivery reroute", "Nimbus Logistics", 89, "confirms", "Shipment was rerouted after checkout.")], verdict=Verdict(outcome="card_member", confidence=96, fairness=98, headline="Card member claim upheld", explanation="Independent fraud signals and the lack of authentication support the card member's claim.", policy_code="4763", policy_title="Fraud Full Recourse"), events=[]),
    ]
    for dispute in cases:
        dispute.events = build_events(dispute)
    return {case.id: case for case in cases}


def build_events(dispute: Dispute) -> list[dict[str, str]]:
    steps = [
        ("Case filed", "Orchestrator", "Case normalized and SLA timer started."),
        ("Evidence assembled", "Evidence Collection Agent", f"Connected {len(dispute.evidence)} evidence records into the trust graph."),
        ("Documents interpreted", "Document Intelligence Agent", "Extracted structured facts and evidence confidence."),
        ("Two-sided advocacy", "Customer and Merchant Advocates", "Generated isolated, evidence-grounded positions for both parties."),
        ("Policy evaluated", "Policy & Compliance Agent", f"Applied AMEX code {dispute.reason_code}: {dispute.reason}."),
        ("Risk and fairness scored", "Financial Risk & Fairness Engine", "Measured evidence completeness, quality, and parity."),
        ("Verdict issued", "Neutral Judge Agent", dispute.verdict.headline if dispute.verdict else "Awaiting decision."),
        ("Explanation and audit saved", "Explainability & Audit Agents", "Stored policy citations, rationale, and immutable replay event."),
    ]
    return [{"time": f"09:{index:02d}", "title": title, "agent": agent, "detail": detail} for index, (title, agent, detail) in enumerate(steps, start=2)]


DATABASE_PATH = Path(__file__).with_name("aegis_resolve.db")


def database_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def save_case(dispute: Dispute) -> None:
    payload = json.dumps(dispute.model_dump(mode="json"))
    with database_connection() as connection:
        connection.execute(
            "INSERT INTO disputes (id, payload) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET payload = excluded.payload",
            (dispute.id, payload),
        )


def all_cases() -> list[Dispute]:
    with database_connection() as connection:
        rows = connection.execute("SELECT payload FROM disputes ORDER BY id").fetchall()
    return [Dispute.model_validate(json.loads(row["payload"])) for row in rows]


def get_case(dispute_id: str) -> Dispute:
    with database_connection() as connection:
        row = connection.execute("SELECT payload FROM disputes WHERE id = ?", (dispute_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return Dispute.model_validate(json.loads(row["payload"]))


def initialise_database() -> None:
    with database_connection() as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS disputes (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        count = connection.execute("SELECT COUNT(*) FROM disputes").fetchone()[0]
    if count == 0:
        for dispute in seeded_disputes().values():
            save_case(dispute)


initialise_database()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "aegis-resolve-api"}


@app.get("/v1/disputes", response_model=list[Dispute])
def list_disputes() -> list[Dispute]:
    return all_cases()


@app.post("/v1/disputes", response_model=Dispute, status_code=201)
def create_dispute(payload: CreateDispute) -> Dispute:
    policy_title, _ = POLICIES.get(payload.reason_code, ("Case assessment", "Policy guidance is pending classification."))
    dispute = Dispute(id=f"AR-2026-{str(uuid4())[:5].upper()}", title=payload.title, card_member=payload.card_member, merchant=payload.merchant, amount=payload.amount, reason_code=payload.reason_code, reason=policy_title, status="open", created_at=now(), deadline="2026-08-20", evidence=[], events=[])
    dispute.events = build_events(dispute)
    save_case(dispute)
    return dispute


@app.get("/v1/disputes/{dispute_id}", response_model=Dispute)
def get_dispute(dispute_id: str) -> Dispute:
    return get_case(dispute_id)


@app.post("/v1/disputes/{dispute_id}/evidence", response_model=Dispute)
def add_evidence(dispute_id: str, payload: EvidenceInput) -> Dispute:
    dispute = get_case(dispute_id)
    dispute.evidence.append(evidence(f"ev-{uuid4().hex[:5]}", payload.type, payload.title, "Submitted by party", 70, "supplements", payload.detail))
    dispute.events.insert(1, {"time": now(), "title": "Supplementary evidence received", "agent": "Evidence Collection Agent", "detail": payload.title})
    save_case(dispute)
    return dispute


@app.post("/v1/disputes/{dispute_id}/process", response_model=Dispute)
def process_dispute(dispute_id: str) -> Dispute:
    dispute = get_case(dispute_id)
    if dispute.verdict is None:
        policy_title, policy_text = POLICIES.get(dispute.reason_code, ("Case assessment", "The policy engine classified the provided evidence."))
        dispute.verdict = Verdict(outcome="human_review", confidence=65, fairness=90, headline="Human review required", explanation=f"{policy_text} The submitted evidence needs a specialist review before resolution.", policy_code=dispute.reason_code, policy_title=policy_title)
        dispute.status = "human_review"
        dispute.events = build_events(dispute)
    save_case(dispute)
    return dispute


@app.get("/v1/disputes/{dispute_id}/verdict", response_model=Verdict)
def get_verdict(dispute_id: str) -> Verdict:
    dispute = get_case(dispute_id)
    if dispute.verdict is None:
        raise HTTPException(status_code=409, detail="Verdict is not ready")
    return dispute.verdict


@app.get("/v1/disputes/{dispute_id}/evidence-graph")
def evidence_graph(dispute_id: str) -> dict:
    dispute = get_case(dispute_id)
    nodes = [{"id": "case", "type": "case", "label": dispute.title, "trust": 100}] + [{"id": item.id, "type": item.type, "label": item.title, "trust": item.trust} for item in dispute.evidence]
    edges = [{"id": f"case-{item.id}", "source": "case", "target": item.id, "label": item.relation} for item in dispute.evidence]
    return {"nodes": nodes, "edges": edges}


@app.get("/v1/disputes/{dispute_id}/replay")
def replay(dispute_id: str) -> list[dict[str, str]]:
    return get_case(dispute_id).events


@app.post("/v1/disputes/{dispute_id}/override", response_model=Dispute)
def override(dispute_id: str, outcome: Literal["card_member", "merchant", "human_review"], note: str) -> Dispute:
    dispute = get_case(dispute_id)
    if dispute.verdict is None:
        raise HTTPException(status_code=409, detail="Process the case before overriding it")
    dispute.verdict.outcome = outcome
    dispute.verdict.headline = "Analyst override recorded"
    dispute.verdict.explanation = note
    dispute.status = "resolved" if outcome != "human_review" else "human_review"
    dispute.events.append({"time": now(), "title": "Human decision recorded", "agent": "Operations Analyst", "detail": note})
    save_case(dispute)
    return dispute


@app.get("/v1/analytics/control-center")
def control_center() -> dict:
    cases = all_cases()
    verdicts = [case.verdict for case in cases if case.verdict]
    evidence_trust = [item.trust for case in cases for item in case.evidence]
    resolved = len([case for case in cases if case.status == "resolved"])
    return {
        "cases": len(cases),
        "open_cases": len([case for case in cases if case.status in ("open", "processing")]),
        "human_review": len([case for case in cases if case.status == "human_review"]),
        "resolution_rate": round((resolved / len(cases)) * 100) if cases else 0,
        "average_minutes": round(sum(max(len(case.events) - 1, 0) for case in cases) / len(cases)) if cases else 0,
        "average_confidence": round(sum(verdict.confidence for verdict in verdicts) / len(verdicts)) if verdicts else 0,
        "average_evidence_trust": round(sum(evidence_trust) / len(evidence_trust)) if evidence_trust else 0,
    }

@app.get("/v1/analytics/fairness")
def fairness() -> dict:
    decided = [case.verdict.fairness for case in all_cases() if case.verdict]
    return {"average": round(sum(decided) / len(decided)), "distribution": [{"band": "90-100", "count": len([score for score in decided if score >= 90])}, {"band": "80-89", "count": len([score for score in decided if 80 <= score < 90])}, {"band": "Below 80", "count": len([score for score in decided if score < 80])}]}


@app.websocket("/v1/disputes/{dispute_id}/stream")
async def case_stream(websocket: WebSocket, dispute_id: str) -> None:
    dispute = get_case(dispute_id)
    await websocket.accept()
    for event in dispute.events:
        await websocket.send_json(event)
    await websocket.close()



