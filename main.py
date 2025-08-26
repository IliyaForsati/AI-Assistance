from fastapi import FastAPI, Request, HTTPException # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse, JSONResponse # pyright: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates # pyright: ignore[reportMissingImports]
from pydantic import BaseModel # pyright: ignore[reportMissingImports]
import requests # pyright: ignore[reportMissingModuleSource]
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

OLLAMA_HOST = "http://ai:11434/v1/completions"
OLLAMA_API = "/v1/completions"
MAX_TOKENS = 100

class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(msg: Message):
    try:
        user_msg = msg.message
        reply = get_ai_reply(user_msg)

        js_code = extract_js_code(reply)

        return JSONResponse({"reply": reply, "js": js_code})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Some thing went wrong. {str(e)}")

def get_ai_reply(prompt: str, max_tokens: int = MAX_TOKENS) -> str: 
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "max_tokens": max_tokens
    }

    response = requests.post(OLLAMA_HOST, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return data["choices"][0]["text"].strip()

def extract_js_code(ai_response: str) -> str:
    code_blocks = re.findall(r"```(?:javascript|js)?\n([\s\S]*?)```", ai_response)
    if code_blocks:
        return code_blocks[0].strip()
    return ""