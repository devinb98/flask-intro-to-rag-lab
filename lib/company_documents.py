"""
Approved company documents for the simplified RAG lab.

The documents are intentionally stored in a Python list so the lab can focus on
retrieval, prompt construction, Flask request handling, and source attribution.
"""

COMPANY_DOCUMENTS = [
    {
        "id": "hr_parental_leave",
        "title": "Parental Leave Policy",
        "category": "human_resources",
        "text": (
            "Full-time employees are eligible for 12 weeks of paid parental leave "
            "after six months of employment. Employees should submit a leave request "
            "through the HR portal at least 30 days before the expected leave start date "
            "when possible."
        ),
        "tags": ["parental", "leave", "family", "benefits", "hr", "full-time"],
    },
    {
        "id": "hr_bereavement_leave",
        "title": "Bereavement Leave Guidelines",
        "category": "human_resources",
        "text": (
            "Employees may take up to five paid business days of bereavement leave "
            "for the loss of an immediate family member. Managers should approve the "
            "request promptly and may coordinate with HR for additional support."
        ),
        "tags": ["bereavement", "leave", "family", "manager", "hr", "paid"],
    },
    {
        "id": "finance_travel_reimbursement",
        "title": "Travel Reimbursement Procedure",
        "category": "finance",
        "text": (
            "Employees must submit travel reimbursement requests within 14 days of "
            "returning from approved business travel. Requests must include itemized "
            "receipts, business purpose, travel dates, and manager approval."
        ),
        "tags": ["travel", "reimbursement", "receipts", "finance", "approval", "expenses"],
    },
    {
        "id": "ops_software_access",
        "title": "Software Access Request Process",
        "category": "operations",
        "text": (
            "Employees who need access to approved software should submit a request "
            "through the service catalog. The request must include the software name, "
            "business reason, department, and manager approval. Most approved requests "
            "are processed within three business days."
        ),
        "tags": ["software", "access", "service", "catalog", "approval", "tools"],
    },
    {
        "id": "security_incident_reporting",
        "title": "Security Incident Reporting Procedure",
        "category": "security",
        "text": (
            "Employees must report suspected security incidents immediately using the "
            "security incident form or the emergency security hotline. Do not delete "
            "evidence, forward suspicious files, or attempt independent investigation "
            "unless instructed by the security team."
        ),
        "tags": ["security", "incident", "report", "phishing", "evidence", "hotline"],
    },
    {
        "id": "dev_api_authentication",
        "title": "Internal API Authentication Guide",
        "category": "developer_docs",
        "text": (
            "Internal API requests must include a bearer token in the Authorization "
            "header. Developers can create a development token from the internal "
            "developer portal. Production tokens require team lead approval and must "
            "not be stored in source control."
        ),
        "tags": ["api", "authentication", "authorization", "token", "bearer", "developer"],
    },
    {
        "id": "data_retention_policy",
        "title": "Customer Data Retention Policy",
        "category": "data_governance",
        "text": (
            "Customer support records are retained for three years unless a legal hold "
            "requires a longer retention period. Exported customer data must be stored "
            "only in approved secure locations and deleted when the business need ends."
        ),
        "tags": ["data", "retention", "customer", "records", "secure", "governance"],
    },
]
