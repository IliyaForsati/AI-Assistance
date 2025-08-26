# library imports
from fastapi import FastAPI, Request, HTTPException # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse, JSONResponse # pyright: ignore[reportMissingImports]
from fastapi.templating import Jinja2Templates # pyright: ignore[reportMissingImports]


# local imports
from models.models import Prompt
from ai_services import phi3

# Fast Api setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# APIs
@app.get("/", response_class=HTMLResponse)
def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(msg: Prompt):
    return phi3.ask(msg=msg)
