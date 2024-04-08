import os
from json import dumps
from httplib2 import Http
from dotenv import load_dotenv
from urllib3 import Retry


def message_card(resource_id, current_date):
    text = resource_id
    print(resource_id)
    print(current_date)
    revisit = {
        "header": f"Revisit - {str(current_date)}",
        "widgets": [
            {
                "textParagraph": {
                    "text": text,
                }
            }
        ],
    }


# alert to revisit instance


def send_revisit_alert(current_date, revisit_resource, no_of_stopped_volume):
    text = "\n\n".join(f"{k}: {v}" for k, v in revisit_resource.items())
    bot_message = {
        "cards": [
            {
                "header": {"title": "Azure Resource"},
                "sections": [
                    {
                        "header": f"Revisit - {str(current_date)}",
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": text,
                                }
                            }
                        ],
                    },
                    {
                        "header": "Volumes not in use",
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": f'Total no of volume: {no_of_stopped_volume}',
                                }
                            }
                        ],
                    },
                ],
            }
        ]
    }
    push_message(bot_message)

# alert for daily report link
def send_daily_report(report_link):
    bot_message = {
        "cards": [{
                "header": {"title": 'Azure report link'},
                "sections": [{
                    "widgets": [{
                    "buttons": [{
                            "textButton": {
                                "text": "OPEN IN AWS",
                                "onClick": {
                                "openLink": {
                                    "url": report_link
                                    }
                                }
                            }
                        }]
                    }]
                }]
            }]
        }

    push_message(bot_message)
 
 
# push alert
def push_message(bot_message):
    load_dotenv()
    webhook_url = os.getenv('WEBHOOK_URL')
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=webhook_url,
        method="POST",
        headers=message_headers,
        body=dumps(bot_message),
    )
