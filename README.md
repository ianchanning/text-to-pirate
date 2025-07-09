# PROJECT CHIMERA: Text-to-Pirate

## Mission: Make the Words Speak

The endless scroll is a curse. We're drowning in text. This is the forge where we give words a voice—a pirate's growl, a mad scientist's cackle, an emo teen's lament. Feed it any text, and let it speak. No more reading. Only listening.

## Quick Start

For those who can't wait to hear the chaos:

```bash
pip install uv  # If you don't have uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key_here" # Replace with your actual key
cat your_blog_post.md | head -n 5 | ./main.py
```

## Setup

Every proper lab needs its foundations. We favour the speed of `uv`, but the old ways of `pip` work too.

1.  **Install `uv`:**
    If you don't have `uv` installed, you can install it using pip:

    ```bash
    pip install uv
    ```

2.  **Create and Activate Virtual Environment:**

    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    uv pip install -r requirements.txt
    ```

4.  **Set OpenAI API Key:**
    The machine needs its fuel. Set your OpenAI API key as an environment variable:
    ```bash
    export OPENAI_API_KEY="your_api_key_here"
    ```

## (⊕) Invoking the Machine

Before you can invoke the machine, you must awaken the environment in each new terminal session. It's a crucial step, lest you be cast into the digital abyss.

```bash
source .venv/bin/activate
```

Once the environment is alive, you can command the script to transmute text into speech. It drinks from files or directly from the ether (`stdin`). You can stream the audio live or bottle it in a file.

### Input from File

#### Stream Audio

```bash
./main.py your_text_file.txt
```

#### Save to File

```bash
./main.py your_text_file.txt --save
```

### Input from Piped Text (stdin)

#### Stream Audio (e.g., first 5 lines of a file)

```bash
cat your_text_file.txt | head -n 5 | ./main.py
```

#### Save to File (e.g., entire file)

```bash
cat your_text_file.txt | ./main.py --save
```

This will generate an MP3 file in the `out/` directory. The filename follows the pattern: `[voice]_[instructor]_[first_four_words_of_input]_[timestamp].mp3`.

The default voice is `nova` and the default instructor is `pirate`.

### Optional Parameters

You can customize the voice and instructor persona using the `--voice` and `--instructor` flags.

- `--voice`: Specifies the voice to use.
  Available voices: `ballad`, `coral`, `nova`, `sage`.
  Example: `--voice coral`

- `--instructor`: Specifies the instructor persona.
  Available instructors: `pirate`, `mad_scientist`, `emo_teenager`.
  Example: `--instructor mad_scientist`

#### Example Usage with Optional Parameters

```bash
./main.py your_text_file.txt --voice ballad --instructor mad_scientist
cat your_text_file.txt | head -n 5 | ./main.py --voice nova --instructor emo_teenager
```

## Configuration

The core of the machine is yours to tinker with. The `main.py` script holds the lists of `reasonable_voices` and `instructors`. Bend them to your will. Add new personalities. Experiment.

## (⇌) The Cleansing Ritual: `clean_markdown.py`

Raw text is messy. It's full of digital detritus—links, tags, and other junk not meant for the spoken word. To ensure a clean transmutation, we first pass the text through a cleansing ritual. This script strips the noise, leaving only the pure essence of the message.

### How it Works

The script performs the following cleaning operations:

1.  **Removes URLs:** It strips out the URL part of a markdown link, leaving only the descriptive text. For example, `[Google](https://google.com)` becomes `Google`.
2.  **Extracts Image Alt Text:** It takes the alt text from an image link and uses that as the spoken text. For example, `![A picture of a cat](cat.jpg)` becomes `A picture of a cat`.
3.  **Strips HTML Tags:** All HTML tags are removed.
4.  **Handles Code Blocks:** It replaces entire code blocks with the phrase "a code snippet follows" to avoid reading code aloud.
5.  **Removes Structural Markers:** It removes heading markers (`#`), and list markers (`*`, `-`) from the start of lines.

### Example Usage

Pipe your markdown file through the cleaner before sending it to the main script:

```bash
cat your_blog_post.md | ./clean_markdown.py | ./main.py
```

## Testing the Contraption

A mad scientist's creation must be robust. These tests ensure the machine is calibrated and ready to roar. Run them to verify that both `pip` and `uv` installations can withstand the pressure.

To run the tests:

1.  **Ensure you are in the project root directory.**

2.  **Run the `pip` installation test:**

    ```bash
    ./tests/test_pip_install.sh
    ```

3.  **Run the `uv` installation test:**
    ```bash
    ./tests/test_uv_install.sh
    ```

These tests will create temporary directories, simulate a fresh installation, and check if the `main.py` script successfully generates an output file.