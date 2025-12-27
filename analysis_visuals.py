import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/fake_user_events.csv')
df.groupby('mood')['distance_km'].mean().plot(kind='bar')
plt.title('Average Distance by Mood')
plt.show()
