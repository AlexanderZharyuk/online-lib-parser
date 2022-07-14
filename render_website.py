import os
import json
import pprint

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def find_json_file(file: str, path: str) -> str:
    for root, dirs, files in os.walk(path):
        if file in files:
            return os.path.join(root, file)


def get_template(filename: str):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env.get_template(filename)


def get_books_from_json() -> dict:
    books_data = find_json_file(file='books_data.json', path='.')

    with open(books_data, 'r') as json_file:
        books = json.load(json_file)

    return books


def on_reload() -> None:
    template = get_template(filename='template.html')
    books = list(chunked(get_books_from_json(), 2))
    os.makedirs('pages', exist_ok=True)

    page = 1
    max_row_with_books = 5
    books_on_page = []
    for row_with_books, books in enumerate(books):
        if row_with_books >= max_row_with_books \
                and row_with_books % max_row_with_books == 0:
            rendered_page = template.render(books=books_on_page)

            with open(
                    f'pages/index{page}.html',
                    'w',
                    encoding="utf8"
            ) as file:
                file.write(rendered_page)
                page += 1
                books_on_page = []

        books_on_page.append(books)


def main() -> None:
    server = Server()
    on_reload()
    server.watch(filepath='pages')
    server.serve()


if __name__ == '__main__':
    main()
