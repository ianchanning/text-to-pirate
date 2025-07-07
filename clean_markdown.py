import re
import sys

def clean_markdown_for_speech(markdown_content):
    # 1. Annihilate URLs: [text](url) -> text
    cleaned_content = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', markdown_content)

    # 2. Image Alt-Text Extraction: ![alt text](image.png) -> alt text
    cleaned_content = re.sub(r'!\[(.*?)\]\((.*?)\)', r'\1', cleaned_content)

    # 3. HTML Tag Purge
    cleaned_content = re.sub(r'<.*?>', '', cleaned_content)

    # 4. Code Block Substitution
    cleaned_content = re.sub(r'```.*?```', 'a code snippet follows', cleaned_content, flags=re.DOTALL)

    # 5. Strip Structural Markers (Headings, Lists)
    cleaned_content = re.sub(r'^#+\s*', '', cleaned_content, flags=re.MULTILINE)
    cleaned_content = re.sub(r'^\*\s*', '', cleaned_content, flags=re.MULTILINE)
    cleaned_content = re.sub(r'^-\s*', '', cleaned_content, flags=re.MULTILINE)

    return cleaned_content

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        content = f.read()

    cleaned_content = clean_markdown_for_speech(content)

    with open(output_file, 'w') as f:
        f.write(cleaned_content)