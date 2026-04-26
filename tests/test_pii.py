from __future__ import annotations

from hookify import RequestContext
from hookify.plugins import PIIMaskPlugin


def test_pii_masks_email_and_phone() -> None:
    ctx = RequestContext(
        body={
            "messages": [
                {
                    "role": "user",
                    "content": "Напиши на user@example.com або подзвони +380 12 345 67 89",
                }
            ]
        },
        user_id="u1",
        model="gpt-4o",
    )
    PIIMaskPlugin().before_request(ctx)
    text = ctx.body["messages"][0]["content"]
    assert "user@example.com" not in text
    assert "[email]" in text
    assert "+380" not in text
    assert "[phone]" in text
