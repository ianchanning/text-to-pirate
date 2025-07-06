# Text-to-Pirate

This project converts text to speech using OpenAI's TTS models, specifically tailored to generate pirate-style speech for any markdown blog post you feed it.

## Quick Start

```bash
pip install uv  # If you don't have uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key_here" # Replace with your actual key
cat your_blog_post.md | head -n 5 | ./main.py --stream
```

## Setup

We use `uv` by default, but `pip` has been tested too.

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
    The project requires your OpenAI API key. Set it as an environment variable:
    ```bash
    export OPENAI_API_KEY="your_api_key_here"
    ```

## Usage

Before running `main.py`, ensure your virtual environment is activated in each new bash session:

```bash
source .venv/bin/activate
```

Once activated, you can convert text to speech by running the `main.py` script. It can accept input from a file or directly from `stdin` (piped text). You can choose to stream the audio or save it to a file.

### Input from File

#### Save to File

```bash
./main.py your_text_file.txt
```

#### Stream Audio

```bash
./main.py your_text_file.txt --stream
```

### Input from Piped Text (stdin)

#### Stream Audio (e.g., first 5 lines of a file)

```bash
cat your_text_file.txt | head -n 5 | ./main.py --stream
```

#### Save to File (e.g., entire file)

```bash
cat your_text_file.txt | ./main.py
```

This will generate an MP3 file in the `out/` directory. The filename follows the pattern: `[voice]_[instructor]_[first_four_words_of_input]_[timestamp].mp3`.

Currently, the hardcoded voice is `nova` (from `reasonable_voices[2]`) and the instructor is `pirate`.

## Configuration

- **Voices and Instructors:** The `main.py` script contains predefined `reasonable_voices` and `instructors` (pirate, mad_scientist, emo_teenager). You can modify these lists and the `voice_selection` and `instructor_selection` variables in `main.py` to experiment with different outputs.

## Testing

This project includes end-to-end test scripts to verify the installation and basic functionality using both `pip` and `uv`.

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
