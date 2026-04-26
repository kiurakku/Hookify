from __future__ import annotations

from collections.abc import Callable

from hookify.base import Plugin, RequestContext


class CostLimitPlugin(Plugin):
    name = "cost_limit"

    def __init__(
        self,
        get_monthly_used: Callable[[str], int],
        budget: int,
    ) -> None:
        self._get_used = get_monthly_used
        self._budget = budget

    def before_request(self, ctx: RequestContext) -> None:
        if not ctx.user_id:
            return
        used = self._get_used(ctx.user_id)
        if used >= self._budget:
            ctx.extras["http_reject"] = (
                "Вичерпано місячний бюджет токенів",
                429,
            )
