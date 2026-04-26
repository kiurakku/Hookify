from __future__ import annotations

from typing import Any

from hookify.base import Plugin, RequestContext


class PluginRegistry:
    def __init__(self, plugins: list[Plugin] | None = None) -> None:
        self._plugins: list[Plugin] = list(plugins or [])

    @property
    def plugins(self) -> list[Plugin]:
        return list(self._plugins)

    def register(self, plugin: Plugin) -> None:
        self._plugins.append(plugin)

    def run_before(self, ctx: RequestContext) -> None:
        for p in self._plugins:
            p.before_request(ctx)

    def run_after(self, ctx: RequestContext, response: dict[str, Any]) -> dict[str, Any]:
        out = response
        for p in self._plugins:
            out = p.after_response(ctx, out)
        return out
