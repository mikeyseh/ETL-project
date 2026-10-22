WITH ranked_actors AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY actor_id ORDER BY actor_id) AS rn
    FROM {{ source('destination_db', 'actors') }}
)
SELECT *
FROM ranked_actors
WHERE rn = 1
