from __future__ import annotations

import re
from typing import Any

from hookify.base import Plugin, RequestContext

_EMAIL = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
_PHONE = re.compile(r"\b\+?\d[\d\s\-()]{7,}\d\b")


def _mask_text(s: str) -> str:
    s = _EMAIL.sub("[email]", s)
    s = _PHONE.sub("[phone]", s)
    return s


def _walk_messages(body: dict[str, Any]) -> None:
    msgs = body.get("messages")
    if not isinstance(msgs, list):
        return
    for m in msgs:
        if isinstance(m, dict) and isinstance(m.get("content"), str):
            m["content"] = _mask_text(m["content"])


class PIIMaskPlugin(Plugin):
    name = "pii_mask"

    def before_request(self, ctx: RequestContext) -> None:
        _walk_messages(ctx.body)
