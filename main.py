from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database

app = FastAPI(title="Atharva AI Receptionist")

database.init_db()


class CallInput(BaseModel):
    call_id: str
    language: str = "en"


class TurnInput(BaseModel):
    speaker: str
    text: str


class RequestInput(BaseModel):
    request_type: str
    description: str


@app.get("/")
def home():
    return {"message": "Atharva Backend is running!"}


@app.post("/calls")
def create_new_call(data: CallInput):
    try:
        database.create_call(data.call_id, data.language)
        return {"message": "Call saved", "call_id": data.call_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/calls/{call_id}/transcripts")
def add_transcript(call_id: str, data: TurnInput):
    try:
        database.save_turn(call_id, data.speaker, data.text)
        return {"message": "Conversation saved"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/calls/{call_id}/requests")
def add_request(call_id: str, data: RequestInput):
    try:
        database.save_request(
            call_id, data.request_type, data.description
        )
        return {"message": "Customer request saved"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/calls")
def list_calls():
    return database.get_calls()


@app.get("/calls/{call_id}/transcripts")
def list_transcripts(call_id: str):
    return database.get_transcripts(call_id)


@app.get("/calls/{call_id}/requests")
def list_requests(call_id: str):
    return database.get_requests(call_id)