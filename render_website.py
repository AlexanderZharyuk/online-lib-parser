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
    books = list(chunked(get_books_from_json(), 2))
    os.makedirs('pages', exist_ok=True)

    max_row_with_books = 5
    books_per_page = max_row_with_books * 2
    all_books_count = len(books) * 2
    total_pages = math.ceil(all_books_count / books_per_page)

    page = 1
    books_on_page = []
    for row_number, books in enumerate(books):
        if row_number >= max_row_with_books and \
                row_number % max_row_with_books == 0:
            rendered_page = template.render(
                books=books_on_page,
                total_pages=total_pages,
                page=page
            )

            index_file = f'pages/index{page}.html'
            with open(index_file, 'w', encoding="utf8") as file:
                file.write(rendered_page)

            page += 1
            books_on_page = []
        books_on_page.append(books)

    if books_on_page:
        rendered_page = template.render(
            books=books_on_page,
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
