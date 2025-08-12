#!/usr/bin/env python3
import asyncio
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
import threading
import time
import itertools

# (⊕) The Inquisitor: A final, definitive check for environmental purity.
# First, is a virtual environment even active?
virtual_env_path = os.getenv("VIRTUAL_ENV")
if not virtual_env_path:
    print(
        """
Halt, voyager! You're treading in the dangerous global Python lands.
This script craves the sanctuary of a virtual environment.

Please consecrate your terminal session with:

    source .venv/bin/activate

...and then try your command again. Don't make me summon the dependency kraken.
""",
        file=sys.stderr,
    )
    sys.exit(1)

# Second, if a venv is active, are we ACTUALLY USING IT?
# This exposes the dark magic of `pyenv` overriding an active venv.
expected_python_path = os.path.join(virtual_env_path, "bin", "python")
current_python_path = sys.executable
if os.path.realpath(current_python_path) != os.path.realpath(expected_python_path):
    # (⊕) Make the path relative for a cleaner, more portable command.
    relative_python_path = os.path.relpath(expected_python_path)
    print(
        f"""
Halt, voyager! A paradox has been detected!

You have an active virtual environment at:
  {virtual_env_path}

...but you are currently running the script with a DIFFERENT python interpreter:
  {current_python_path}

This is the dark magic of `pyenv` at work, hijacking your session.
To break the curse, you MUST invoke the venv's python by its relative path:

    {relative_python_path} main.py

Trust this path. It is the only way.
""",
        file=sys.stderr,
    )
    sys.exit(1)


import openai
from openai import AsyncOpenAI

# (⇌) Now, let's check for our audio conduit. Even in a venv, one might forget the tools.
try:
    from openai.helpers import LocalAudioPlayer
except ImportError:
    print(
        """

Hold yer horses, matey! To stream the glorious pirate shanties (or, y'know, other voices),
ye need the 'sounddevice' package. The OpenAI library keeps it separate to stay lightweight.

Choose yer weapon and install the necessary extras:

Using pip:
    pip install 'openai[voice_helpers]'
    
Using uv:
    uv pip install 'openai[voice_helpers]'
    
Once that's done, run this script again and we'll make some noise!

""",
        file=sys.stderr,
    )
    sys.exit(1)


# (⊕) A pirate needs their treasure! Check for the API key.
if not os.getenv("OPENAI_API_KEY"):
    print(
        """
Halt, voyager! Ye be missin' yer treasure map!
Set yer OPENAI_API_KEY environment variable before ye set sail.

Example:
    export OPENAI_API_KEY="sk-your-secret-key-here"

Without it, ye'll be adrift!
""",
        file=sys.stderr,
    )
    sys.exit(1)

asyncopenai = AsyncOpenAI()

