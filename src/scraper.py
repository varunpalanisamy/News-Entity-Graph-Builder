import requests
from bs4 import BeautifulSoup
import spacy
from datetime import datetime
import re

nlp = spacy.load('en_core_web_sm')

def fetch_articles(url="https://www.ndtv.com/india", limit=15):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('h2', class_='newsHdng')
    return articles[:limit]

def convert_date_format(date_text):
    try:
        date_part = re.search(r'\w+ \d+, \d+', date_text).group()
        return datetime.strptime(date_part, '%B %d, %Y').strftime('%Y-%m-%d')
    except:
        return None

def scrape_article(article):
    title_tag = article.find('a')
    title = title_tag.text.strip() if title_tag else "No title"
    article_url = title_tag['href'] if title_tag else "No URL"

    content, date = "No content", "No date"
    if article_url != "No URL":
        article_response = requests.get(article_url)
        soup = BeautifulSoup(article_response.content, 'html.parser')
        content = ' '.join([p.text.strip() for p in soup.find_all('p')])
        date_tag = soup.find('span', class_='pst-by_lnk')
        date = convert_date_format(date_tag.text.strip()) if date_tag else "No date"

    doc = nlp(content)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return {'title': title, 'url': article_url, 'date': date, 'content': content, 'entities': entities}
