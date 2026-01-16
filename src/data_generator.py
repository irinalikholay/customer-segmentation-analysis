from pathlib import Path

import numpy as np

import pandas as pd



# paths

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"

RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)



OUTPUT_FILE = RAW_DATA_PATH / "orders_raw.csv"



# reproducibility

np.random.seed(42)



# customers

N_CUSTOMERS = 5000

customer_ids = np.arange(1, N_CUSTOMERS + 1)



orders = []



for customer_id in customer_ids:

    orders_count = np.random.choice(

        [1, 2, 3, 5, 10, 20],

        p=[0.30, 0.25, 0.20, 0.15, 0.07, 0.03]

    )



    for _ in range(orders_count):

        order_date = (

            pd.Timestamp("2023-01-01")

            + pd.to_timedelta(np.random.randint(0, 365), unit="D")

        )



        revenue = np.random.normal(100, 30)

        revenue = max(round(revenue, 2), 0)



        orders.append((customer_id, order_date, revenue))



df = pd.DataFrame(

    orders,

    columns=["customer_id", "order_date", "revenue"]

)



df.to_csv(OUTPUT_FILE, index=False)



print("OK")

print("customers:", df["customer_id"].nunique())

print("rows:", len(df))

print("file:", OUTPUT_FILE)