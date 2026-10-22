WITH ranked_film_actors AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY actor_id, film_id ORDER BY actor_id) AS rn
    FROM {{ source('destination_db', 'film_actors') }}
)
SELECT *
FROM ranked_film_actors
WHERE rn = 1
