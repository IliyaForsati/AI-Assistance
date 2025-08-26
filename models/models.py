
from pydantic import BaseModel # pyright: ignore[reportMissingImports]

class Prompt(BaseModel):
    message: str