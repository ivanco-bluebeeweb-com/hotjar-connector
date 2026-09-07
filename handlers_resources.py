"""Resource handlers for Hotjar Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListEventParams, GetEventParams,
    EventRecord, EventList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_events", "List events in Hotjar.", action_type="read", chain_callable=True, event="hotjar-connector.list_events", effects=["read:events"], data_model=EventList)
async def list_events(ctx, params: ListEventParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_events(limit=params.limit)
        items = []
        for r in raw_items:
            rid = str(r.get("id") or r.get("key") or r.get("uuid") or "unknown")
            rname = r.get("name") or r.get("title") or r.get("label") or rid
            items.append({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r})
        return ActionResult.success({"events": items, "total": len(items)}, summary=f"Found {len(items)} events.")
    except Exception as e:
        return ActionResult.error(f"Error listing events: {e}")

@chat.function("get_event", "Get details of one Event in Hotjar.", action_type="read", chain_callable=True, event="hotjar-connector.get_event", effects=["read:event"], data_model=EventRecord)
async def get_event(ctx, params: GetEventParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_event(params.event_id)
        rid = str(r.get("id") or params.event_id)
        rname = r.get("name") or r.get("title") or rid
        return ActionResult.success({"id": rid, "name": rname, "status": r.get("status"), "created_at": r.get("createdAt") or r.get("created_at"), "raw": r}, summary=f"Retrieved Event {rid}.")
    except Exception as e:
        return ActionResult.error(f"Error retrieving Event: {e}")

@chat.function("audit_event_health", "Audit health of Hotjar events and connectivity.", action_type="read", chain_callable=True, event="hotjar-connector.audit_event_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_event_health(ctx, params: ConnectionIdParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_events(limit=50)
        return ActionResult.success({
            "healthy": True,
            "total_events": len(items),
            "details": {"sample_count": len(items)},
            "summary": f"Hotjar healthy. Sampled {len(items)} events."
        }, summary=f"Hotjar health check passed with {len(items)} events.")
    except Exception as e:
        return ActionResult.error(f"Error auditing Hotjar health: {e}")
