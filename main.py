from fastapi import FastAPI

import databases
import sqlalchemy
import short_url

from models.url import UrlIn
from models.target_url import TargetUrlIn

BASE_URL = "http://localhost:8000/"
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

target_url_database = sqlalchemy.Table(
    "target_url_database",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("url", sqlalchemy.String),
    sqlalchemy.Column("send_sms", sqlalchemy.Boolean),
    sqlalchemy.Column("send_whatsapp", sqlalchemy.Boolean),
    sqlalchemy.Column("send_email", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

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
async def redirect_to_url(url_part: str):
    db_id = short_url.decode_url(url_part)
    query = url_database.select().where(url_database.c.id == db_id)
    return await database.fetch_all(query)


@app.post("/add-target-url")
async def shorten(url_parameter: TargetUrlIn):
    query = url_database.insert().values(
        url=url_parameter.url,
        send_sms=url_parameter.send_sms,
        send_whatsapp=url_parameter.send_whatsapp,
        send_email=url_parameter.send_email,
    )
    last_record_id = await database.execute(query)
    shorted_url = short_url.encode_url(last_record_id)
    return {"id": last_record_id, "shortUrl": BASE_URL + shorted_url}

