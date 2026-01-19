import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
from pathlib import Path

## Define project paths

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "orders_raw.csv"

## Create folder for plots 

PLOTS_PATH = PROJECT_ROOT / "plots"
PLOTS_PATH.mkdir(exist_ok=True)

## Paths for processed (final) dataset

PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed"
OUTPUT_CUSTOMER_FILE = PROCESSED_DATA_PATH / "customer_segments.csv"

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

## Visualization 

# Customer segment distribution (bar chart)

segment_count = customer_df["customer_segment"].value_counts()

plt.figure(figsize=(10, 5))
segment_count.plot(kind="bar")
plt.title("Customer segment distribution")
plt.xlabel("Customer segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(PLOTS_PATH / "customer_segment_distribution.png", dpi=300)
plt.show()
plt.close()

# Revenue distribution by segment (boxplot)

plt.figure(figsize=(10, 5))
sns.boxplot(
    data=customer_df,
    x="customer_segment",
    y="total_revenue"
)
plt.title("Revenue distribution by customer")
plt.xlabel("Customer segment")
plt.ylabel("Total revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(PLOTS_PATH / "revenue_distribution_by_segment.png", dpi=300)
plt.show()
plt.close()

# Revenue share by segment (pie chart)

revenue_by_segment = (
    customer_df
    .groupby("customer_segment")["total_revenue"]
    .sum()
    .sort_values(ascending=False)
)
plt.figure(figsize=(8, 8))
revenue_by_segment.plot(kind="pie")
plt.title("Revenue share by customer segment")
plt.ylabel("")
plt.tight_layout()

plt.savefig(PLOTS_PATH / "revenue_share_by_segment.png", dpi=300)
plt.show()
plt.close()

## Save final customer-level dataset

PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

customer_df.to_csv(OUTPUT_CUSTOMER_FILE, index=False)

print("\n*** FINAL DATA SAVED ***")
print("File:", OUTPUT_CUSTOMER_FILE)
print("Rows:", len(customer_df))
print("Columns:", list(customer_df.columns))