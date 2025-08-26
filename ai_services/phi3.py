#library imports
from fastapi import HTTPException # pyright: ignore[reportMissingImports]
from fastapi.responses import JSONResponse # pyright: ignore[reportMissingImports]
import requests # pyright: ignore[reportMissingModuleSource]
import re

# local imports
from models.models import Prompt

MAX_TOKENS = 100
DOCKER_CONTAINER = "ai"
OLLAMA_HOST = f"http://{DOCKER_CONTAINER}:11434"
OLLAMA_API = "/v1/completions"

def ask(msg: Prompt) -> JSONResponse:
    try:
        user_msg = msg.message
        reply = _get_ai_reply(user_msg)

        js_code = _extract_js_code(reply)

        have_js = False if js_code is None else True

        return JSONResponse({"reply": reply,"haveJs": have_js, "js": js_code})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Some thing went wrong. {str(e)}")

def _get_ai_reply(prompt: str, max_tokens: int = MAX_TOKENS) -> str: 
    payload = {
        "model": "phi3",
        "prompt": prompt,
        "max_tokens": max_tokens
    }

    response = requests.post(OLLAMA_HOST + OLLAMA_API, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return data["choices"][0]["text"].strip()

def _extract_js_code(ai_response: str) -> str:
    code_blocks = re.findall(r"```(?:javascript|js)?\n([\s\S]*?)```", ai_response)
    if code_blocks:
        return code_blocks[0].strip()
    return None