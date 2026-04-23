import sqlite3
import pandas as pd

conn = sqlite3.connect("ipl.db")

final_df = pd.read_csv("final_df.csv")

final_df.to_sql("final_df", conn, if_exists="replace", index=False)

print("Database created successfully")