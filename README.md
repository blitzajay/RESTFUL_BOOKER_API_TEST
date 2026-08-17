# Restful Booker API Test Framework

An interview-focused API automation framework built with Python, Pytest,
Requests, and JSON Schema. It exercises the Restful Booker API through reusable
clients, fixtures, test-data factories, validators, logging, and environment
configuration.

## Framework Architecture

See the [framework architecture](docs/architecture.md) for the component design,
request flow, validation strategy, and interview-ready explanation.

## Run the Tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Copy `.env.example` when you need to supply different environment settings.
