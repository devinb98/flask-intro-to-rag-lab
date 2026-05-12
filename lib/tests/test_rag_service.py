from __future__ import annotations

from company_documents import COMPANY_DOCUMENTS
from rag_service import (
    build_prompt,
    document_search_text,
    format_context,
    retrieve_context,
    score_document,
    source_metadata,
    tokenize,
)


def ids(matches):
    return [match["document"]["id"] for match in matches]


def test_tokenize_returns_searchable_terms_without_common_stopwords():
    tokens = tokenize("How do I request travel reimbursement after 14 days?")

    assert isinstance(tokens, set)
    assert "travel" in tokens
    assert "reimbursement" in tokens
    assert "14" in tokens
    assert "days" in tokens
    assert "how" not in tokens
    assert "do" not in tokens
    assert "i" not in tokens


def test_document_search_text_combines_metadata_and_body_text():
    document = COMPANY_DOCUMENTS[0]
    searchable = document_search_text(document).lower()

    assert document["title"].lower() in searchable
    assert document["category"].lower() in searchable
    assert " ".join(document["tags"]).lower() in searchable
    assert document["text"][:30].lower() in searchable


def test_score_document_returns_score_and_matched_terms():
    travel_document = next(
        document
        for document in COMPANY_DOCUMENTS
        if document["id"] == "finance_travel_reimbursement"
    )

    result = score_document("travel reimbursement receipts", travel_document)

    assert result["document"] == travel_document
    assert result["score"] >= 3
    assert "travel" in result["matched_terms"]
    assert "reimbursement" in result["matched_terms"]
    assert "receipts" in result["matched_terms"]


def test_retrieve_context_selects_travel_reimbursement_for_expense_query():
    matches = retrieve_context(
        "How do I submit receipts for travel reimbursement?",
        COMPANY_DOCUMENTS,
    )

    assert matches
    assert matches[0]["document"]["id"] == "finance_travel_reimbursement"


def test_retrieve_context_selects_developer_api_auth_for_token_query():
    matches = retrieve_context(
        "How should developers authenticate internal API requests with a bearer token?",
        COMPANY_DOCUMENTS,
    )

    assert matches
    assert matches[0]["document"]["id"] == "dev_api_authentication"


def test_retrieve_context_selects_different_documents_for_different_queries():
    leave_matches = retrieve_context(
        "How much paid bereavement leave is allowed?",
        COMPANY_DOCUMENTS,
    )
    security_matches = retrieve_context(
        "How do I report a suspected security incident?",
        COMPANY_DOCUMENTS,
    )
    software_matches = retrieve_context(
        "How do I request access to approved software?",
        COMPANY_DOCUMENTS,
    )

    assert leave_matches[0]["document"]["id"] == "hr_bereavement_leave"
    assert security_matches[0]["document"]["id"] == "security_incident_reporting"
    assert software_matches[0]["document"]["id"] == "ops_software_access"
    assert len(
        {
            leave_matches[0]["document"]["id"],
            security_matches[0]["document"]["id"],
            software_matches[0]["document"]["id"],
        }
    ) == 3


def test_retrieve_context_respects_limit_and_filters_low_scores():
    matches = retrieve_context(
        "customer data retention secure records",
        COMPANY_DOCUMENTS,
        limit=1,
    )

    assert len(matches) == 1
    assert matches[0]["document"]["id"] == "data_retention_policy"

    no_matches = retrieve_context("cafeteria lunch menu soup today", COMPANY_DOCUMENTS)
    assert no_matches == []


def test_format_context_includes_source_metadata_and_content():
    matches = retrieve_context("parental leave policy", COMPANY_DOCUMENTS)
    context = format_context(matches)

    assert "Source ID:" in context
    assert "Title:" in context
    assert "Category:" in context
    assert "Content:" in context
    assert "hr_parental_leave" in context
    assert "Parental Leave Policy" in context


def test_format_context_handles_empty_context():
    context = format_context([])

    assert isinstance(context, str)
    assert "No relevant context" in context or "no relevant context" in context.lower()


def test_build_prompt_has_required_structure_and_boundaries():
    query = "How do I get a development API token?"
    matches = retrieve_context(query, COMPANY_DOCUMENTS)
    prompt = build_prompt(query, matches)

    assert "Instructions:" in prompt
    assert "Context:" in prompt
    assert "Question:" in prompt
    assert "Response requirements:" in prompt
    assert query in prompt
    assert "dev_api_authentication" in prompt
    assert "Use only" in prompt or "use only" in prompt.lower()
    assert "Do not invent" in prompt or "do not invent" in prompt.lower()


def test_source_metadata_returns_only_id_and_title():
    matches = retrieve_context("software access service catalog", COMPANY_DOCUMENTS)
    metadata = source_metadata(matches[0])

    assert metadata == {
        "id": "ops_software_access",
        "title": "Software Access Request Process",
    }
    assert set(metadata.keys()) == {"id", "title"}
