# Requirements Reference

## Platform

- Python + PySpark
- Databricks
- ADLS Gen2 storage account `cdl`
- Unity Catalog
- Parquet files

## Source

Sales source fields: Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City.

## Bronze

- Read source Parquet.
- Normalize source names to snake_case.
- Add `file_path` and `execution_datetime`.
- Add `order_year`, `order_month`, `order_day`.
- Write Parquet partitioned by the date parts.

## Silver

- Read Bronze Parquet.
- Mandatory: `order_id`, `customer_id`, `order_date`.
- `ship_date` may be null; if present it cannot be before `order_date`.
- Trim string business columns on `Customer Name`
- Refresh execution metadata/date partitions.
- Write Parquet partitioned by date parts.

## Gold Sales

- Business columns: `order_id`, `order_date`, `shipment_date`, `shipment_mode`, `city`.
- Keep operational metadata and partition columns.
- Write partitioned Parquet.

## Gold Customer

- One row per customer.
- Full overwrite each execution.
- `customer_id`, first name, last name, segment, country.
- Distinct order counts for last 1, 6, 12 months and all time.
- Anchor rolling windows to dataset maximum order date.
- Do not date-partition Customer Gold because Order Date is not part of the Customer grain.

## Testing

Cover read, write, wrong path, transformations, edge cases, Gold Sales columns, customer-name splitting, and Gold Customer metrics.
