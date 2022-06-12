from fastapi import FastAPI, Path
from pydantic import BaseModel

import databases
import sqlalchemy

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

url_database = sqlalchemy.Table(
    "url_database",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("url", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class UrlIn(BaseModel):
    url: str


class Url(BaseModel):
    id: int
    url: str


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/shorten", response_model=Url)
async def shorten(url_parameter: UrlIn):
    query = url_database.insert().values(url=url_parameter.url)
    last_record_id = await database.execute(query)
    return {**url_parameter.dict(), "id": last_record_id}


@app.get("/{short_url}")
async def short_url(
    short_url: str = Path(title="Short URL Link"),
):
    results = {"short_url": short_url}
    return results


@app.post("/add-target-url")
async def shorten(url: Url):
    return url
