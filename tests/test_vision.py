from fastapi.testclient import TestClient

from vision.api import app
from vision.engine import DocumentVisionEngine

client = TestClient(app)


def test_doc_vision() -> None:
    e = DocumentVisionEngine()
    res = e.extract_invoice_fields([{"text": "INV-999"}, {"text": "$500.00"}])
    assert res["invoice_number"] == "INV-999"
    assert res["total_amount"] == "$500.00"
    assert res["status"] == "PARSED_SUCCESSFULLY"


def test_doc_vision_partial_and_missing_fields_not_fabricated() -> None:
    e = DocumentVisionEngine()
    missing = e.extract_invoice_fields([{"text": "unrelated receipt text"}])
    assert missing == {
        "invoice_number": None,
        "total_amount": None,
        "status": "FIELDS_NOT_FOUND",
    }

    partial = e.extract_invoice_fields([{"text": "INV-2026-10"}])
    assert partial["invoice_number"] == "INV-2026-10"
    assert partial["total_amount"] is None
    assert partial["status"] == "PARTIAL"


def test_vision_api_endpoints() -> None:
    assert client.get("/health").json() == {"status": "ok"}

    ok = client.post(
        "/api/v1/parse-document",
        json={"boxes": [{"text": "  INV-42  "}, {"text": "  199.00 EUR "}]},
    )
    assert ok.status_code == 200
    assert ok.json() == {
        "invoice_number": "INV-42",
        "total_amount": "199.00 EUR",
        "status": "PARSED_SUCCESSFULLY",
    }

    empty = client.post("/api/v1/parse-document", json={"boxes": []})
    assert empty.status_code == 200
    assert empty.json()["status"] == "FIELDS_NOT_FOUND"
