import pandas as pd 
from pathlib import Path

## Define project paths

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "orders_raw.csv"

## Load raw data 

df = pd.read_csv(RAW_DATA_PATH)

## Basic structure check 

print("\*** BASIC INFO ***")
print(df.info())

print("\n*** FIRST ROWS ***")
print(df.head())

## Sanity check 

print("\n*** DATA SANITY CHECK ***")

print("Total rows:", len(df))
print("Unique customers:", df["customer_id"].nunique())
print("Min revenue:", df["revenue"].min())
print("Max revenue:", df["revenue"].max())

print("\n*** Orders per customer (describe):")
order_per_customer = df.groupby("customer_id").size()
print(order_per_customer.describe())

# Aggregate orders to customer level 

customer_df = (
    df
    .groupby("customer_id")
    .agg(
        orders_count=("revenue", "count"),
        total_revenue=("revenue", "sum"),
        avg_order_value=("revenue", "mean"),
        first_order_date=("order_date", "min"),
        last_order_date=("order_date", "max"),
    )
    .reset_index()
)

print("\n*** CUSTOMER LEVEL TABLE ***")
print(customer_df.head())