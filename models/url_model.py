from pydantic import BaseModel


class UrlIn(BaseModel):
    url: str