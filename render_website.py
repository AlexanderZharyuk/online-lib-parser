import os
import json
import math

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def find_json_file(filename: str, path: str) -> str:
    for root, dirs, files in os.walk(path):
        if filename in files:
            return os.path.join(root, filename)


def get_template(filename: str):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env.get_template(filename)


def get_books_from_json() -> dict:
    json_filepath = find_json_file(filename='books_data.json', path='.')

    with open(json_filepath, 'r') as json_file:
        books = json.load(json_file)

    return books


def on_reload() -> None:
    template = get_template(filename='template.html')
    os.makedirs('pages', exist_ok=True)

    max_row_with_books_on_page = 5
    columns_with_books_on_page = 2

    books_count_on_page = max_row_with_books_on_page * columns_with_books_on_page
    books = list(chunked(get_books_from_json(), columns_with_books_on_page))
    all_books_count = len(books) * columns_with_books_on_page
    total_pages = math.ceil(all_books_count / books_count_on_page)
    splited_books_by_pages = list(chunked(books, max_row_with_books_on_page))

    for page, books_on_row in enumerate(splited_books_by_pages, start=1):
        rendered_page = template.render(
            books=books_on_row,
            total_pages=total_pages,
            page=page
        )

        index_file = f'pages/index{page}.html'
        with open(index_file, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main() -> None:
    server = Server()
    on_reload()
    server.watch(filepath='pages')
    server.serve()


if __name__ == '__main__':
    main()
