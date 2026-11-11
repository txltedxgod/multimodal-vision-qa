from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from vision.engine import DocumentVisionEngine

app = FastAPI(title="Multimodal Vision QA", version="0.1.0")
engine = DocumentVisionEngine()


class OCRReq(BaseModel):
    boxes: list[dict[str, Any]] = Field(default_factory=list)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/parse-document")
def parse_doc(req: OCRReq) -> dict[str, Any]:
    return engine.extract_invoice_fields(req.boxes)
