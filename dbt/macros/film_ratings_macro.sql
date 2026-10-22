{% macro generate_film_ratings() %}

WITH films_with_ratings AS (
    SELECT
        film_id,
        title,
        release_date,
        price,
        rating,
        user_rating,
        CASE
            WHEN user_rating >= 4.5 THEN 'Excellent'
            WHEN user_rating >= 4.0 THEN 'Good'
            WHEN user_rating >= 3.0 THEN 'Average'
            ELSE 'Poor'
        END AS rating_category
    FROM {{ ref('films') }}
),

films_with_actors AS (
    SELECT
        f.film_id,
        STRING_AGG(a.actor_name, ', ') AS actors,
        COUNT(a.actor_id) AS actor_count,
        AVG(f.user_rating) AS avg_actor_rating  -- use film.user_rating if actors has no rating
    FROM {{ ref('films') }} f
    LEFT JOIN {{ ref('film_actors') }} fa ON f.film_id = fa.film_id
    LEFT JOIN {{ ref('actors') }} a ON fa.actor_id = a.actor_id
    GROUP BY f.film_id
)

SELECT
    fwf.film_id,
    fwf.title,
    fwf.release_date,
    fwf.price,
    fwf.rating,
    fwf.user_rating,
    fwf.rating_category,
    fwa.actors,
    fwa.actor_count,
    fwa.avg_actor_rating
FROM films_with_ratings fwf
LEFT JOIN films_with_actors fwa
    ON fwf.film_id = fwa.film_id

{% endmacro %}