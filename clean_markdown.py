import re
import sys

def clean_markdown_for_speech(markdown_content):
    # 1. Extract Abstract and Title from YAML front matter.
    abstract_content = ""
    title_content = ""
    yaml_match = re.match(r'---\s*(.*?)\s*---', markdown_content, re.DOTALL)
    if yaml_match:
        yaml_block = yaml_match.group(1)
        abstract_match = re.search(r'abstract:\s*\|(.*?)(?=\n\S|\n---)', yaml_block, re.DOTALL)
        title_match = re.search(r'title:\s*"(.*?)"', yaml_block, re.DOTALL)
        if abstract_match:
            abstract_content = abstract_match.group(1).strip()
        if title_match:
            title_content = title_match.group(1).strip()

    # 2. Remove the entire YAML front matter.
    cleaned_content = re.sub(r'---\s*.*?---', '', markdown_content, flags=re.DOTALL)

    # 3. Remove ::: thebibliography ... :::
    cleaned_content = re.sub(r':::\s+thebibliography.*?:::', '', cleaned_content, flags=re.DOTALL)

    # 4. Remove ::::: tcbraster ... :::::
    cleaned_content = re.sub(r':::::\s+tcbraster.*?:::::', '', cleaned_content, flags=re.DOTALL)

    # 5. Remove <figure ...> ... </figure>
    cleaned_content = re.sub(r'<figure.*?<\/figure>', '', cleaned_content, flags=re.DOTALL)

    # 6. Remove inline math $...$
    cleaned_content = re.sub(r'\$.*?\$', '', cleaned_content)

    # 7. Remove block math $$...$$
    cleaned_content = re.sub(r'\$\$.*?\$\$', '', cleaned_content, flags=re.DOTALL)

    # 8. Remove \[ ... \] math
    cleaned_content = re.sub(r'\\\[.*?\\\]', '', cleaned_content, flags=re.DOTALL)

    # 9. Remove [@...] references
    cleaned_content = re.sub(r'\[@.*?\]', '', cleaned_content)

    # 10. Remove [...](#...) references
    cleaned_content = re.sub(r'\[.*?\]\(#.*?\)\{.*?\}', '', cleaned_content)

    # 11. Remove footnotes [^1]
    cleaned_content = re.sub(r'\[\^.*?\]', '', cleaned_content)

    # 12. Remove footnote definitions at the end
    cleaned_content = re.sub(r'\n\[\^.*?\]:.*', '', cleaned_content)

    # 13. Prepend the extracted Abstract and Title as a new YAML front matter.
    simplified_yaml = "---\n"
    if abstract_content:
        simplified_yaml += f"abstract: |\n  {abstract_content.replace('\n', '\n  ')}\n"
    if title_content:
        simplified_yaml += f"title: \"{title_content}\"\n"
    simplified_yaml += "---\n"

    return simplified_yaml + cleaned_content

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        content = f.read()

    cleaned_content = clean_markdown_for_speech(content)

    with open(output_file, 'w') as f:
        f.write(cleaned_content)
