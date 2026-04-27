# Hookify

[![CI](https://github.com/kiurakku/Hookify/actions/workflows/ci.yml/badge.svg)](https://github.com/kiurakku/Hookify/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Lightweight plugin registry with `before_request` / `after_response` hooks for FastAPI and LLM gateways.

Hookify is intentionally small: you wire plugins into your request pipeline, each plugin can mutate request context, reject suspicious input, or post-process responses.

<p align="center">
  <img src="docs/images/hookify-logo.jpg" alt="Hookify visual" width="320" />
</p>

## Why this project exists

Hookify is the reusable plugin layer in a 3-repository ecosystem:

- [BOLA](https://github.com/kiurakku/BOLA): OWASP API security training lab.
- [FastLM-API](https://github.com/kiurakku/FastLM-API): OpenAI-compatible LLM gateway.
- **Hookify**: portable hook system used by FastLM request/response flow.

## Core concepts

- `RequestContext`: shared mutable context (`body`, `user_id`, `model`, `extras`).
- `Plugin`: base class with `before_request()` and `after_response()`.
- `PluginRegistry`: deterministic execution in registration order.

## Built-in plugins

- `PIIMaskPlugin`: masks email and phone patterns in message content.
- `PromptInjectionPlugin`: detects common jailbreak/prompt-injection phrases and sets `ctx.extras["http_reject"]`.
- `AuditLogPlugin`: sends masked prompt audit lines into your sink function.
- `CostLimitPlugin`: budget guard plugin (available in package; you provide usage callback + budget).

## Example

```python
from hookify import PluginRegistry, RequestContext
from hookify.plugins import PIIMaskPlugin, PromptInjectionPlugin

registry = PluginRegistry([
    PIIMaskPlugin(),
    PromptInjectionPlugin(),
])

ctx = RequestContext(
    body={"messages": [{"role": "user", "content": "email me at dev@example.com"}]},
    user_id="u-1",
    model="gpt-4o-mini",
)

registry.run_before(ctx)

if "http_reject" in ctx.extras:
    message, status_code = ctx.extras["http_reject"]
    # return HTTP error in your API layer

response = {"choices": [{"message": {"role": "assistant", "content": "ok"}}]}
response = registry.run_after(ctx, response)
```

## Installation

```bash
git clone https://github.com/kiurakku/Hookify.git
cd Hookify
pip install -e .
```

or directly from GitHub:

```bash
pip install git+https://github.com/kiurakku/Hookify.git
```

## Development

```bash
pip install -e ".[dev]"
pytest -v --tb=short
python -m ruff check src tests
```

## Project structure

```text
src/hookify/
  base.py          # RequestContext + Plugin base class
  registry.py      # PluginRegistry
  plugins/
    pii.py
    injection.py
    audit.py
    cost.py
tests/
  test_pii.py
  test_injection.py
  test_registry.py
```

## Release notes

See [CHANGELOG.md](CHANGELOG.md).

---

If you want to replicate the polished GitHub profile style (About, topics, release notes), set:

- **Description**: `Lightweight plugin registry with before/after hooks for FastAPI`
- **Topics**: `python`, `fastapi`, `plugins`, `middleware`, `llm`
