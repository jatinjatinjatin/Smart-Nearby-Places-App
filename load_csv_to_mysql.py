import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://analytics_user:analytics123@localhost/recommender_analytics"
)

df = pd.read_csv("data/fake_user_events.csv")

df.to_sql(
    "user_events",
    engine,
    if_exists="append",
    index=False
)

print("✅ CSV loaded into MySQL")
