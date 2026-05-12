from __future__ import annotations

import app as app_module
from app import create_app


class GenerateSpy:
    def __init__(self, answer="Generated answer from selected context."):
        self.answer = answer
        self.calls = []

    def __call__(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self.answer


def test_health_check_returns_ok():
    client = create_app().test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_ask_rejects_missing_query():
    client = create_app().test_client()

    response = client.post("/api/ask", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data
    assert "query" in data["error"].lower()


def test_ask_rejects_blank_query():
    client = create_app().test_client()

    response = client.post("/api/ask", json={"query": "   "})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_ask_rejects_non_string_query():
    client = create_app().test_client()

    response = client.post("/api/ask", json={"query": ["travel", "reimbursement"]})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_ask_returns_answer_sources_and_uses_prompt(monkeypatch):
    spy = GenerateSpy("Submit travel receipts within 14 days. Source: finance_travel_reimbursement")
    monkeypatch.setattr(app_module, "generate_response", spy)
    client = create_app().test_client()

    response = client.post(
        "/api/ask",
        json={"query": "How do I submit receipts for travel reimbursement?"},
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["query"] == "How do I submit receipts for travel reimbursement?"
    assert data["answer"] == "Submit travel receipts within 14 days. Source: finance_travel_reimbursement"
    assert data["sources"][0] == {
        "id": "finance_travel_reimbursement",
        "title": "Travel Reimbursement Procedure",
    }
    assert len(spy.calls) == 1
    assert "Instructions:" in spy.calls[0]
    assert "Context:" in spy.calls[0]
    assert "Question:" in spy.calls[0]
    assert "finance_travel_reimbursement" in spy.calls[0]


def test_ask_returns_query_dependent_sources(monkeypatch):
    spy = GenerateSpy()
    monkeypatch.setattr(app_module, "generate_response", spy)
    client = create_app().test_client()

    api_response = client.post(
        "/api/ask",
        json={"query": "How do developers authenticate internal API requests?"},
    )
    leave_response = client.post(
        "/api/ask",
        json={"query": "How many days of bereavement leave are available?"},
    )

    api_data = api_response.get_json()
    leave_data = leave_response.get_json()

    assert api_response.status_code == 200
    assert leave_response.status_code == 200
    assert api_data["sources"][0]["id"] == "dev_api_authentication"
    assert leave_data["sources"][0]["id"] == "hr_bereavement_leave"
    assert api_data["sources"][0]["id"] != leave_data["sources"][0]["id"]


def test_ask_returns_safe_fallback_when_no_context_found(monkeypatch):
    spy = GenerateSpy()
    monkeypatch.setattr(app_module, "generate_response", spy)
    client = create_app().test_client()

    response = client.post(
        "/api/ask",
        json={"query": "What is the cafeteria serving for lunch today?"},
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["query"] == "What is the cafeteria serving for lunch today?"
    assert data["sources"] == []
    assert "do not contain enough information" in data["answer"]
    assert spy.calls == []


def test_ask_returns_503_when_model_service_fails(monkeypatch):
    def failing_generate_response(prompt: str) -> str:
        raise RuntimeError("Could not connect to Ollama.")

    monkeypatch.setattr(app_module, "generate_response", failing_generate_response)
    client = create_app().test_client()

    response = client.post(
        "/api/ask",
        json={"query": "How do I request access to approved software?"},
    )
    data = response.get_json()

    assert response.status_code == 503
    assert "error" in data
    assert (
        "model" in data["error"].lower()
        or "ollama" in data["error"].lower()
        or "service" in data["error"].lower()
    )
