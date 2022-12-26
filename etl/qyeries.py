genres = '''
SELECT gfw.film_work_id
FROM content.genre g
LEFT JOIN content.genre_film_work gfw ON gfw.genre_id = g.id
WHERE g.updated_at > '%s'
ORDER BY g.updated_at
'''

persons = '''
SELECT pfw.film_work_id
FROM content.person p
LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
WHERE p.updated_at > '%s'
ORDER BY p.updated_at
'''

film_work = '''
SELECT
    fw.id,
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
       ) FILTER (WHERE pfw.role = 'writer'),
       '{}'
   ) as writers_names,
    COALESCE (
       ARRAY_AGG(
           DISTINCT (p.full_name)
       ) FILTER (WHERE pfw.role = 'actor'),
       '{}'
   ) as actors_names,
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
WHERE fw.updated_at >= '%s'
GROUP BY fw.id
ORDER BY fw.updated_at;
'''