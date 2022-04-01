from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError
import requests
import re
from queue import Queue

def simple_job(count):
    return count

def get_links(url):
    req = Request(url)

    try:
        html_page = urlopen(req)
    except URLError as e:
        return []

    soup = BeautifulSoup(html_page, "lxml")
    links = []
    for link in soup.findAll('a'):
        possible_link = link.get('href')
        if possible_link is not None and len(possible_link) > 4 and possible_link[:4] == "http":
            links.append(possible_link)

    return links

def search_path(url_from, url_to, max_transiitions):
    links = Queue()
    links.put((url_from, [url_from.encode("utf-8", 'ignore')]))

    for i in range(max_transiitions):
        url, path_to_link = links.get()
        if url == url_to:
            return path_to_link
        
        for child_link in get_links(url):
            links.put((child_link, path_to_link + [child_link.encode("utf-8", 'ignore')]))

        if links.empty():
            return []

    return []
