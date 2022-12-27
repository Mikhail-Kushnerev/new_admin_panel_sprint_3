from elasticsearch.helpers import bulk

from utils.qyeries import first_film_work, genres, film_work, persons
from utils.constants import DOCUMENT_BODY


class Postgres:
    def __init__(self, conn, storage):
        self.__cur = conn.cursor()
        self.start = 0
        self.storage = storage

    def take_first_film_work_date(self):
        query = first_film_work
        self.__cur.execute(query)
        result = self.__cur.fetchone()
        date_first_film_work = result[0].date()
        return date_first_film_work

    def take_datas_by_date(self):
        date_first_film_work = self.take_first_film_work_date()
        # query = genres % date_first_film_work
        for query in (persons, genres):
            self.__cur.execute(query % date_first_film_work)
            result = list(self.__cur)
            start, end, mid = 0, len(result), 50
            while start <= end:
                ids_coll = []
                for i in result[start: start + mid]:
                    ids_coll.append(i[0])
                self.start += len(ids_coll)
                start += mid
                self.storage.set_state('stop', self.start)
                yield ids_coll

    def take_film_works_by_needed_ids(self):
        for i in self.take_datas_by_date():
            query = film_work % str(tuple(i))
            self.__cur.execute(query)
            for j in self.__cur:
                yield dict(j)

    def __call__(self, *args, **kwargs):
        for i in self.take_film_works_by_needed_ids():
            yield dict(i)
        else:
            print('all!')


class Elastic:
    def __init__(self, engine, datas=None):
        self.engine = engine
        self.datas = datas

    def check_exists_index(self):
        # es.indices.create(index='movies', mappings=mappings, settings=settings)
        ...

    def create_body_documents(self, data):
        DOCUMENT_BODY['_id'] = data['id']
        DOCUMENT_BODY['_source'] = data
        return self.create_documennt([DOCUMENT_BODY])

    def create_documennt(self, data):
        # print(data)
        bulk(self.engine, data)
        ...
