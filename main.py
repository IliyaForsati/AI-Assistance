from fastapi import FastAPI, Request # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse, JSONResponse # pyright: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates # pyright: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(msg: Message):
    user_msg = msg.message
    reply = f"{user_msg}"
    return JSONResponse({"reply": reply})