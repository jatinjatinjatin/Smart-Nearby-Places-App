import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Ensure data directory exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)

users = range(1, 101)
moods = ['work', 'date', 'quick_bite', 'budget']
rows = []

for _ in range(2000):
    rows.append({
        'user_id': random.choice(users),
        'event_type': 'place_click',
        'mood': random.choice(moods),
        'place_id': f'place_{random.randint(1, 300)}',
        'rating': round(np.random.uniform(3.0, 5.0), 1),
        'distance_km': round(np.random.exponential(1.5), 2),
        'price_level': random.choice([1, 2, 3]),
        'is_open': random.choice([True, False]),
        'event_time': datetime.now() - timedelta(minutes=random.randint(1, 20000))
    })

df = pd.DataFrame(rows)

output_path = os.path.join(DATA_DIR, "fake_user_events.csv")
df.to_csv(output_path, index=False)

print(f"✅ Fake user data generated successfully at: {output_path}")
