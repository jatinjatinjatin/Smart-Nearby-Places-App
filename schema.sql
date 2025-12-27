CREATE DATABASE IF NOT EXISTS recommender_analytics;
USE recommender_analytics;

CREATE TABLE IF NOT EXISTS user_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(50),
    mood VARCHAR(20),
    place_id VARCHAR(255),
    rating FLOAT,
    distance_km FLOAT,
    price_level INT,
    is_open BOOLEAN,
    experiment_group VARCHAR(1),
    recommendation_score FLOAT,
    event_time DATETIME
);
