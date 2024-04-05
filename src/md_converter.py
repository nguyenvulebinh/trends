import sys
from src.tools.content_handling import translate_text, summarize_text
import glob
import traceback
import os

def load_md_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        md_file = file.read()
    
    layout = None
    layout_title = None
    date = None
    categories = None
    
    title, link = None, None
    image = None
    content = ""

    for line in md_file.split('\n'):
        if line.strip().startswith('---'):
            continue
        elif line.strip().startswith('layout:'):
            layout = ' '.join(line.split(':')[1:]).strip()
        elif line.strip().startswith('title:'):
            layout_title = ' '.join(line.split(':')[1:]).strip()
        elif line.strip().startswith('date:'):
            date = ' '.join(line.split(':')[1:]).strip()
        elif line.strip().startswith('categories:'):
            categories = ' '.join(line.split(':')[1:]).strip()
        elif line.strip().startswith('['):
            title, link = line.split('](')
            title = title[1:].strip()
            link = link[:-1].strip()
        elif line.strip().startswith('!['):
            image = line.split('(')[1][:-1].strip()
        elif line.strip().startswith('<details>'):
            break
        elif line.strip() != '':
            content += '\n' + line
    content = content.strip()

    return layout, layout_title, date, categories, title, link, image, content

def transform_md_file(file_path: str) -> str:
    try:
        layout, layout_title, date, categories, title, link, image, content = load_md_file(file_path)
        with open(file_path, 'r') as file:
            original_md = file.read()
        hot_and_keyword = (layout_title.split(']')[0] + ']').strip(' "')
    except Exception as e:
        traceback.print_exc()
        return None
    if 'llm' in categories:
        return None
    else:
        language = None
        if 'DE' in categories:
            language = 'German'
        elif 'EN' in categories:
            language = 'English'
        elif 'VN' in categories:
            language = 'Vietnamese'

        translated_title = translate_text(title, src_lang=language, tgt_lang="English", stop_sequences=['\n']).replace('\n', ' ').replace('"', "'")
        translated_content = translate_text(content, src_lang=language, tgt_lang="English")
        summarized_content = summarize_text(translated_content)

        md = f"""---
layout: {layout}
title: "{hot_and_keyword} {translated_title}"
date: {date}
categories: {categories} llm
---
[{translated_title}]({link})

>{summarized_content}

![{translated_title}]({image})

{translated_content}

<details>
  <summary>Origin content</summary>
  {original_md}
</details>
"""
        with open(file_path, 'w') as file:
            file.write(md)
        print(translated_title)
        return file_path

# Read files from path given in command line
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the path to the folder containing the markdown files")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"Path {path} does not exist")
        sys.exit(1)
    all_md_files = glob.glob(path + '/*.md')
    for md_file in all_md_files:
        transform_md_file(md_file)

    # PYTHONPATH=. python src/md_converter.py ./_posts