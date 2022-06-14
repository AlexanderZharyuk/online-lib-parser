# LIBRARY PARSER

Парсер, который позволяет получить информацию о книгах с сайта [tutulu](https://tululu.org/).
Данный скрипт выкачивает обложку книги и саму книгу в директории `images/` и `books/` соответственно.

## Предустановка

Все используемые библиотеки указаны в файле **requirements.txt**
Для установки библиотек в виртуальное окружение используйте команды:

```
pip install -r requirements.txt
```

### Начало работы

Для старта скрипта напишите в консоле, находясь в директории с файлом:
```
python3 main.py [--start_id]={START_ID_BOOK} [--end_id]={END_ID_BOOK}
```
Где вместо `START_ID_BOOK` передайте id книги с которой начать поиск, а вместо `END_ID_BOOK` передайте id книги на которой закончить поиск.
Команда запущенная без этих аргументов спарсит информцию от книги под номером 1 до 10.

Пример выполнения скрипта:
```
python3 main.py --start_id=20 --end_id=30
```

## Создано при помощи

* [DEVMAN](https://dvmn.org/) - Обучающая платформа

## Авторы

* [Alexander Zharyuk](https://gist.github.com/AlexanderZharyuk)
