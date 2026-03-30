import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:YOUR_PASSWORD@localhost:5432/king_county_db"
)

df = pd.read_csv("./data/raw/kc_house_data.csv")
df.to_sql("house_sales", engine, if_exists="replace", index=False)
print(f"house_sales — {len(df):,} rows loaded")
print("\nAll tables loaded.")
