SELECT user_id, mood, place_id, rating, distance_km,
RANK() OVER (PARTITION BY mood ORDER BY rating DESC, distance_km ASC) AS place_rank
FROM user_events
WHERE event_type='place_click';

SELECT user_id,
COUNT(*) AS total_events,
DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS engagement_rank
FROM user_events
GROUP BY user_id;
