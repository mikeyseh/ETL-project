WITH ranked_films AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY film_id ORDER BY film_id) AS rn
    FROM {{ source('destination_db', 'films') }}
)
SELECT *
FROM ranked_films
WHERE rn = 1