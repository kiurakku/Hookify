from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RequestContext:
    """Контекст одного запиту (наприклад chat completions)."""

    body: dict[str, Any]
    user_id: str | None = None
    model: str | None = None
    extras: dict[str, Any] = field(default_factory=dict)


class Plugin:
    """Базовий плагін: перевизначте методи за потреби."""

    name: str = "plugin"

    def before_request(self, ctx: RequestContext) -> None:
        """Може змінювати ctx.body та ctx.extras."""

    def after_response(self, ctx: RequestContext, response: dict[str, Any]) -> dict[str, Any]:
        """Повертає (можливо змінений) JSON-відповіді."""
        return response
