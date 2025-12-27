# Smart-Nearby-Places-App
Smart Nearby Places Recommender is a Python-based analytics app that recommends nearby places by user mood and evaluates ranking strategies using A/B testing, real-time analytics, and statistical significance testing.

## 🚀 Live Demo (Local)
```bash
streamlit run frontend_app.py


🧠 Key Features

🎯 Recommendation Engine

Mood-based recommendations (Work, Date, Quick Bite, Budget)

Scoring model using:

Ratings

Distance

Availability

Two ranking strategies (A/B variants)

🧪 A/B Testing & Experimentation

Experiment A: Distance-first ranking

Experiment B: Score-based ranking

User assignment via deterministic logic

Live comparison of variants

📊 Advanced Analytics

Click tracking in MySQL

Conversion rate & lift analysis

Distance sensitivity

Mood × Variant interaction

Statistical significance testing (z-test)

📈 Live Dashboard

Real-time metrics

Animated charts

Experiment maturity indicator

P-value monitoring

🎨 Product-Grade UI

Dark / Light theme toggle

Hover animations

Color-coded experiment variants

High-contrast recommendation cards

🛠 Tech Stack
Layer	Tools
Frontend -->	Streamlit (Python)
Backend	-->Python
Database-->	MySQL
Maps Data-->	OpenStreetMap (Nominatim)
Analytics-->	Pandas, NumPy
Statistics--> SciPy
ORM--> 	SQLAlchemy
