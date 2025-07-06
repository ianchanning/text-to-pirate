from bs4 import BeautifulSoup
import re
import sys

def clean_html_for_speech(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove bibliography/references section
    for div in soup.find_all('div', class_='thebibliography'):
        div.decompose()
    for div in soup.find_all('div', id=re.compile(r'^refs')):
        div.decompose()

    # Remove figures and figcaptions
    for figure in soup.find_all('figure'):
        figure.decompose()
    for figcaption in soup.find_all('figcaption'):
        figcaption.decompose()

    # Remove algorithms (pandoc often puts them in div with class algorithm or similar)
    for div in soup.find_all('div', class_='algorithm'):
        div.decompose()
    for div in soup.find_all('div', class_='algorithmic'):
        div.decompose()

    # Remove pandoc-specific divs and spans that contain math or other unwanted elements
    # Keep <span class="math inline"> elements
    for div in soup.find_all('div', class_='math'): # This targets div.math (block math)
        div.decompose()
    for span in soup.find_all('span', class_='math-display'): # This targets span.math-display
        span.decompose()
    for span in soup.find_all('span', class_='math-block'): # This targets span.math-block
        span.decompose()
    for div in soup.find_all('div', class_='math-block'): # This targets div.math-block
        div.decompose()
    # Explicitly target elements with BOTH 'display' and 'math' classes
    for div in soup.find_all('div', class_='display math'):
        div.decompose()
    for span in soup.find_all('span', class_='display math'):
        span.decompose()

    # Remove pandoc-generated citation placeholders
    for span in soup.find_all('span', class_='citation'):
        span.decompose()

    # Remove pandoc-specific div wrappers like title-block-header, abstract, tcbraster, tcolorbox
    for div_id in ['title-block-header']:
        div = soup.find('div', id=div_id)
        if div: div.decompose()
    for div_class in ['abstract', 'abstract-title', 'tcbraster', 'tcolorbox']:
        for div in soup.find_all('div', class_=div_class):
            div.decompose()

    # Remove any img tags that might be rendered math (pandoc sometimes does this)
    for img in soup.find_all('img', src=re.compile(r'^data:image')):
        img.decompose()

    # Remove any links that are clearly just references (e.g., internal links to sections)
    # This is a bit more aggressive, might need fine-tuning
    for a_tag in soup.find_all('a'):
        if a_tag.get('href') and (
            a_tag['href'].startswith('#') or 
            '@' in a_tag.get_text() or 
            a_tag.get_text().strip().isdigit()
        ):
            a_tag.decompose()

    # Remove any remaining script or style tags
    for script in soup.find_all('script'):
        script.decompose()
    for style in soup.find_all('style'):
        style.decompose()

    # Remove any empty paragraphs or divs that might be left behind
    for p in soup.find_all('p'):
        if not p.get_text(strip=True):
            p.decompose()
    for div in soup.find_all('div'):
        if not div.get_text(strip=True) and not div.find_all(): # Only remove if truly empty of text and children
            div.decompose()

    return str(soup)

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned_content = clean_html_for_speech(content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)