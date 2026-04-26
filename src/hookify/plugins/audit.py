from __future__ import annotations

from collections.abc import Callable
from typing import Any

from hookify.base import Plugin, RequestContext
from hookify.plugins.pii import _mask_text


def _collect_prompt_text(body: dict[str, Any]) -> str:
    msgs = body.get("messages")
    if not isinstance(msgs, list):
        return ""
    parts: list[str] = []
    for m in msgs:
        if isinstance(m, dict) and isinstance(m.get("content"), str):
            parts.append(m["content"])
    return "\n".join(parts)


class AuditLogPlugin(Plugin):
    name = "audit"

    def __init__(self, sink: Callable[[str], None] | None = None) -> None:
        self._sink = sink

    def before_request(self, ctx: RequestContext) -> None:
        if not self._sink:
            return
        raw = _collect_prompt_text(ctx.body)
        masked = _mask_text(raw)[:2000]
        uid = ctx.user_id or "anonymous"
        self._sink(f"user={uid} model={ctx.model} prompt_masked={masked!r}")
