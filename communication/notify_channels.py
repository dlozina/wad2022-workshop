from typing import Union, Any

from infobip_channels.sms.channel import SMSChannel
from infobip_channels.core.models import ResponseBase

BASE_URL = "<URL>"
KEY = "<API KEY>"


class NotifyChannels:
    @staticmethod
    def notify_sms(url: str) -> Union[ResponseBase, Any]:
        c = SMSChannel.from_auth_params({
            "base_url": BASE_URL,
            "api_key": KEY
        })
        response = c.send_sms_message(
            {
                "messages": [
                    {
                        "destinations": [
                            {
                                "to": "<MY NUMBER>"
                            }
                        ],
                        "from": "InfoSMS",
                        "text": "Redirected to: " + url
                    }
                ]
            }
        )
        return response
