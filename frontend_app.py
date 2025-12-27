import streamlit as st
import pandas as pd
import random
import requests
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine
from scipy.stats import norm

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Smart Nearby Places", layout="wide")

# ================= THEME TOGGLE =================
theme = st.toggle("🌈 Light / Dark Mode", value=False)

if theme:  # Light mode
    bg = "#f9fafb"
    card_bg = "#ffffff"
    text = "#111827"
else:      # Dark mode
    bg = "#0f1117"
    card_bg = "#111827"
    text = "#f9fafb"

# ================= GLOBAL STYLES =================
st.markdown(f"""
<style>
body {{
    background-color: {bg};
    color: {text};
}}

h1 {{
    font-size: 3rem !important;
    font-weight: 800 !important;
}}

h2, h3 {{
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}}

/* Recommendation card */
.reco-card {{
    background: {card_bg};
    border-left: 6px solid;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.reco-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.45);
}}

.reco-title {{
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 12px;
}}

.reco-metric {{
    font-size: 1.3rem;
    font-weight: 600;
    margin: 6px 0;
}}

.reco-metric span {{
    font-weight: 800;
}}

.exp-A {{
    border-color: #3b82f6;
}}

.exp-B {{
    border-color: #22c55e;
}}

.exp-A span {{
    color: #3b82f6;
}}

.exp-B span {{
    color: #22c55e;
}}
</style>
""", unsafe_allow_html=True)

# ================= DB CONNECTION =================
engine = create_engine(
    "mysql+pymysql://analytics_user:analytics123@localhost/recommender_analytics"
)

# ================= HELPERS =================
def assign_experiment_group(user_id):
    return "A" if user_id % 2 == 0 else "B"

def compute_score(row):
    distance_score = max(0, 5 - row["Distance (km)"])
    open_score = 1 if row["Open Now"] else 0
    return 0.5 * row["Rating"] + 0.3 * distance_score + 0.2 * open_score

def fetch_places(keyword, city="San Francisco"):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": f"{keyword} in {city}", "format": "json", "limit": 8}
    headers = {"User-Agent": "SmartNearbyPlacesApp"}
    res = requests.get(url, params=params, headers=headers).json()

    if not res:
        return []

    return [{
        "Place": p.get("display_name", "").split(",")[0],
        "Rating": round(random.uniform(3.5, 4.8), 1),
        "Distance (km)": round(random.uniform(0.3, 3.5), 2),
        "Open Now": random.choice([True, False])
    } for p in res]

def log_event(row, mood, group):
    pd.DataFrame([{
        "user_id": random.randint(1, 100),
        "event_type": "place_click",
        "mood": mood,
        "place_id": row["Place"],
        "rating": row["Rating"],
        "distance_km": row["Distance (km)"],
        "price_level": 2,
        "is_open": row["Open Now"],
        "experiment_group": group,
        "recommendation_score": row["score"],
        "event_time": datetime.now()
    }]).to_sql("user_events", engine, if_exists="append", index=False)

def ab_significance_test(a, b):
    total = a + b
    if total == 0:
        return None
    p_pool = total / (2 * total)
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / total))
    z = (b - a) / se if se != 0 else 0
    return 1 - norm.cdf(abs(z))

# ================= UI =================
st.title("📍 Smart Nearby Places Recommender")

mood_map = {
    "Work 💻": "cafe",
    "Date ❤️": "restaurant",
    "Quick Bite 🍔": "fast food",
    "Budget 💸": "restaurant"
}

mood_label = st.selectbox("Choose your mood", list(mood_map.keys()))
keyword = mood_map[mood_label]
mood = mood_label.split()[0].lower()

df = pd.DataFrame(fetch_places(keyword))

if df.empty:
    st.warning("⚠️ No places found for this mood.")
    st.stop()

df["score"] = df.apply(compute_score, axis=1)

user_id = random.randint(1, 100)
exp = assign_experiment_group(user_id)

df = df.sort_values("score" if exp == "B" else ["Distance (km)", "Rating"],
                    ascending=False if exp == "B" else True).reset_index(drop=True)

top = df.iloc[0]

# ================= TOP RECOMMENDATION =================
st.subheader(f"🏆 Top Recommendation (Experiment {exp})")

st.markdown(f"""
<div class="reco-card exp-{exp}">
  <div class="reco-title">{top['Place']}</div>
  <div class="reco-metric">⭐ Rating: <span>{top['Rating']}</span></div>
  <div class="reco-metric">📍 Distance: <span>{top['Distance (km)']} km</span></div>
  <div class="reco-metric">📊 Score: <span>{round(top['score'],2)}</span></div>
</div>
""", unsafe_allow_html=True)

if st.button("Log Interaction"):
    log_event(top, mood, exp)
    st.success("✅ Interaction logged")

# ================= LIVE ANALYTICS =================
st.subheader("📊 Live Analytics")

ab = pd.read_sql("""
SELECT experiment_group, COUNT(*) clicks
FROM user_events
GROUP BY experiment_group
""", engine)

a = ab.loc[ab.experiment_group == "A", "clicks"].sum()
b = ab.loc[ab.experiment_group == "B", "clicks"].sum()
p = ab_significance_test(a, b)

c1, c2, c3 = st.columns(3)
c1.metric("Variant A Clicks", a)
c2.metric("Variant B Clicks", b)
c3.metric("P-value", f"{p:.4f}" if p else "N/A")

st.progress(min((a + b) / 50, 1.0), text="Experiment maturity")

score_df = pd.read_sql("""
SELECT mood, AVG(recommendation_score) avg_score
FROM user_events
GROUP BY mood
""", engine)

st.bar_chart(score_df.set_index("mood"))
