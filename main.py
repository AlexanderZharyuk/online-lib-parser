import os

import requests
from requests.exceptions import HTTPError


def download_logo():
    url = 'https://dvmn.org/filer/canonical/1542890876/16/'
    response = requests.get(url)
    response.raise_for_status()

    filename = 'dvmn.svg'
    with open(f'images/{filename}', 'wb') as logo:
        logo.write(response.content)


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def download_books():
    for book_id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={book_id}'
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
        except HTTPError:
            continue

        os.makedirs('books', exist_ok=True)
        filename = f'id {book_id}.txt'
        with open(f'books/{filename}', 'wb') as book:
            book.write(response.content)


if __name__ == '__main__':
    download_books()
