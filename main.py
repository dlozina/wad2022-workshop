from typing import List

from fastapi import FastAPI

import databases
import sqlalchemy
import short_url
from fastapi.responses import RedirectResponse

from models.url import UrlIn
from models.target_url import TargetUrlIn, TargetUrl
from communication.notify_channels import NotifyChannels

BASE_URL = "http://localhost:8000/"
# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

url_table = sqlalchemy.Table(
    "url_table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("url", sqlalchemy.String),
)

target_url_table = sqlalchemy.Table(
    "target_url_table",
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


@app.get("/")
async def hi_attendees():
    return {"message": "Welcome to our workshop! Thank you!"}


@app.get("/get-all-target-urls", response_model=List[TargetUrl])
async def get_all_target_urls():
    query = target_url_table.select()
    return await database.fetch_all(query)


@app.post("/shorten")
async def shorten(url_parameter: UrlIn):
    query = url_table.insert().values(
        url=url_parameter.url,
    )
    last_record_id = await database.execute(query)
    shorted_url = short_url.encode_url(last_record_id)

    query = target_url_table.select()
    db_entity_list = await database.fetch_all(query)
    for db_entity in db_entity_list:
        if db_entity['url'] == url_parameter.url:
            is_target_url = True
            break
        else:
            is_target_url = False

    return {
        "id": last_record_id,
        "longUrl": url_parameter.url,
        "shortUrl": BASE_URL + shorted_url,
        "isTargetUrl": is_target_url
    }


@app.get("/{url_part}")
async def redirect_to_url(url_part: str):
    db_id = short_url.decode_url(url_part)

    query = url_table.select().where(url_table.c.id == db_id)
    db_entity_list = await database.fetch_all(query)
    for db_entity in db_entity_list:
        result = db_entity['url']

    # NotifyChannels().notify_sms(result)

    return RedirectResponse("https://" + result)


@app.post("/add-target-url")
async def add_target_url(url_parameter: TargetUrlIn):
    query = target_url_table.insert().values(
        url=url_parameter.url,
        send_sms=url_parameter.send_sms,
        send_whatsapp=url_parameter.send_whatsapp,
        send_email=url_parameter.send_email,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "url": url_parameter.url}

