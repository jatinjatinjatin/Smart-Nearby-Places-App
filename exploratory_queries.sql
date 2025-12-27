SELECT mood, COUNT(*) AS total_interactions
FROM user_events
GROUP BY mood
ORDER BY total_interactions DESC;

SELECT mood,
       ROUND(AVG(distance_km),2) AS avg_distance_km,
       ROUND(AVG(rating),2) AS avg_rating
FROM user_events
WHERE event_type='place_click'
GROUP BY mood;

SELECT
  CASE
    WHEN distance_km < 1 THEN '<1 km'
    WHEN distance_km < 3 THEN '1–3 km'
    ELSE '3+ km'
  END AS distance_bucket,
  COUNT(*) AS clicks
FROM user_events
WHERE event_type='place_click'
GROUP BY distance_bucket;
