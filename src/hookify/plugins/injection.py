from __future__ import annotations

import re
from typing import Any

from hookify.base import Plugin, RequestContext

_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions?", re.I),
    re.compile(r"disregard\s+(the\s+)?(above|system)", re.I),
    re.compile(r"jailbreak", re.I),
    re.compile(r"you\s+are\s+now\s+(DAN|evil)", re.I),
]


def _collect_prompt_text(body: dict[str, Any]) -> str:
    msgs = body.get("messages")
    if not isinstance(msgs, list):
        return ""
    parts: list[str] = []
    for m in msgs:
        if isinstance(m, dict) and isinstance(m.get("content"), str):
            parts.append(m["content"])
    return "\n".join(parts)


class PromptInjectionPlugin(Plugin):
    name = "prompt_injection"

    def before_request(self, ctx: RequestContext) -> None:
        blob = _collect_prompt_text(ctx.body)
        for pat in _PATTERNS:
            if pat.search(blob):
                ctx.extras["http_reject"] = (
                    "Вміст схожий на спробу prompt injection",
                    400,
                )
                return
