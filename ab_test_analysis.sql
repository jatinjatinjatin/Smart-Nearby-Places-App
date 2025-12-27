WITH experiment_data AS (
  SELECT *,
  CASE WHEN user_id % 2 = 0 THEN 'Variant A' ELSE 'Variant B' END AS experiment_group
  FROM user_events
)
SELECT experiment_group,
COUNT(CASE WHEN event_type='place_click' THEN 1 END)/COUNT(*) AS ctr
FROM experiment_data
GROUP BY experiment_group;
