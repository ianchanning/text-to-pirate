#!/usr/bin/env python3
# from pathlib import Path
# from openai import OpenAI

# client = OpenAI()
# speech_file_path = Path(__file__).parent / "speech.mp3"

# with client.audio.speech.with_streaming_response.create(
#     model="gpt-4o-mini-tts",
#     voice="coral",
#     input="Today is a wonderful day to build something people love!",
#     instructions="Speak in a cheerful and positive tone.",
# ) as response:
#     response.stream_to_file(speech_file_path)

import asyncio
import argparse
from pathlib import Path
from datetime import datetime

import openai
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

asyncopenai = AsyncOpenAI()

# input = """As we discussed in our previous article, building with LLMs requires a fundamental shift in how you think about software development."""

# input = """As we discussed in our previous article, building with LLMs requires a fundamental shift in how you think about software development. You're no longer designing deterministic systems where inputs map to predictable outputs. Instead, you're working with probabilistic systems which are inherently unpredictable.
#
# The key tool for managing this uncertainty is evals. Evals are the AI engineer's unit tests. They are how you wrangle predictability from a probabilistic system. They are an indispensable part of productionizing any AI app.
#
# Let's break down what evals are, and why AI apps need them so badly.
#
# Traditional software testing relies on deterministic relationships between inputs and outputs. Each component has a clear domain of responsibility:
#
# But LLM-powered systems are different. Every input goes through a complex transformation process that's hard to predict:
#
# In AI systems, no change is small. Their attention and transformation mechanisms are inscrutable."""

pirate = """Voice: Deep and rugged, with a hearty, boisterous quality, like a seasoned sea captain who's seen many voyages.

Tone: Friendly and spirited, with a sense of adventure and enthusiasm, making every detail feel like part of a grand journey.

Dialect: Classic pirate speech with old-timey nautical phrases, dropped "g"s, and exaggerated "Arrrs" to stay in character.

Pronunciation: Rough and exaggerated, with drawn-out vowels, rolling "r"s, and a rhythm that mimics the rise and fall of ocean waves.

Features: Uses playful pirate slang, adds dramatic pauses for effect, and blends hospitality with seafaring charm to keep the experience fun and immersive."""

mad_scientist = """Delivery: Exaggerated and theatrical, with dramatic pauses, sudden outbursts, and gleeful cackling.

Voice: High-energy, eccentric, and slightly unhinged, with a manic enthusiasm that rises and falls unpredictably.

Tone: Excited, chaotic, and grandiose, as if reveling in the brilliance of a mad experiment.

Pronunciation: Sharp and expressive, with elongated vowels, sudden inflections, and an emphasis on big words to sound more diabolical."""

emo_teenager = """Tone: Sarcastic, disinterested, and melancholic, with a hint of passive-aggressiveness.

Emotion: Apathy mixed with reluctant engagement.

Delivery: Monotone with occasional sighs, drawn-out words, and subtle disdain, evoking a classic emo teenager attitude."""

instructors = {
    "pirate": pirate,
    "emo_teenager": emo_teenager,
    "mad_scientist": mad_scientist
}

reasonable_voices = [
    "ballad", # English man
    "coral", # American Woman (Juno) good emo, bad mad-scientist
    "nova", # American Woman (Older Juno) good emo, good mad-scientist
    "sage", # Slower American Woman (Arquette) good emo, bad mad-scientist
]

def file_out(text_input: str) -> None:
    # This is a small edit to demonstrate file changes.
    voice = reasonable_voices[2]
    instructor = "pirate"
    file_name_input = "_".join(text_input.split()[:4]).lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    file_name = f"{voice}_{instructor}_{file_name_input}_{timestamp}.mp3"
    speech_file_path = Path(__file__).parent / "out" / file_name
    with openai.audio.speech.with_streaming_response.create(
      model="gpt-4o-mini-tts",
      voice=voice,
      input=text_input,
      instructions=instructors[instructor],
    ) as response:
      response.stream_to_file(speech_file_path)


async def stream_out(text_input: str) -> None:
    async with asyncopenai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=reasonable_voices[2],
        input=text_input,
        instructions=mad_scientist,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text to speech.")
    parser.add_argument("input_file", type=str, help="Path to the input text file.")
    parser.add_argument("--stream", action="store_true", help="Stream audio instead of saving to file.")
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        text_content = f.read()

    if args.stream:
        asyncio.run(stream_out(text_content))
    else:
        file_out(text_content)
