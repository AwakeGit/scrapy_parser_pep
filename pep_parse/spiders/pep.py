import re
from typing import Generator, List, Union, Any
from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """
    Паук для парсинга (PEP) с сайта peps.python.org.
    """

    name: str = 'pep'
    allowed_domains: list[str] = ['peps.python.org']
    start_urls: list[str] = ['https://peps.python.org/']

    def parse(self, response: scrapy.http.Response) -> Generator[
        scrapy.Request, None, None]:
        """
        Обрабатывает ответ с главной страницы, содержащей список PEP.

        args:
            response (scrapy.http.Response): Объект ответа с главной страницы.

        returns:
            Generator[scrapy.Request, None, None]:
            Генератор scrapy-запросов для парсинга каждой страницы PEP.
        """
        peps: object = response.css('#numerical-index tbody tr')

        for pep in peps:
            link: object = pep.css('a::attr(href)').get()
            yield response.follow(
                urljoin(self.start_urls[0], link), callback=self.parse_pep
            )

    def parse_pep(self, response: scrapy.http.Response) -> Generator[
        PepParseItem, None, None]:
        """
        Обрабатывает ответ с отдельной страницы PEP.

        args:
            response (scrapy.http.Response): Объект ответа с страницы PEP.

        returns:
            Generator[PepParseItem, None, None]:
            Генератор элементов с информацией о парсинге PEP.
        """
        pattern: str = r'PEP (?P<number>\d+) – (?P<name>.*)'

        number: Union[str, Any]
        name: Union[str, Any]
        number, name = re.search(
            pattern, response.css('h1.page-title::text').get()
        ).groups()

        yield PepParseItem({
            'number': number,
            'name': name,
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get()
        })
