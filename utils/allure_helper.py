import json

import allure
from allure_commons.types import AttachmentType
from requests import Response


def attach_request(response: Response, request_data: dict | None = None):
    allure.attach(
        body=f"{response.request.method} {response.request.url}",
        name="Request URL",
        attachment_type=AttachmentType.TEXT,
    )

    if request_data:
        allure.attach(
            body=json.dumps(request_data, indent=2, ensure_ascii=False),
            name="Request Body",
            attachment_type=AttachmentType.JSON,
        )


def attach_response(response: Response):
    allure.attach(body=str(response.status_code), name="Response Status Code", attachment_type=AttachmentType.TEXT)

    try:
        body_json = response.json()
        allure.attach(
            body=json.dumps(body_json, indent=2, ensure_ascii=False),
            name="Response Body",
            attachment_type=AttachmentType.JSON,
        )
    except:
        allure.attach(body=response.text, name="Response Body", attachment_type=AttachmentType.TEXT)
