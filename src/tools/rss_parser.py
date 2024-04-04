import feedparser
import time
from dotenv import dotenv_values
from unidecode import unidecode
import os
import traceback
rss_config = dotenv_values('.env_rss')

def convert_entry_to_md(entry):
    hot_rate = int(entry['ht_approx_traffic'].replace('+', '').replace(',', '')) # 2,000+ 20,000+ -> emoji:  🔥
    if hot_rate < 10000:
        hot_rate = ''
    elif hot_rate < 50000:
        hot_rate = '🔥🔥'
    elif hot_rate < 100000:
        hot_rate = '🔥🔥🔥'
    else:
        hot_rate = '🔥🔥🔥🔥'
    md = f"""---
layout: post
title:  "{hot_rate} [{entry.title}] {entry['ht_news_item_title']}"
date:   {entry.published}
categories: entries
---
"""
    md += f"[{entry['ht_news_item_title']}]({entry['ht_news_item_url']})\n\n"
    md += f"{entry['ht_news_item_snippet']}\n\n"

    # file title (remove tone) include date and title in camel case
    file_title = time.strftime("%Y-%m-%d", entry.published_parsed) + '-' + unidecode(entry['title']).replace(' ', '-').lower() + ".md"
    return file_title.replace('/', '-'), md

if __name__ == "__main__":
    d = feedparser.parse(rss_config['RSS_URL'])
    count = 0
    for i, entry in enumerate(d.entries):
        try:
            title, content = convert_entry_to_md(entry)
            if os.path.exists(os.path.join(rss_config['RSS_SAVE_PATH'], title)):
                print(f"File {title} already exists")
                continue
            with open(os.path.join(rss_config['RSS_SAVE_PATH'], title), 'w') as f:
                f.write(content)
                count += 1
            print(f"File {title} created")
        except:
            traceback.print_exc()
            print(f"Error in creating file {title}")

    print(f"Total {count} files created")