import argparse
import wikipedia
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

parser = argparse.ArgumentParser(
    description="script for extracting content from wikipedia pages"
)

parser.add_argument("--keyword", help="string argument to define the query string")
parser.add_argument("--num_urls", help="integer argument for number of wikipedia pages to extract from", type=int)
parser.add_argument("--output", help="output json-file name")

args = parser.parse_args()

def preprocess_func(soup):

    # Fetching the text
    text = ""
    for paragraph in soup.find_all('p', limit=3):
        text += paragraph.text
    
    # Preprocessing the data/text
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


keyword = args.keyword
num_urls = args.num_urls

wikipedia_pages = wikipedia.search(query=keyword, results=num_urls)

urls = []
paragraphs = []

for page_title in wikipedia_pages:
    try:
        _url = wikipedia.page(page_title, auto_suggest=False).url
        
        if _url not in urls:
            urls.append(_url)

            # Fetching the data
            response = requests.get(_url).text

            # Parsing the data/ Creating BeautifulSoup Object
            soup = BeautifulSoup(response, "html.parser")

            text = preprocess_func(soup)
            
            #We can also wikipedia.summary() to fetch summary of current page

            paragraphs.append(text)
    except:
        pass

# print(urls)

# print(paragraphs)

df = pd.DataFrame({"url" : urls , "paragraph" : paragraphs})
# df

df.to_json(args.output, orient='records')