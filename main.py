import argparse
import logging
import os
import time

from typing import NamedTuple
from urllib.parse import urljoin, urlparse, urlencode

import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError, ConnectionError


def check_for_redirect(response):
    if response.history:
        raise HTTPError


class BookInfo(NamedTuple):
    title: str
    author: str
    book_image_url: str
    comments: str
    genres: list


def parse_book_page(page_html: str) -> BookInfo:
    soup = BeautifulSoup(page_html, 'lxml')
    page_info = soup.find('body').find('h1').text.replace(u'\xa0', '')
    book_title, book_author = [text.strip() for text in page_info.split('::')]
    book_image = soup.find('div', class_='bookimage').find('img')['src']

    domain = 'https://tululu.org'
    image_url = urljoin(domain, book_image)

    comments = [comment.find('span', class_="black").text for comment in soup.find_all('div', class_='texts')]

    genres = [genre.text for genre in soup.find('span', class_='d_book').find_all('a')]

    return BookInfo(title=book_title, author=book_author, book_image_url=image_url,
                    comments='\n'.join(comments), genres=genres)


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    reformed_filename = f'{sanitize_filename(filename)}.txt'
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, reformed_filename)

    with open(file_path, 'wb') as book:
        book.write(response.text.encode("utf-8"))

    return file_path


def download_image(url, image_name, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, image_name)

    with open(file_path, 'wb') as image:
        image.write(response.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Парсер выводит информацию о книгах, их картинки и качает их.')
    parser.add_argument('--start_id', type=int, default=1)
    parser.add_argument('--end_id', type=int, default=10)
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id + 1):
        params = {
            'id': book_id
        }
        book_id_url = 'https://tululu.org/txt.php?'
        try:
            book_full_url = book_id_url + urlencode(params)

            book_url = f'https://tululu.org/b{book_id}/'
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)

            book = parse_book_page(response.text)
            book_name = f'{book_id}. {book.title}'
            parsed_image_url = urlparse(book.book_image_url)
            image_name = parsed_image_url.path.split('/')[-1]

            download_txt(book_full_url, book_name)
            download_image(book.book_image_url, image_name)
        except ConnectionError:
            logging.error('ConnectionError. Going sleep 1 min.')
            time.sleep(60)
            continue
        except HTTPError:
            logging.error('HTTPError. Maybe book id not find.')
            continue

        print(f'Заголовок: {book.title}')
        print(f'Жанр: {book.genres}')
        print(f'Автор: {book.author}')
        print(f'Comments: {book.comments}')
