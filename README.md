# Text-to-Speech Project

This project converts text to speech using OpenAI's TTS models.

## Setup

To set up the development environment, follow these steps:

1.  **Install `uv`:**
    If you don't have `uv` installed, you can install it using pip:

    ```bash
    pip install uv
    ```

    Or, for a more robust installation, refer to the official `uv` documentation.

2.  **Create and Activate Virtual Environment:**

    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## Usage

Before running `main.py`, ensure your virtual environment is activated in each new bash session:

```bash
source .venv/bin/activate
```

Once activated, you can convert text to speech by running the `main.py` script with the path to your input text file. You can choose to stream the audio or save it to a file.

### Stream Audio

```bash
./main.py your_text_file.txt --stream
```

This will stream the audio directly to your speakers.

### Save to File

```bash
./main.py your_text_file.txt
```

This will generate an MP3 file in the `out/` directory. The filename follows the pattern: `[voice]_[instructor]_[first_four_words_of_input]_[timestamp].mp3`.

Currently, the hardcoded voice is `nova` (from `reasonable_voices[2]`) and the instructor is `pirate`.

## Configuration

- **Voices and Instructors:** The `main.py` script contains predefined `reasonable_voices` and `instructors` (pirate, mad_scientist, emo_teenager). You can modify these lists and the `voice_selection` and `instructor_selection` variables in `main.py` to experiment with different outputs.
