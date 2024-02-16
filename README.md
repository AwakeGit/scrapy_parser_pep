# scrapy_parser_pep

### Описание:

Парсер PEP (Python Enhancement Proposal) собирает информацию и сохраняет в два CSV-файла: 
 * Информация о PEP (номер, название, статус).
 * Статусы PEP с общим количеством документов.


### Стек:

* Python v3.9
* Scrapy

## Установка и запуск проекта

Клонировать репозиторий и перейти в него в командной строке:
```python
git@github.com:AwakeGit/scrapy_parser_pep.git
cd scrapy_parser_pep
```
Cоздать и активировать виртуальное окружение:
```python
python -m venv venv
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```python
python -m pip install -r requirements.txt
```
Запуск парсера:
```python
scrapy crawl pep
```

## License

[MIT](https://choosealicense.com/licenses/mit/)