import argparse
import urllib.parse
import json
import os
import time
import logging

import requests

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from general_functions import parse_book_page, download_txt, download_image, check_for_redirect


def find_books(category_url: str, start_page: int, end_page: int) -> list:
    all_books_ids = []
    for page_number in range(start_page, end_page):
        page_url = urllib.parse.urljoin(category_url, str(page_number))
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            check_for_redirect(response)
        except ConnectionError:
            logging.error('ConnectionError. Something was wrong with Internet Connection. Going sleep 1 min.')
            time.sleep(60)
            continue
        except HTTPError:
            logging.error("HTTPError, can't find address")
            continue
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            selector = '.bookimage a'
            books_in_page_ids = [found_selector['href'] for found_selector in soup.select(selector)]
            [all_books_ids.append(book_id) for book_id in books_in_page_ids]

    founded_books = [urllib.parse.urljoin(category_url, book_id) for book_id in all_books_ids]
    return founded_books


def write_to_json(books_urls: list, folder: str, skip_images: bool,
                  skip_txts: bool, json_path: str) -> None:
    books_to_json = []

    for book_url in books_urls:
        books_folder = os.path.join(folder, 'books')
        images_folder = os.path.join(folder, 'images')

        try:
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
        except ConnectionError:
            logging.error('ConnectionError. Something was wrong with Internet Connection. Going sleep 1 min.')
            time.sleep(60)
            continue
        except HTTPError:
            logging.error("HTTPError, can't find address")
            continue

        requested_book = parse_book_page(response.text)
        book = {
            'title': requested_book.title,
            'author': requested_book.author
        }

        parsed_image_url = urllib.parse.urljoin(book_url, requested_book.book_image_name)
        image_name = parsed_image_url.split('/')[-1]
        if not skip_images:
            book_image_path = download_image(url=parsed_image_url, image_name=image_name,
                                             folder=images_folder)
            book['img_src'] = book_image_path

        if not skip_txts:
            book_path = download_txt(url=book_url, filename=requested_book.title,
                                     folder=books_folder)
            book['book_path'] = book_path

        book['comments'] = requested_book.comments
        book['genres'] = requested_book.genres
        books_to_json.append(book)

    json_folder, json_filename = os.path.split(json_path)
    if not os.path.isdir(json_folder):
        os.makedirs(json_folder, exist_ok=True)

    with open(json_path, 'w') as json_file:
        json.dump(books_to_json, json_file, ensure_ascii=False, indent=4)


def get_pages_count(category_url: str) -> int:
    response = requests.get(category_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    selector = '.npage:last-of-type'
    pages_count = int(soup.select_one(selector).text)

    return pages_count


def main():
    pages_count = get_pages_count('https://tululu.org/l55/')

    parser = argparse.ArgumentParser(description='Парсер книг из категории Научная Фантастика.')
    parser.add_argument('--start_page', type=int, default=1,
                        help='Укажите с какой страницы начать парсинг')
    parser.add_argument('--end_page', type=int, default=pages_count + 1,
                        help='Укажите на какой странице закончить парсинг')
    parser.add_argument('--dest_folder', type=str, default='parse_results/',
                        help='Папка, куда сохранится результат парсинга')
    parser.add_argument('--skip_imgs', action='store_true',
                        help='Укажите этот флаг, если не хотите скачивать фото книги')
    parser.add_argument('--skip_txts', action='store_true',
                        help='Укажите этот флаг, если не хотите скачивать текст книги')
    parser.add_argument('--json_path', type=str, default='parse_results/books_data.json',
                        help='Можете указать свой путь до .json-файла, где будет информация о книгах.')
    args = parser.parse_args()

    founded_books = find_books('https://tululu.org/l55/', start_page=args.start_page,
                               end_page=args.end_page)
    write_to_json(founded_books, folder=args.dest_folder, skip_images=args.skip_imgs,
                  skip_txts=args.skip_txts, json_path=args.json_path)


if __name__ == '__main__':
    main()
