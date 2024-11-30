import twitchio
from twitchio.ext import commands
from ai import *
from config import TWITCH_TOKEN, OPEN_AI_KEY, CHANNEL
import colorama
import pygame
import os
import time
import requests
import json
import random

openai.api_key = OPEN_AI_KEY
colorama.init(autoreset=True)
voices = ["fable", "onyx", "nova"]
chatters = {
}  # if you have returning viewers that should have the same voice each time
# https://platform.openai.com/docs/guides/text-to-speech


def create_voice_file(text, model="tts-1", voice="alloy", filepath="output.mp3"):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json",
    }
    data = {"model": model, "input": f"{text}", "voice": voice}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)


def play_audio_file(filepath="output.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    os.remove(filepath)


class TwitchBot(commands.Bot):

    def __init__(self, token, channel):
        super().__init__(token=token, prefix="!", initial_channels=[channel])

    @commands.command(name="chat")
    async def chat(self, ctx: commands.Context):
        filepath = "output.mp3"

        user = ctx.author.name


        if ctx.message.content[0] == "!":
            user_message = ctx.message.content[len("!chat ") :].strip()
        else:
            user_message = ""

        new_user_message = f"{colorama.Fore.RED}{user}: {colorama.Fore.WHITE}{user_message}"
        print(new_user_message)
        if user in chatters:
            voice = chatters[user]
            create_voice_file(new_user_message, voice=voice, filepath=filepath)
        else:
            voice = random.choice(voices)
            chatters[user] = voice
            text = f"Hi my name is: {user}. {user_message}"
            create_voice_file(text, voice=voice, filepath=filepath)

        play_audio_file(filepath)

        ai_response = await chat(user_message)
        ai_response_message = (
            f"{colorama.Fore.RED}ChatBOT: {colorama.Fore.WHITE}{ai_response}"
        )
        await ctx.send(f"{ai_response}")
        print(ai_response_message)
        create_voice_file(ai_response, voice="shimmer", filepath=filepath)
        play_audio_file(filepath)



print("Twitch bot is running")
if __name__ == "__main__":
    bot = TwitchBot(token=TWITCH_TOKEN, channel=CHANNEL)
    bot.run()
