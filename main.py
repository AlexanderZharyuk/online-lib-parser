import os
import urllib.parse

from typing import NamedTuple
from urllib.parse import urljoin, urlparse

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError


def check_for_redirect(response):
    if response.history:
        raise HTTPError


class BookInfo(NamedTuple):
    title: str
    author: str
    book_image_url: str


def get_book_information(url: str) -> BookInfo:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    page_info = soup.find('body').find('h1').text.replace(u'\xa0', '')
    book_title, book_author = [text.strip() for text in page_info.split('::')]
    book_image = soup.find('div', class_='bookimage').find('img')['src']

    parsed_url = urlparse(url)
    domain = f'{parsed_url.scheme}://{parsed_url.netloc}'
    image_url = urljoin(domain, book_image)

    return BookInfo(title=book_title, author=book_author, book_image_url=image_url)


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()

    reformed_filename = f'{sanitize_filename(filename)}.txt'
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, reformed_filename)

    with open(file_path, 'wb') as book:
        book.write(response.content)

    return file_path


def download_image(url, image_name, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, image_name)

    with open(file_path, 'wb') as image:
        image.write(response.content)


if __name__ == '__main__':
    for book_id in range(1, 11):
        book_id_url = f'https://tululu.org/txt.php?id={book_id}'
        response = requests.get(book_id_url)
        response.raise_for_status()

        try:
            check_for_redirect(response)
        except HTTPError:
            continue

        book_url = f'https://tululu.org/b{book_id}'
        book_info = get_book_information(book_url)
        book_name = f'{book_id}. {book_info.title}'
        parsed_image_url = urlparse(book_info.book_image_url)
        image_name = parsed_image_url.path.split('/')[-1]
        download_txt(book_url, book_name)
        download_image(book_info.book_image_url, image_name)
