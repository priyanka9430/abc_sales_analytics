# ABC Sales Data Engineering - Requirement Summary

## Business case

A sales dataset is provided to a new ABC data engineer. Build an end-to-end ETL pipeline in **Python/PySpark** that ingests the dataset into a Data Lake, applies transformations and business rules, and produces final Sales and Customer datasets.

## Source schema

The test/source dataset contains:

- Row ID
- Order ID
- Order Date
- Ship Date
- Ship Mode
- Customer ID
- Customer Name
- Segment
- Country
- City

## Technical requirements

1. Use Medallion Architecture: **Bronze -> Silver -> Gold**.
2. Store Data Lake datasets as **Parquet**.
3. Implement ingestion and transformations using **Python + PySpark**.
4. Carry metadata such as `file_path` and `execution_datetime` in each layer.
5. Use consistent logging that supports debugging.
6. Partition order-grained datasets by `order_year`, `order_month`, `order_day` derived from Order Date.
7. Normalize column names to `snake_case`.
8. Package the solution as an installable Python project.
9. Use modularization, error handling, reusable code, and engineering best practices.
10. Separate pipeline stages so failures are easier to isolate and rerun.

## Functional requirements

### Gold Sales

Business columns:

- `order_id`
- `order_date`
- `shipment_date`
- `shipment_mode`
- `city`

The implementation may additionally keep required operational metadata and partition columns.

### Gold Customer

One row per customer, rewritten on every pipeline execution, containing:

- `customer_id`
- `customer_first_name`
- `customer_last_name`
- `customer_segment`
- `country`
- quantity of orders in the last 1 month
- quantity of orders in the last 6 months
- quantity of orders in the last 12 months
- total quantity of orders for all time

The assignment uses **30-Dec-2018** as the reference latest date. The implementation should calculate the maximum `order_date` dynamically so it continues to work when new data arrives.

## README-derived business rules / assumptions

- `order_id`, `customer_id`, and `order_date` are mandatory.
- `ship_date` may be null.
- If present, `ship_date >= order_date`.
- "Quantity of orders" means `countDistinct(order_id)`.
- ADLS Gen2 storage account: `cdl`.
- Use Unity Catalog table registration when enabled.

## Required tests

At minimum cover:

- valid Parquet read
- Parquet write/read round-trip
- wrong file path
- Bronze normalization/metadata
- Silver filtering/transformation
- customer-name split, including single-name edge case
- Gold Sales required columns
- Gold Customer rolling metrics
