from __future__ import annotations

from typing import Any

from hookify import Plugin, PluginRegistry, RequestContext
from hookify.plugins import PIIMaskPlugin


class OrderPlugin(Plugin):
    def __init__(self, name: str, order: list[str]) -> None:
        self._name = name
        self._order = order

    def before_request(self, ctx: RequestContext) -> None:
        self._order.append(self._name)

    def after_response(self, ctx: RequestContext, response: dict[str, Any]) -> dict[str, Any]:
        response = dict(response)
        response.setdefault("trail", []).append(f"after:{self._name}")
        return response


def test_registry_runs_before_in_registration_order() -> None:
    seq: list[str] = []
    r = PluginRegistry([OrderPlugin("a", seq), OrderPlugin("b", seq)])
    ctx = RequestContext(body={"messages": []})
    r.run_before(ctx)
    assert seq == ["a", "b"]


def test_registry_runs_after_chains_response() -> None:
    r = PluginRegistry([OrderPlugin("x", []), OrderPlugin("y", [])])
    ctx = RequestContext(body={})
    out = r.run_after(ctx, {"ok": True})
    assert out["trail"] == ["after:x", "after:y"]


def test_pii_runs_before_on_registry() -> None:
    r = PluginRegistry([PIIMaskPlugin()])
    ctx = RequestContext(
        body={"messages": [{"role": "user", "content": "a@b.co test"}]},
        user_id="u",
    )
    r.run_before(ctx)
    assert "[email]" in ctx.body["messages"][0]["content"]
