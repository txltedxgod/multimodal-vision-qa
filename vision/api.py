from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from vision.engine import DocumentVisionEngine

app = FastAPI(title="Multimodal Vision QA", version="0.1.0")
engine = DocumentVisionEngine()

class OCRReq(BaseModel):
    boxes: List[Dict[str, Any]]

@app.post("/api/v1/parse-document")
def parse_doc(req: OCRReq):
    return engine.extract_invoice_fields(req.boxes)
