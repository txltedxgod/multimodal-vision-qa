from __future__ import annotations

from typing import Any


class DocumentVisionEngine:
    """Structured field extractor for OCR bounding-box payloads."""

    def extract_invoice_fields(
        self, ocr_boxes: list[dict[str, Any]]
    ) -> dict[str, Any]:
        total_amount: str | None = None
        invoice_number: str | None = None
        for box in ocr_boxes:
            text = str(box.get("text", "")).strip()
            if not text:
                continue
            if invoice_number is None and "INV-" in text:
                invoice_number = text
            if total_amount is None and ("$" in text or "USD" in text or "EUR" in text):
                total_amount = text

        if invoice_number and total_amount:
            extraction_status = "PARSED_SUCCESSFULLY"
        elif invoice_number or total_amount:
            extraction_status = "PARTIAL"
        else:
            extraction_status = "FIELDS_NOT_FOUND"

        return {
            "invoice_number": invoice_number,
            "total_amount": total_amount,
            "status": extraction_status,
        }
