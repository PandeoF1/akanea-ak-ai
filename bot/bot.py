# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, CardFactory, MessageFactory
from botbuilder.schema import ChannelAccount
from botbuilder.schema import HeroCard, CardImage, CardAction, ActionTypes, Attachment
import requests
import json

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

    def create_hero_card(
        self,
        name: str,
        image_url: str,
        email: str,
        position: str,
    ) -> Attachment:
        card = HeroCard(
            title=name,
            subtitle=position,
            images=[
                CardImage(
                    url=(
                        image_url
                        if image_url
                        else "https://www.francetravail.fr/files/live/sites/PE/files/secteurs-metiers/commerce-vente/Commercial-850x523.jpg"
                    )
                )
            ],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Profil",
                    value="https://www.linkedin.com/in/johndoe",
                )
            ],
        )
        return CardFactory.hero_card(card)

    async def on_message_activity(self, turn_context: TurnContext):
        response = query_ai(turn_context.activity.text.strip()).get("text")
        print(response)
        text = response.split("---")
        await turn_context.send_activity(text[0])

        if len(text) > 1:
            command = json.loads(text[1].strip().rstrip())
            if command.get("type") == "person":
                card = self.create_hero_card(
                    name=command.get("name"),
                    image_url=command.get("imageUrl"),
                    email=command.get("email"),
                    position=command.get("poste"),
                )
                await turn_context.send_activity(MessageFactory.attachment(card))

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                response = query_ai("Bonjour")
                print(response)
                await turn_context.send_activity(response.get("text"))
