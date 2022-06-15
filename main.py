import argparse
import os
import time

from typing import NamedTuple
from urllib.parse import urljoin, urlparse

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


def parse_book_page(url: str) -> BookInfo:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    page_info = soup.find('body').find('h1').text.replace(u'\xa0', '')
    book_title, book_author = [text.strip() for text in page_info.split('::')]
    book_image = soup.find('div', class_='bookimage').find('img')['src']

    parsed_url = urlparse(url)
    domain = f'{parsed_url.scheme}://{parsed_url.netloc}'
    image_url = urljoin(domain, book_image)

    comments = ''
    if soup.find('div', class_='texts'):
        all_comments_html = [comment.find('span', class_="black")
                             for comment in soup.find_all('div', class_='texts')]
        for comment in all_comments_html:
            comments += comment.text

    genres = []
    for genre in soup.find('span', class_='d_book').find_all('a'):
        genres.append(genre.text)

    return BookInfo(title=book_title, author=book_author, book_image_url=image_url, comments=comments, genres=genres)


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
    parser = argparse.ArgumentParser(description='Парсер выводит информацию о книгах, их картинки и качает их.')
    parser.add_argument('--start_id', type=int, default=1)
    parser.add_argument('--end_id', type=int, default=10)
    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id + 1):
        params = {
            'id': book_id
        }
        book_id_url = f'https://tululu.org/txt.php'
        try:
            response = requests.get(book_id_url, params=params)
            response.raise_for_status()
            check_for_redirect(response)

            book_url = f'https://tululu.org/b{book_id}'
            book_info = parse_book_page(book_url)
            book_name = f'{book_id}. {book_info.title}'
            parsed_image_url = urlparse(book_info.book_image_url)
            image_name = parsed_image_url.path.split('/')[-1]

            download_txt(book_url, book_name)
            download_image(book_info.book_image_url, image_name)
        except ConnectionError:
            print('ConnectionError. Going sleep 1 min.')
            time.sleep(60)
            continue
        except HTTPError:
            print('HTTPError')
            continue

        print(f'Заголовок: {book_info.title}')
        print(f'Жанр: {book_info.genres}')
        print(f'Автор: {book_info.author}')
