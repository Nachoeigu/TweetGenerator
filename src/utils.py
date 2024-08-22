import re
from pytube import YouTube
from langchain_community.document_loaders import WebBaseLoader
import requests
import bs4
from src.constants import UNICEF_HEADERS
from datetime import datetime, timezone
from lxml import html

def is_youtube_url(url):
    # Regular expression pattern for YouTube URLs
    youtube_regex = (
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )

    youtube_regex_match = re.match(youtube_regex, url)
    return bool(youtube_regex_match)


def is_medium_url(url):
    # Regular expression pattern for Medium URLs
    medium_regex = r"https?://medium\.com/"
    medium_regex_match = re.match(medium_regex, url)
    return bool(medium_regex_match)


def get_youtube_description(url):
    # Create a YouTube object
    yt = YouTube(url)

    return f"Title: {yt.title}\n\nDescription: {yt.description}"


def get_medium_content(url):
    loader = WebBaseLoader(
        web_paths=[url],
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer("article")
        ),  # only elements in article tag
    )

    docs = loader.load()
    return docs[0].page_content

def is_unicef_site(url):
    unicef_regex = r"https://(www\.)?unicef\.org/.*"
    unicef_regex_match = re.match(unicef_regex, url)
    return bool(unicef_regex_match)

def get_unicef_content(url):
    
    response = requests.get(
        url = url,
        headers = UNICEF_HEADERS
    )

    data = html.fromstring(response.content)

    title = 'TITLE:\n'+ data.xpath("//h1[@class='h1']")[0].text.strip() + '\n\n'
    try:
        description = 'SUB-TITLE:\n'+ data.xpath("//h3[@class='sub-title center']")[0].text.strip() + '\n\n'
    except IndexError:
        description = ''
    content = 'CONTENT:\n'+ ' '.join([paragraph.replace('\xa0', ' ').strip() for paragraph in data.xpath("//div[contains(@class, 'text_content')]//p//text()")])

    return title + description + content


def get_content(url):
    if is_youtube_url(url):
        return get_youtube_description(url)
    elif is_medium_url(url):
        return get_medium_content(url)
    elif is_unicef_site(url):
        return get_unicef_content(url)
    else:
        loader = WebBaseLoader(url)
        docs = loader.load()
        return docs[0].page_content
