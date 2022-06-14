import os

from typing import NamedTuple

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


def get_book_information(url: str) -> BookInfo:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    post_title = soup.find('body').find('h1').text.replace(u'\xa0', '')
    book_title, book_author = [text.strip() for text in post_title.split('::')]

    return BookInfo(title=book_title, author=book_author)


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url)
    response.raise_for_status()

    reformed_filename = f'{sanitize_filename(filename)}.txt'
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, reformed_filename)

    with open(file_path, 'wb') as book:
        book.write(response.content)

    return file_path


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
        book_name = f'{book_id}. {get_book_information(book_url).title}'
        download_txt(book_url, book_name)
