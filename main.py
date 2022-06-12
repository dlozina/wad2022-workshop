from fastapi import FastAPI, Path
from pydantic import BaseModel


class Url(BaseModel):
    name: str


app = FastAPI()


@app.post("/shorten")
async def shorten(url: Url):
    return url


@app.get("/{short_url}")
async def short_url(
    short_url: str = Path(title="Short URL Link"),
):
    results = {"short_url": short_url}
    return results


@app.post("/add-target-url")
async def shorten(url: Url):
    return url
