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
    # Read all input from stdin
    content = sys.stdin.read()
    
    # Process the content
    cleaned_content = clean_markdown_for_speech(content)
    
    # Print the result to stdout
    print(cleaned_content)