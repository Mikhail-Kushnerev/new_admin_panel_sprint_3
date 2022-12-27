from time import sleep

from etl.utils.qyeries import first_film_work, genres, film_work


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
        query = genres % date_first_film_work
        self.__cur.execute(query)
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
            yield dict(i), self.start
        else:
            print('all!')



class Elastic:
    ...
