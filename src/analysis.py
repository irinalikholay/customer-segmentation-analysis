import pandas as pd 
from pathlib import Path

## Define project paths

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "orders_raw.csv"

## Load raw data 

df = pd.read_csv(RAW_DATA_PATH)

## Convert order date to datetime

df["order_date"] = pd.to_datetime(df["order_date"])

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

## Aggregate orders to customer level 

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

## Edge cases check

print("\n*** EDGE CASES CHECK ***")

one_order_customers = customer_df[customer_df["orders_count"] == 1]
zero_revenue_customers = customer_df[customer_df["total_revenue"] == 0]

high_value_threshold = customer_df["total_revenue"].quantile(0.99)
high_value_customers = customer_df[
    customer_df["total_revenue"] >= high_value_threshold
]

print("One-order customers:", len(one_order_customers))
print("Zero-revenue customers:", len(zero_revenue_customers))
print("High-value customers (top 1%):", len(high_value_customers))
print("High-value revenue threshold:", round(high_value_threshold, 2))

## Add edge case flag

customer_df["is_one_order"] = customer_df["orders_count"] == 1
customer_df["is_zero_revenue"] = customer_df["total_revenue"] == 0
customer_df["is_high_value"] = (
    customer_df["total_revenue"] >= high_value_threshold
)

print("\n*** EDGE CASE FLAGS (counts) ***")
print("Is one order:", customer_df["is_one_order"].sum())
print("Is zero revenue:", customer_df["is_zero_revenue"].sum())
print("Is high value:", customer_df["is_high_value"].sum())

## Distribution

print("\n*** DISTRIBUTION: ORDERS COUNT ***")
print(customer_df["orders_count"].describe())

print("\n*** DISTRIBUTION: TOTAL REVENUE ***")
print(customer_df["total_revenue"].describe())

print("\n*** DISTRIBUTION: AVG ORDER VALUE ***")
print(customer_df["avg_order_value"].describe())

## Customer segmentation

print("\n*** CUSTOMER SEGMENTATION ***")

print("\n*** Order count ***")

def activity_segment(x):
    if x == 1:
        return "one order"
    elif 2 <= x <= 4:
        return "repeat"
    else:
        return "loyal"
    
customer_df["activity_segment"] = customer_df["orders_count"].apply(activity_segment)

print("\nActivity segment distribution:")
print(customer_df["activity_segment"].value_counts())

print("\n*** Revenue ***")

revenue_q50 = customer_df["total_revenue"].quantile(0.5)
revenue_q75 = customer_df["total_revenue"].quantile(0.75)

def value_segment(x):
    if x <= revenue_q50:
        return "low value"
    elif x <= revenue_q75:
        return "mid value"
    else:
        return "high value"
    
customer_df["value_segment"] = customer_df["total_revenue"].apply(value_segment)

print("\nValue segment distribution:")
print(customer_df["value_segment"].value_counts())

print("\n*** Combined ***")

customer_df["customer_segment"] = (
    customer_df["activity_segment"] + "_" + customer_df["value_segment"]
)

print("\nCombined customer segments:")
print(customer_df["customer_segment"].value_counts(10))

