from __future__ import annotations

from flask import Flask, jsonify, request

from lib.ai_client import generate_response
from lib.company_documents import COMPANY_DOCUMENTS
from lib.rag_service import build_prompt, retrieve_context, source_metadata


def create_app():
    app = Flask(__name__)

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"})

    @app.post("/api/ask")
    def ask_question():
        """Accept a query and return a source-backed generated answer.

        TODO:
        1. Read JSON request data safely.
        2. Validate that `query` is a non-empty string.
        3. Retrieve relevant context from COMPANY_DOCUMENTS.
        4. If no context is found, return a safe fallback with an empty sources list.
        5. Build a structured prompt from the selected context.
        6. Call generate_response(prompt).
        7. Return query, answer, and sources as JSON.
        8. If generate_response raises RuntimeError, return a 503 service error.
        """
        # TODO: Replace this placeholder response with your implementation.
        return jsonify({"message": "TODO: implement /api/ask"}), 501

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
