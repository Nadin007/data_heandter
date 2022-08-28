import concurrent.futures
import queue
from dataclasses import dataclass
from typing import Union

import requests
import threading
from bs4 import BeautifulSoup, SoupStrainer

import logging

logging.basicConfig(filename='file.log', level=logging.INFO)


@dataclass
class Company:
    name: str
    link: str
    html_page: Union[str, None] = None


LOCK = threading.Lock()
LOCK_Set = threading.Lock()
RESULT = {}
LINKS = set()

URLs = ['https://xbsoftware.com', 'https://www.jbsoftware.ca', 'https://www.itransition.com']


def requester(parser_queue: queue.Queue, url: str, name: str):
    try:
        page = requests.get(url).text
        logging.info("Requester got page: %s", url)
        parser_queue.put((url, page, name))
    except Exception as ex:
        logging.error('Can not parse obj %s', url)
        raise Exception(
            f'Can not parse obj: {ex}')


def request_all(requestor_queue: queue.Queue, parser_queue: queue.Queue):
    try:
        while True:
            url, name = requestor_queue.get()
            if not url:
                return
            requester(parser_queue, url, name)
    except Exception as ex:
        raise Exception(f'Something wrong happened {ex}')


def find_link(response):
    result = []
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            new_link = link['href']
            name = link.get_text()
        result.append((new_link, name))


def parser(requestor_queue: queue.Queue, parser_queue: queue.Queue, results: int):
    try:
        while results != 0:
            # Get/put is a block method - stop until it will be complited
            url, page, link_name = parser_queue.get()

            results -= 1
            html_page = BeautifulSoup(page, 'html.parser')
            key = url.split('/')[2]
            logging.info("Got key: %s", key)
            with LOCK:
                if key not in RESULT:
                    RESULT[key] = []
                RESULT[key].append(Company(link_name, url, html_page))
                logging.info('Added new element to RESULT - %s', key)
            for link in html_page.find_all('a', href=True):
                new_link = link['href']
                if new_link != '#' and new_link != '/':
                    if new_link.startswith('/'):
                        new_link = 'https://' + key + new_link
                    if new_link.startswith('https://' + key):
                        name = link.get_text()

                        with LOCK_Set:
                            if new_link in LINKS:
                                continue
                            LINKS.add(new_link)

                        logging.info('Accepted new link - %s', new_link)
                        results += 1
                        requestor_queue.put((new_link, name))
        requestor_queue.put((None, ''))
    except Exception as ex:
        logging.error("Error happened %s - %s", url, ex)
        raise Exception(f'Something wrong happened {ex}')


requestor_queue = queue.Queue(maxsize=200)
parser_queue = queue.Queue(maxsize=200)


for url in URLs:
    requestor_queue.put(
        (url, url.replace('https://', '').replace('.com', '')))


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    tasks = requestor_queue.qsize()
    executor.submit(request_all, requestor_queue, parser_queue)
    executor.submit(parser, requestor_queue, parser_queue, tasks)

logging.info('Parser finised!')


print(RESULT)
