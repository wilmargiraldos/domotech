"""Persistent traceability for sales and operational events."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


class TraceStore:
    """JSON-backed sales history plus JSONL operational audit log."""

    def __init__(
        self,
        sales_path: Path | str = "data/sales_history.json",
        events_path: Path | str = "data/audit_log.jsonl",
    ):
        self.sales_path = Path(sales_path)
        self.events_path = Path(events_path)
        self.sales_path.parent.mkdir(parents=True, exist_ok=True)
        self.events_path.parent.mkdir(parents=True, exist_ok=True)

    def record_sale(
        self,
        username: str,
        cart_entries: list[dict[str, Any]],
        user_id: int | None = None,
        user_role: str = "client",
    ) -> dict[str, Any]:
        order_id = self._new_order_id()
        items = []
        total = 0.0

        for entry in cart_entries:
            product = entry["product"]
            qty = int(entry["qty"])
            unit_price = float(product["price"])
            line_total = round(unit_price * qty, 2)
            total += line_total
            items.append(
                {
                    "product_id": int(product["id"]),
                    "name": str(product["name"]),
                    "category": str(product["cat"]),
                    "qty": qty,
                    "unit_price": unit_price,
                    "line_total": line_total,
                }
            )

        sale = {
            "order_id": order_id,
            "timestamp": self._timestamp(),
            "user_id": user_id,
            "username": username,
            "user_role": user_role,
            "items": items,
            "total": round(total, 2),
            "status": "completed",
        }

        sales = self.list_sales()
        sales.append(sale)
        self._write_json(self.sales_path, sales)
        self.record_event(
            "sale_completed",
            user_id=user_id,
            username=username,
            user_role=user_role,
            order_id=order_id,
            total=sale["total"],
            item_count=sum(item["qty"] for item in items),
        )
        return sale

    def record_event(self, event_type: str, **details: Any) -> dict[str, Any]:
        event = {
            "timestamp": self._timestamp(),
            "event_type": event_type,
            "details": details,
        }
        with self.events_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")
        return event

    def list_sales(self) -> list[dict[str, Any]]:
        if not self.sales_path.exists():
            return []
        with self.sales_path.open("r", encoding="utf-8") as file:
            return list(json.load(file))

    def list_events(self) -> list[dict[str, Any]]:
        if not self.events_path.exists():
            return []
        events = []
        with self.events_path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    events.append(json.loads(line))
        return events

    def sales_summary(self) -> dict[str, Any]:
        sales = self.list_sales()
        total_revenue = round(sum(float(sale["total"]) for sale in sales), 2)
        total_items = sum(sum(int(item["qty"]) for item in sale["items"]) for sale in sales)
        return {
            "sales_count": len(sales),
            "total_revenue": total_revenue,
            "total_items": total_items,
        }

    def _write_json(self, path: Path, data: Any) -> None:
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")

    def _new_order_id(self) -> str:
        return f"DTWG-{uuid4().hex[:8].upper()}"

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()
