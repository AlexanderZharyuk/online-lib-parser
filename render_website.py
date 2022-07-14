import os
import json

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
    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main() -> None:
    server = Server()
    on_reload()
    server.watch(filepath='index.html')
    server.serve()


if __name__ == '__main__':
    main()
