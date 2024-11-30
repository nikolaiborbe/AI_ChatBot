import openai
from config import OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY


async def chat(user_message):
    response = openai.chat.completions.create(
        model="gpt-4",
        # Use "gpt-3.5-turbo" if desired
        messages=[
            {"role": "user", "content": "Please keep reponse short, and use twitch emote, and BTTV emote. The response should work as a twitch chat."},
            {"role": "user", "content": "When writing an emote keep a space behind the next character so it will be formatted correctly."},
            {"role": "user", "content": user_message},
        ],
    )
    output = response.choices[0].message.content[:500]
    return output