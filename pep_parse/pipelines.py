from collections import defaultdict
from os import path
from typing import Dict, Any
import csv
import datetime as dt

BASE_DIR: str = path.dirname(path.dirname(path.abspath(__file__)))


class PepParsePipeline:
    """Пайплайн для подсчета количества элементов с разными статусами и
    сохранения результатов в CSV-файл."""

    def open_spider(self: 'PepParsePipeline', spider) -> None:
        """
        Инициализирует счетчик статусов.

        args:
            spider: PepParseSpider - экземпляр паука для парсинга данных.

        returns:
            None.
        """
        self.status_counter: Dict[str, int] = defaultdict(int)

    def process_item(
            self: 'PepParsePipeline',
            item: Dict[str, Any],
            spider
    ) -> Dict[str, Any]:
        """
        Обрабатывает элемент и обновляет счетчик статусов.

        args:
            item: Dict[str, Any]: словарь с данными, полученного пауком.
            spider: PepParseSpider: экземпляр паука для парсинга данных.

        returns:
            Dict[str, Any]: обработанный элемент.
        """
        self.status_counter[item['status']] += 1
        return item

    def close_spider(
            self: 'PepParsePipeline',
            spider
    ) -> None:
        """
        Создает CSV-файл с итоговой статистикой статусов.

        args:
            spider: PepParseSpider: экземпляр паука для парсинга данных.

        returns:
            None.
        """
        now: dt.datetime = dt.datetime.utcnow()
        filename: str = path.join(
            BASE_DIR, 'results', (
                f'status_summary_{now.strftime("%Y-%m-%d_%H-%M-%S")}.csv'
            )
        )
        with open(filename, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect=csv.unix_dialect)
            writer.writerows((
                ('Статус', 'Количество'),
                *self.status_counter.items(),
                ('Всего', sum(self.status_counter.values()))
            ))
