from pathlib import Path

from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine, select, delete

from models import AtlasDB, Location, Person, Writing, Event
from llm_utils import extract_atlas

DATA_PATH = Path("data/atlas.json")
DB_PATH = Path("data/atlas.db")
engine = create_engine(f"sqlite:///{DB_PATH}")
app = FastAPI(title="Modern Smart Historical Atlas")


@app.on_event("startup")
def on_startup():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        has_data = session.exec(select(Location)).first() is not None
        if not has_data and DATA_PATH.exists():
            atlas = AtlasDB.model_validate_json(DATA_PATH.read_text("utf-8"))
            session.add_all(atlas.locations)
            session.add_all(atlas.people)
            session.add_all(atlas.writings)
            session.add_all(atlas.events)
            session.commit()


@app.get("/", tags=["info"])
def root():
    return {"message": "Welcome to the Modern Smart Historical Atlas API!"}


@app.get("/atlas", response_model=AtlasDB, tags=["atlas"])
def get_atlas():
    with Session(engine) as session:
        return AtlasDB(
            locations=session.exec(select(Location)).all(),
            people=session.exec(select(Person)).all(),
            writings=session.exec(select(Writing)).all(),
            events=session.exec(select(Event)).all(),
        )


@app.post("/extract", response_model=AtlasDB, tags=["atlas"])
def post_extract(text: str):
    atlas = extract_atlas(text)
    with Session(engine) as session:
        session.exec(delete(Location))
        session.exec(delete(Person))
        session.exec(delete(Writing))
        session.exec(delete(Event))
        session.add_all(atlas.locations)
        session.add_all(atlas.people)
        session.add_all(atlas.writings)
        session.add_all(atlas.events)
        session.commit()
    return atlas
