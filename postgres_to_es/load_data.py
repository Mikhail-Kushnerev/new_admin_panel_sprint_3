import datetime
import json
from typing import Any, Callable, Generator, Optional

from elasticsearch.helpers import bulk
from elasticsearch import NotFoundError
from pydantic import ValidationError

from utils import (
    Model,
    INDEX_NAME,
    first_film_work_query,
    genres_query,
    film_work_query,
    persons_query,
    mappings,
    settings
)


class Postgres:
    def __init__(self, conn, storage, checkpoint=None):
        self.__cur = conn.cursor()
        self.start: int = 0
        self.checkpoint: Optional[datetime] = checkpoint
        self.storage = storage
        self.date: str = ''

    def _take_first_film_work_date(self) -> datetime:
        """
        Метод, возвращающий самый ранний фильм

        Returns:
            datetime: `updated_at` самой первой записи в Filmwork

        """
        query: str = first_film_work_query
        self.__cur.execute(query)
        result: list[datetime] = self.__cur.fetchone()
        date_first_film_work: datetime = result[0]
        return date_first_film_work

    def _take_datas_by_date(self) -> Generator[list[str], None, None]:
        """
        Метод, генерирующий список индексов заданной длинны из выборки

        Yields:
            list[str]: Список из 50 индексов БД (М2М), удовлетворяющие условию

        """
        for query in (persons_query, genres_query):
            self.__cur.execute(query % self.checkpoint)
            result: list[str] = list(self.__cur)
            start, end, mid = 0, len(result), 50

            while start <= end:
                ids_coll: list[str] = []

                for data in result[start: start + mid]:
                    ids_coll.append(data[0])

                self.start += len(ids_coll)
                start += mid
                yield ids_coll

    def _take_film_works_by_needed_ids(
            self
    ) -> Generator[list[dict[str, Any]], None, None]:
        """
        Метод, генерирующий список из полной информации о фильмах

        Yields: Список записей Filmwork, индексы которые удовлетворяют условию

        """
        for data in self._take_datas_by_date():
            query: str = film_work_query % str(tuple(data))
            self.__cur.execute(query)

            result_coll: list[dict[str, Any]] = self._make_target_to_dict()

            self.storage.set_state(
                'finished part',
                json.dumps(self.date, default=str)
            )

            yield result_coll

    def _make_target_to_dict(self) -> list[dict[str, Any]]:
        """
        Метод, проверяющий корректность аргументов у записи

        Returns: Список записей Filmwork, прошедшие валидацию

        Raises: Запись пропускается, проверяется следующая

        """
        result_coll: list[dict[str, Any]] = []
        for data in self.__cur:
            target: dict[str, Any] = dict(data)
            self.date: datetime = target.pop('updated_at')

            try:
                self._validate_film_work(target)
            except ValidationError:
                continue
            else:
                result_coll.append(target)

        return result_coll

    @staticmethod
    def _validate_film_work(target: dict[str, Any]) -> None:
        """
        Валидатор

        Args:
            target (dict[str, Any]): Запись Filmwork

        """
        for arg in target:
            setattr(Model, arg, target[arg])

    def __call__(self, *args, **kwargs):
        """
        Запуск сбора записей для переноса в ElasticSearch. Сбор
        осуществляется посредством выполнения условия. Для его выполнения
        необходима переменная `self.checkpoint`. Если она не определена,
        то опорной точкой для сравнения самый ранний фильм.


        Yields: Выборка записей Filmwork для последующей записи в Elastic

        """
        self.checkpoint: None = self.storage.get_state('finished part')
        if not self.checkpoint:
            self.checkpoint: datetime = self._take_first_film_work_date()

        for data in self._take_film_works_by_needed_ids():
            yield data


class Elastic:
    def __init__(self, engine):
        self.engine = engine

    def _check_exists_index(self):
        """
        Метод, проверяющий существование индекса.
        """

        try:
            self.engine.indices.get(index=INDEX_NAME)
        except NotFoundError:
            self.engine.indices.create(
                index=INDEX_NAME,
                mappings=mappings,
                settings=settings
            )

    def create_body_documents(
            self,
            datas: list[dict[str, Any]]
    ) -> Callable[[list[dict[str, Any]]], None]:
        """
        Метод, подготавливающий найденную выборку в соответствии с
        требованиями создания документа для ElasticSearch

        Args:
            datas (list[dict[str, Any]]): Выборка записей Filmwork

        Returns: Комплект документов для записи в ElasticSearch

        """
        self._check_exists_index()
        results_coll: list[dict[str, Any]] = [
            {
                '_index': INDEX_NAME,
                '_id': film_work['id'],
                '_source': film_work
            }
            for film_work in datas
        ]
        return self._create_document(results_coll)

    def _create_document(self, data: list[dict[str, Any]]) -> None:
        """
        Метод, записывающий комплект документов в ElasticSearch

        Args:
            data (list[dict[str, Any]]): Комплект документов, прошедщих
                верификацию для записи в ElasticSearch
        """

        bulk(self.engine, data, index=INDEX_NAME)
        self.engine.indices.refresh(index=INDEX_NAME)
