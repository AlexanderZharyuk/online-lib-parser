# LIBRARY PARSER

Парсер, который позволяет получить информацию о книгах с сайта [tutulu](https://tululu.org/). А также вывести эту информацию на свой сайт.

Пример сайта: [https://alexanderzharyuk.github.io/](https://alexanderzharyuk.github.io/online-lib-parser/pages/index1.html)

## Предустановка

Все используемые библиотеки указаны в файле `requirements.txt`
Для установки библиотек в виртуальное окружение используйте команды:

```
pip install -r requirements.txt
```

### Если вы хотите запустить сайт локально
Для запуска сайта локально напишите команду:

```shell
python3 render_website.py
```
После чего запустится сервер по адресу `http://127.0.0.1:5500/`, далее переходите по ссылке [http://127.0.0.1:5500/pages/index1.html](http://127.0.0.1:5500/pages/index1.html).

### Если вы хотите собрать свою базу с книгами
Для создания json-файла с данными используйте следующие файлы:

* **parse_books_by_id.py**

Данный скрипт качает книги с абсолютно любой категорией, подбирая `id-книги`. 
У этого скрипта два аргумента, которые вы можете использовать при запуске:
``` 
start_id - Передайте здесь id-книги, с которой желаете начать поиск | DEFAULT=1
end_id - Передайте здесь id-книги, на которой желаете закончить поиск | DEFAULT=10
```
Если аргументы не будут указаны, то скрипт возьмет значения по умолчанию.

Для старта скрипта напишите в консоле, находясь в директории с файлом:
```
python3 parse_books_by_id.py
```

Пример выполнения скрипта:
```
python3 parse_books_by_id.py --start_id=20 --end_id=30
```

* **parse_tululu_category.py**

Данный скрипт качает книги из категории "Научная фантастика". 
У этого скрипта несколько аргументов, которые вы можете использовать при запуске:
``` 
start_page - Укажите с какой страницы начать парсинг | DEFAULT=1
end_page - Укажите на какой странице закончить парсинг | DEFAULT=Последняя страница
dest_folder - Папка, куда сохранится результат парсинга | DEFAULT=parse_results/
skip_imgs - Укажите этот флаг, если не хотите скачивать фото книги | DEFAULT=False
skip_txts - Укажите этот флаг, если не хотите скачивать текст книги | DEFAULT=False
json_path - Можете указать свой путь до .json-файла, где будет информация о книгах.| DEFAULT=parse_results/books_data.json
```
Если аргументы не будут указаны, то скрипт возьмет значения по умолчанию.

Для старта скрипта напишите в консоле, находясь в директории с файлом:
```
python3 parse_tululu_category.py
```

Примеры выполнения скрипта:
```
python3 parse_tululu_category.py --start_page=700
python3 parse_tululu_category.py --start_page=650 --end_page 700 --dest_folder results --skip_imgs
python3 parse_tululu_category.py --end_page 10 --skip_txts --json_path json_files/json_data.json
```

После заполнения данных - запускаете локальный сервер командой:

```shell
python3 render_website.py
```

Если вы хотите поменять что-либо в верстке сайта - используйте файл `template.html`.

## Создано при помощи

* [DEVMAN](https://dvmn.org/) - Обучающая платформа

## Авторы

* [Alexander Zharyuk](https://gist.github.com/AlexanderZharyuk)
