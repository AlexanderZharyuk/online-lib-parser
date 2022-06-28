import urllib.parse
import json

import requests

from bs4 import BeautifulSoup

from main import parse_book_page, download_txt, download_image


def find_books(category_url: str, pages: int) -> list:
    base_url = 'https://tululu.org/'

    founded_books = []
    for page_number in range(1, pages + 1):
        page_url = urllib.parse.urljoin(category_url, str(page_number))
        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        books_ids = [book_id.find('a')['href'] for book_id in soup.find_all('div', class_='bookimage')]
        for book_id in books_ids:
            founded_books.append(urllib.parse.urljoin(base_url, book_id))

    return founded_books


def write_to_json(books_urls: list):
    books_to_json = []

    for book_url in books_urls:
        response = requests.get(book_url)
        response.raise_for_status()

        requested_book = parse_book_page(response.text)
        book_path = download_txt(url=book_url, filename=requested_book.title)
        parsed_image_url = urllib.parse.urljoin(book_url, requested_book.book_image_name)
        image_name = parsed_image_url.split('/')[-1]
        book_image_path = download_image(url=parsed_image_url, image_name=image_name)

        book = {
            'title': requested_book.title,
            'author': requested_book.author,
            'img_src': book_image_path,
            'book_path': book_path,
            'comments': requested_book.comments,
            'genres': requested_book.genres
        }
        books_to_json.append(book)

    with open('books_data.json', 'w') as json_file:
        json.dump(books_to_json, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    founded_books = find_books('https://tululu.org/l55/', 4)
    write_to_json(founded_books)

