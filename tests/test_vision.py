from vision.engine import DocumentVisionEngine

def test_doc_vision():
    e = DocumentVisionEngine()
    res = e.extract_invoice_fields([{"text": "INV-999"}, {"text": "$500.00"}])
    assert res["invoice_number"] == "INV-999"
