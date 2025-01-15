from http import HTTPStatus

import requests_mock
from django.test import SimpleTestCase


class BotTests(SimpleTestCase):
    def setUp(self):
        self.mock_requests = self.enterContext(requests_mock.Mocker())

    def test_incorrect_content_type(self):
        response = self.client.post(
            "/bot/",
            content_type="text/plain",
        )
        assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    def test_post_non_dict(self):
        response = self.client.post(
            "/bot/",
            content_type="application/json",
            data=[],
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_post_empty_dict(self):
        response = self.client.post(
            "/bot/",
            content_type="application/json",
            data={},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_post_message(self):
        self.mock_requests.post(
            "http://localhost:50096/v3/conversations/19%3Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa%40thread.tacv2%3Bmessageid%3D1111111111111/activities/bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
        )
        # Data based on a payload captured from Bot Framework Emulator
        payload = {
            "text": "Hi!",
            "textFormat": "plain",
            "type": "message",
            "channelId": "msteams",
            "from": {
                "id": "82d12900-783f-496d-9449-43dcd216666a",
                "name": "User",
                "role": "user",
            },
            "localTimestamp": "2024-09-04T12:05:50+01:00",
            "localTimezone": "Europe/London",
            "timestamp": "2024-09-04T12:05:50.281Z",
            "channelData": {
                "channel": {
                    "id": "19:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@thread.tacv2",
                },
            },
            "conversation": {
                "id": "19:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@thread.tacv2;messageid=1111111111111",
            },
            "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "recipient": {
                "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
                "name": "Bot",
                "role": "bot",
            },
            "serviceUrl": "http://localhost:50096",
        }

        response = self.client.post(
            "/bot/",
            content_type="application/json",
            data=payload,
        )

        assert response.status_code == HTTPStatus.OK
        assert len(self.mock_requests.request_history) == 1
        data = self.mock_requests.request_history[0].json()
        assert data["type"] == "message"
        assert data["text"] == "Beep boop 🤖"
