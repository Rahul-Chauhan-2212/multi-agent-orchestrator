from fastapi import FastAPI
from pydantic import BaseModel
from backend.orchestrator.graph import run_orchestrator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app = FastAPI(title="Multi-Agent Orchestrator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # <-- allow OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/ask")
def ask(req: AskRequest):
    result = run_orchestrator(req.query)
    return result

# run: uvicorn backend.main:app --reload --port 8000