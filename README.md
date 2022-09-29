# LIBRARY PARSER

A web-scraping parser that allows you to get information about books from the site [tutulu](https://tululu.org/). And also display this information on your website.

Site example: [https://alexanderzharyuk.github.io/](https://alexanderzharyuk.github.io/online-lib-parser/pages/index1.html)

## Setting up your development environment

All libraries used are specified in the `requirements.txt` file
To install libraries in a virtual environment, use the commands:

```
pip install -r requirements.txt
```

### If you want to run the site locally
To run the site locally, write the command:

```shell
python3 render_website.py
```
After that, the server will start at `http://127.0.0.1:5500/`, then follow the link [http://127.0.0.1:5500/pages/index1.html](http://127.0.0.1:5500 /pages/index1.html).

### If you want to build your base with books
To create a json file with data, use the following commands:

* **parse_books_by_id.py**

This script downloads books with absolutely any category, selecting `id-books`.
This script has two arguments that you can use when running:
```
start_id - Pass here the id of the book you want to start the search with | DEFAULT=1
end_id - Pass here the id of the book you want to end the search on | DEFAULT=10
```
If no arguments are specified, the script will take the default values.

To start the script, write in the console, being in the directory with the file:
```
python3 parse_books_by_id.py
```

Example of script execution:
```
python3 parse_books_by_id.py --start_id=20 --end_id=30
```

* **parse_tululu_category.py**

This script downloads books from the "Science Fiction" category.
This script has several arguments that you can use when running:
```
start_page - Specify which page to start parsing from | DEFAULT=1
end_page - Specify on which page to end parsing | DEFAULT=Last page
dest_folder - Folder where the parsing result will be saved | DEFAULT=parse_results/
skip_imgs - Specify this flag if you don't want to download photo books | DEFAULT=False
skip_txts - Specify this flag if you don't want to download book text | DEFAULT=False
json_path - You can specify your path to the .json file where the information about the books will be.| DEFAULT=parse_results/books_data.json
```
If no arguments are specified, the script will take the default values.

To start the script, write in the console, being in the directory with the file:
```
python3 parse_tululu_category.py
```

Examples of script execution:
```
python3 parse_tululu_category.py --start_page=700
python3 parse_tululu_category.py --start_page=650 --end_page 700 --dest_folder results --skip_imgs
python3 parse_tululu_category.py --end_page 10 --skip_txts --json_path json_files/json_data.json
```

After filling in the data, start the local server with the command:

```shell
python3 render_website.py
```

If you want to change something in the layout of the site, use the `template.html` file.

## The author

* [Alexander Zharyuk](https://gist.github.com/AlexanderZharyuk)
