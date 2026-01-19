# Customer Segmentation Analysis

## Project Overview

This project demonstrates a full end-to-end customer analytics workflow, starting from raw transactional data and ending with actionable customer segmentation and business insights.

The goal of the project is to show how raw order-level data can be transformed into a clean, interpretable customer-level dataset and used to understand customer behavior, value distribution, and revenue concentration.

The analysis follows a clear, real-world analytical workflow rather than a purely academic or notebook-style approach.


## Business Questions

The analysis focuses on answering the following questions:

- How active are customers in terms of repeat purchases?
- How is total revenue distributed across customers?
- Which customer segments generate the majority of revenue?
- How do edge cases affect aggregated metrics?
- How can customers be segmented in a transparent and business-friendly way?


## Data Preparation & Validation

Raw transactional data was loaded and validated before analysis.

Key preparation steps included:
- Verifying data structure and data types
- Converting order dates to proper datetime format
- Checking row counts and unique customer counts
- Identifying edge cases such as zero-revenue and single-order customers

This step ensured data quality and reliability for further analysis.


## Customer-Level Aggregation

Transactional order-level data was aggregated to the customer level.

For each customer, the following metrics were calculated:
- Number of orders
- Total revenue
- Average order value
- First and last order dates

This transformation shifts the analytical focus from individual transactions to customer behavior.


## Edge Case Analysis

Several customer behaviors were identified as potential edge cases:
- Customers with only one order
- Customers with zero total revenue
- High-value customers in the upper tail of the revenue distribution

Rather than removing these observations, explicit flags were added to preserve transparency and analytical control.


## Customer Segmentation

Customer segmentation was implemented using a rule-based approach with two dimensions:

**Activity-based segmentation:**
- One-time customers
- Repeat customers
- Loyal customers

**Value-based segmentation:**
- Low-value customers
- Mid-value customers
- High-value customers

These dimensions were combined into final customer segments such as:
- `one_order_low_value`
- `repeat_mid_value`
- `loyal_high_value`

This approach keeps the segmentation logic interpretable and easy to communicate to business stakeholders.


## Visualization & Analysis

Visual analysis was used to explore and validate customer segments.

Key visualizations include:
- Distribution of customers across segments
- Revenue distribution within each segment
- Revenue share contribution by segment

These visualizations highlight the concentration of revenue and the behavioral differences between customer groups.


## Final Output

The final result of the analysis is a clean, customer-level dataset that includes all calculated metrics and segment labels.

This dataset can be directly used for:
- Business intelligence dashboards
- Marketing and CRM analysis
- Strategic decision-making
- Further analytical or modeling work


## Key Insights

- Most customers place only one or two orders.
- A small group of high-value customers contributes a disproportionately large share of total revenue.
- Average metrics are strongly influenced by high-value customers and should be interpreted with caution.
- Rule-based customer segmentation provides clear, actionable insights without requiring complex models.


## Tools & Libraries

- Python
- pandas
- matplotlib
- seaborn

All dependencies are listed in `requirements.txt`.


## Final Notes

This project emphasizes analytical thinking, data quality awareness, and business interpretability over complex modeling techniques.

It reflects how real-world data analysts structure projects, reason about edge cases, and communicate insights clearly to non-technical audiences.