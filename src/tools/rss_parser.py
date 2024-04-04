import feedparser
import time
from dotenv import dotenv_values
from unidecode import unidecode
import html
import os
import traceback
from newspaper import Article

rss_config = dotenv_values('.env_rss')

def extract_content_from_news_url(url):
    summary, content, image = None, None, None
    try:
        article = Article(url)
        article.download()
        article.parse()
        summary = html.unescape(article.summary)
        content = html.unescape(article.text)
        image = article.top_image
    except:
        traceback.print_exc()
        print(f"Error in extracting content from {url}")
    return summary, content, image

def convert_entry_to_md(entry, geo):
    hot_rate = int(entry['ht_approx_traffic'].replace('+', '').replace(',', '')) # 2,000+ 20,000+ -> emoji:  🔥
    if hot_rate < 10000:
        hot_rate = ''
    elif hot_rate < 50000:
        hot_rate = '🔥🔥'
    elif hot_rate < 100000:
        hot_rate = '🔥🔥🔥'
    else:
        hot_rate = '🔥🔥🔥🔥'

    # convert escape characters to unicode
    item_title = html.unescape(entry['ht_news_item_title']).replace('"', "'")

    md = f"""---
layout: post
title: "{hot_rate} [{entry.title}] {item_title}"
date: {entry.published}
categories: entries {geo}
---
"""
    md += f"[{item_title}]({entry['ht_news_item_url']})\n\n"
    # md += f"{entry['ht_news_item_snippet']}\n\n"

    summary, content, image = extract_content_from_news_url(entry['ht_news_item_url'])

    if image:
        md += f"![{item_title}]({image})\n\n"

    if summary:
        md += f"{summary}\n\n"
    else:
        md += f"{html.unescape(entry['ht_news_item_snippet'])}\n\n"
    if content:
        md += f"{content}\n\n"

    return md

if __name__ == "__main__":
    for geo in rss_config['RSS_GEO'].split(','):
        d = feedparser.parse(rss_config['RSS_URL'] + geo)
        count = 0
        for i, entry in enumerate(d.entries):
            try:
                title = file_title = (time.strftime("%Y-%m-%d", entry.published_parsed) + '-' + unidecode(entry['title']).replace(' ', '-').lower() + ".md").replace('/', '-')
                if os.path.exists(os.path.join(rss_config['RSS_SAVE_PATH'], title)):
                    print(f"File {title} already exists")
                    continue
                content = convert_entry_to_md(entry, geo)
                with open(os.path.join(rss_config['RSS_SAVE_PATH'], title), 'w') as f:
                    f.write(content)
                    count += 1
                print(f"File {title} created")
            except:
                traceback.print_exc()
                print(f"Error in creating file {title}")

        print(f"Total {count} files created")