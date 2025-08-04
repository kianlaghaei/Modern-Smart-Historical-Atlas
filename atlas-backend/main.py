from pathlib import Path

from fastapi import FastAPI, HTTPException

from models import AtlasDB
from llm_utils import extract_atlas

DATA_PATH = Path("data/atlas.json")
app = FastAPI(title="Modern Smart Historical Atlas")


@app.on_event("startup")
def ensure_data_file():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        DATA_PATH.write_text(AtlasDB().model_dump_json(indent=2), encoding="utf-8")


@app.get("/", tags=["info"])
def root():
    return {"message": "Welcome to the Modern Smart Historical Atlas API!"}


@app.get("/atlas", response_model=AtlasDB, tags=["atlas"])
def get_atlas():
    try:
        return AtlasDB.model_validate_json(DATA_PATH.read_text("utf-8"))
    except Exception as e:
        raise HTTPException(500, f"Failed to read atlas data: {e}")


@app.post("/extract", response_model=AtlasDB, tags=["atlas"])
def post_extract(text: str):
    atlas = extract_atlas(text)
    DATA_PATH.write_text(atlas.model_dump_json(indent=2), encoding="utf-8")
    return atlas
