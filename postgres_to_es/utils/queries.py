genres_query: str = '''
SELECT DISTINCT gfw.film_work_id
FROM content.genre g
LEFT JOIN content.genre_film_work gfw ON gfw.genre_id = g.id
WHERE g.updated_at >= '%s';
'''

persons_query: str = '''
SELECT DISTINCT pfw.film_work_id
FROM content.person p
LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
WHERE p.updated_at >= '%s';
'''

film_work_query: str = '''
SELECT
    fw.id,
    fw.updated_at,
    fw.rating AS imdb_rating,
    COALESCE (
        ARRAY_AGG(
            DISTINCT g.name
        ),
        '{}'
    ) AS genre,
    fw.title,
    fw.description,
    COALESCE (
       ARRAY_AGG(
           DISTINCT (p.full_name)
       ) FILTER (WHERE pfw.role = 'director'),
       '{}'
   ) as director,
   COALESCE (
       ARRAY_AGG(
           DISTINCT (p.full_name)
       ) FILTER (WHERE pfw.role = 'actor'),
       '{}'
   ) as actors_names,
     COALESCE (
       ARRAY_AGG(
           DISTINCT (p.full_name)
       ) FILTER (WHERE pfw.role = 'writer'),
       '{}'
   ) as writers_names,
    COALESCE (
       JSON_AGG(
           DISTINCT JSONB_BUILD_OBJECT(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE pfw.role = 'actor'),
       '[]'
   ) as actors,
    COALESCE (
       JSON_AGG(
           DISTINCT JSONB_BUILD_OBJECT(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE pfw.role = 'writer'),
       '[]'
   ) as writers
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON gfw.genre_id = g.id
WHERE fw.id IN %s
GROUP BY fw.id
ORDER BY fw.updated_at ASC;
'''

first_film_work_query: str = '''
SELECT fw.updated_at AS date
FROM content.film_work fw
ORDER BY date ASC;
'''