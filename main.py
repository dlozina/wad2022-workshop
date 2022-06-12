from fastapi import FastAPI, Path
from pydantic import BaseModel

import databases
import sqlalchemy
import short_url

BASE_URL = "http://localhost:8000/"
# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

url_database = sqlalchemy.Table(
    "url_database_2",
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
    short_url: str


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/shorten")
async def shorten(url_parameter: UrlIn):
    query = url_database.insert().values(
        url=url_parameter.url,
    )
    last_record_id = await database.execute(query)
    shorted_url = short_url.encode_url(last_record_id)
    return {"id": last_record_id, "shortUrl": BASE_URL + shorted_url}


@app.get("/{url_part}")
async def redirect_to_url(url_part):
    query = url_database.select().where(url_database.c.id == 14)
    return await database.fetch_all(query)

