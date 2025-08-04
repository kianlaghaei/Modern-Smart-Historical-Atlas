# Modern Smart Historical Atlas – Backend

## Setup
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Set `OPENAI_API_KEY` in your environment.
4. `uvicorn main:app --reload`

Endpoints:
- `GET /`: Welcome message.
- `GET /atlas`: Returns `atlas.json`.
- `POST /extract`: Accepts raw text and rewrites `atlas.json` with extracted data.
