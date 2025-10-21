from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .chatgpt import get_client


class TranslateRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


class TranslateResponse(BaseModel):
    translated_text: str


class CorrectionRequest(BaseModel):
    text: str
    language: str


class CorrectionResponse(BaseModel):
    corrected_text: str


app = FastAPI(title="Easy Translator", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_index_path = Path(__file__).parent / "static" / "index.html"


@app.get("/", response_class=HTMLResponse)
async def read_root() -> str:
    return _index_path.read_text(encoding="utf-8")


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest) -> TranslateResponse:
    try:
        client = get_client()
        translated = client.translate(request.text, request.source_language, request.target_language)
    except Exception as exc:  # pragma: no cover - passthrough to HTTP error
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return TranslateResponse(translated_text=translated)


@app.post("/api/correct", response_model=CorrectionResponse)
async def correct(request: CorrectionRequest) -> CorrectionResponse:
    try:
        client = get_client()
        corrected = client.correct(request.text, request.language)
    except Exception as exc:  # pragma: no cover - passthrough to HTTP error
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return CorrectionResponse(corrected_text=corrected)
