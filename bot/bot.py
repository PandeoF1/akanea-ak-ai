# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import requests

API_URL = "http://10.14.1.5:3000/api/v1/prediction/d0b3e77f-d39e-47c2-b2d9-df155e745e56"


def query_ai(question: str):
    response = requests.post(
        API_URL,
        json={
            "question": question,
        },
    )
    return response.json()


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        response = query_ai(turn_context.activity.text.strip())
        print(response)
        await turn_context.send_activity(response.get("text"))

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                response = query_ai("Bonjour")
                print(response)
                await turn_context.send_activity(response.get("text"))
