#!/usr/bin/env python

import feedparser
import re
import random
from bs4 import BeautifulSoup
import requests

TABLE_TEMPLATE = """
<table style="border-radius: 5px">
    {rows}
</table>
"""

LATEST_ARTICLE_TEMPLATE = """    <tr>
        <td>
            {banner}
        </td>
        <td>
            {title}
            {description}
        </td>
    </tr>
"""

BANNER_START = '<a class="article-body-image-wrapper">'
BANNER_END = '</a>'

LATEST_ARTICLES_START = '<!-- latest articles start -->'
LATEST_ARTICLES_END = '<!-- latest articles end -->'
REPLACE_PATTERN = re.compile(rf'({LATEST_ARTICLES_START}).*({LATEST_ARTICLES_END})', re.DOTALL)


def add_row(feed_entry):
    r = lambda: random.randint(0, 255)
    collor = lambda: 'style="background-color:  #f8B4%02X"' % (r())
    title = f'<h3><a href="{feed_entry.link}">{feed_entry.title}</a></h3>'
    # tags = "<div class=\"container\">" + " ".join([f"<div class=\"item\" {collor()}>{i.term}</div>" for i in feed_entry.tags]) + "</div>"
    tags = "<div class=\"container\">" + ", ".join([i.term for i in feed_entry.tags]) + "</div>"

    page = requests.get(feed_entry.link)
    soup = BeautifulSoup(page.text, "html.parser")
    img = soup.find('img', class_='crayons-article__cover__image')
    img['height'] = '100'
    img['width'] = '200'

    return LATEST_ARTICLE_TEMPLATE.format(banner=img, title=title, description=tags)


def update_readme(updated_table):
    with open('README.md', mode='r+', encoding='utf-8') as readme:
        current = readme.read()
        updated = re.sub(REPLACE_PATTERN, rf'\1{updated_table}\2', current)
        readme.seek(0)
        readme.write(updated)
        readme.truncate()


res = feedparser.parse("https://dev.to/feed/daniilroman")

rows = ''
for entry in res.entries[0:5]:
    rows += add_row(entry)

updated_table = TABLE_TEMPLATE.format(rows=rows.strip())
update_readme(updated_table)