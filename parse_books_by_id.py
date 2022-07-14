import argparse
import logging
import time

from urllib.parse import urljoin, urlencode

import requests

from requests.exceptions import HTTPError, ConnectionError

from general_functions import check_for_redirect, parse_book_page, download_txt, download_image


def main():
    parser = argparse.ArgumentParser(
        description='Парсер выводит информацию о '
                    'книгах, их картинки и качает их.'
    )
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
            parsed_image_url = urljoin(book_url, book.book_image_url)
            image_name = parsed_image_url.split('/')[-1]

            download_txt(book_full_url, book_name)
            download_image(parsed_image_url, image_name)
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


if __name__ == '__main__':
    main()
