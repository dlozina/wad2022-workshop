from pydantic import BaseModel


class TargetUrlIn(BaseModel):
    url: str
    send_sms: bool
    send_whatsapp: bool
    send_email: bool


class TargetUrl(BaseModel):
    id: int
    url: str
    send_sms: bool
    send_whatsapp: bool
    send_email: bool
