import os

from typing import NamedTuple

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError


def check_for_redirect(response):
    if response.history:
        raise HTTPError


class Book(NamedTuple):
    title: str
    author: str
    book_image_url: str
    comments: list
    genres: list


def parse_book_page(page_html: str) -> Book:
    soup = BeautifulSoup(page_html, 'lxml')

    selector = 'body h1'
    page = soup.select_one(selector).text.replace(u'\xa0', '')
    book_title, book_author = [text.strip() for text in page.split('::')]

    selector = '.bookimage img'
    book_image = soup.select_one(selector)['src']

    selector = '.texts .black'
    comments = [comment.text for comment in soup.select(selector)]

    selector = 'span.d_book a'
    genres = [genre.text for genre in soup.select(selector)]

    return Book(title=book_title, author=book_author, book_image_url=book_image,
                comments=comments, genres=genres)


def download_txt(url, filename, folder='parse_results/books/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    reformed_filename = f'{sanitize_filename(filename)}.txt'
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, reformed_filename)

    with open(file_path, 'wb') as book:
        book.write(response.text.encode("utf-8"))

    return file_path


def download_image(url, image_name, folder='parse_results/images/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, image_name)

    with open(file_path, 'wb') as image:
        image.write(response.content)

    return file_path