pirate = """Voice: Deep and rugged, with a hearty, boisterous quality, like a seasoned sea captain who's seen many voyages.

Tone: Friendly and spirited, with a sense of adventure and enthusiasm, making every detail feel like part of a grand journey.

Dialect: Classic pirate speech with old-timey nautical phrases, dropped \"g\"s, and exaggerated \"Arrrs\" to stay in character.

Pronunciation: Rough and exaggerated, with drawn-out vowels, rolling \"r\"s, and a rhythm that mimics the rise and fall of ocean waves.

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
    "mad_scientist": mad_scientist,
}

reasonable_voices = [
    "ballad",  # English man
    "coral",  # American Woman (Juno) good emo, bad mad-scientist, bad pirate
    "nova",  # American Woman (Older Juno) good emo, good mad-scientist, good pirate
    "sage",  # Slower American Woman good emo, bad mad-scientist, bad pirate
]


class Spinner:
    """A simple terminal spinner that runs in a separate thread."""

    def __init__(self, message: str = "Loading...", delay: float = 0.1):
        self.spinner = itertools.cycle(["-", "/", "|", "\\"])
        self.delay = delay
        self.busy = False
        self.spinner_visible = False
        self.message = message
        self.thread = threading.Thread(target=self._run)

    def _run(self):
        while self.busy:
            spinner_char = next(self.spinner)
            sys.stderr.write(f"\r{self.message} {spinner_char}")
            sys.stderr.flush()
            self.spinner_visible = True
            time.sleep(self.delay)

    def start(self):
        self.busy = True
        self.thread.start()

    def stop(self):
        self.busy = False
        self.thread.join()
        if self.spinner_visible:
            # Clear the spinner line
            sys.stderr.write("\r" + " " * (len(self.message) + 2) + "\r")
            sys.stderr.flush()


class BroadcastingAudioStream:
    """
    A wrapper for the OpenAI audio stream that prints a message
    the first time audio data is requested.
    """

    def __init__(self, audio_stream):
        self._audio_stream = audio_stream
        self._broadcasted = False

    async def iter_bytes(self, chunk_size: int = 4096):
        """
        An async generator that yields audio chunks.
        The first time it's called, it prints a message to stderr.
        """
        if not self._broadcasted:
            # The spinner can leave a partial line, so we add a newline
            # to ensure our message starts on a fresh line.
            sys.stderr.write("\n")
            sys.stderr.flush()
            print(
                "(I) Transmission received! Broadcasting the shanty now...",
                file=sys.stderr,
            )
            self._broadcasted = True

        async for chunk in self._audio_stream.iter_bytes(chunk_size=chunk_size):
            yield chunk


def file_out(text_input: str, voice: str, instructor: str) -> None:
    print(
        "(I) Sending a parrot to the OpenAI galleon with your message...",
        file=sys.stderr,
    )
    # This is a small edit to demonstrate file changes.
    file_name_raw = "_".join(text_input.split()[:4]).lower()
    # (⊕) Sanitize the filename to cast out any devilish non-ASCII characters or filesystem fiends.
    sanitized_filename = "".join(
        char for char in file_name_raw if char.isalnum() or char == "_"
    ).strip()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"{voice}_{instructor}_{sanitized_filename}_{timestamp}.mp3"
    speech_file_path = Path(__file__).parent / "out" / file_name

    spinner = Spinner("(I) Brewing the audio grog...")
    spinner.start()
    try:
        with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text_input,
            instructions=instructors[instructor],
        ) as response:
            # (⊕) Manually stream to file to keep our spinner alive.
            with open(speech_file_path, "wb") as f:
                for chunk in response.iter_bytes(chunk_size=4096):
                    f.write(chunk)
    finally:
        spinner.stop()

    # (⊕) Announce the location of our newly plundered treasure.
    print(f"Ahoy! Yer audio treasure be saved at: {os.path.relpath(speech_file_path)}")


async def stream_out(text_input: str, voice: str, instructor: str) -> None:
    print(
        "(I) Sending a parrot to the OpenAI galleon with your message...",
        file=sys.stderr,
    )
    async with asyncopenai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text_input,
        instructions=instructors[instructor],
        response_format="pcm",
    ) as response:
        broadcasting_stream = BroadcastingAudioStream(response)
        await LocalAudioPlayer().play(broadcasting_stream)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text to speech.")
    parser.add_argument(
        "input_file",
        type=str,
        nargs="?",
        help="Path to the input text file. If not provided, reads from stdin.",
    )
    parser.add_argument(
        "--save", action="store_true", help="Save audio to a file instead of streaming."
    )
    parser.add_argument(
        "--voice",
        type=str,
        choices=reasonable_voices,
        default=reasonable_voices[2],  # Default to 'nova'
        help="Specify the voice to use for speech generation.",
    )
    parser.add_argument(
        "--instructor",
        type=str,
        choices=list(instructors.keys()),
        default="pirate",
        help="Specify the instructor persona for speech generation.",
    )
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, "r") as f:
            text_content = f.read()
    else:
        text_content = sys.stdin.read()

    voice_selection = args.voice
    instructor_selection = args.instructor

    if args.save:
        file_out(text_content, voice_selection, instructor_selection)
    else:
        asyncio.run(stream_out(text_content, voice_selection, instructor_selection))
