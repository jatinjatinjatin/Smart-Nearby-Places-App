-- A/B test performance
SELECT experiment_group, COUNT(*) AS clicks
FROM user_events
GROUP BY experiment_group;

-- Mood behavior
SELECT mood, COUNT(*) AS clicks
FROM user_events
GROUP BY mood;

-- Average recommendation score
SELECT mood, ROUND(AVG(recommendation_score),2) AS avg_score
FROM user_events
GROUP BY mood;

-- Power users
SELECT user_id, COUNT(*) AS events,
DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS rank_
FROM user_events
GROUP BY user_id
LIMIT 10;
