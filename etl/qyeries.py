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