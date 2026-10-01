# ABC Sales Data Engineering Assignment

## 1. Project Overview

This project implements a simple end-to-end sales data pipeline using **Python, PySpark, Databricks, ADLS Gen2, and Unity Catalog**.

The goal is to ingest sales data from an ADLS Gen2 landing location, transform the data through **Bronze, Silver, and Gold** layers, and create two final Gold datasets:

- `gold_sales`
- `gold_customer`

The solution is intentionally kept simple and modular so that the code is easy to understand, test, maintain, and explain during an interview.

This implementation uses **normal Python/PySpark functions** instead of DLT/Lakeflow decorators.

---

## 2. Technology Stack

| Component | Purpose |
|---|---|
| Python | Main programming language |
| PySpark | Distributed data processing |
| Databricks | Compute and job orchestration |
| ADLS Gen2 | Data lake storage |
| Unity Catalog | Table governance and access management |
| Parquet | Storage file format |
| Databricks Workflows | Job scheduling |
| Pytest | Unit testing |
| Python Logging | Operational logging |

---

## 3. High-Level Architecture

```text
                 Source System
                      |
                      v
              ADLS Gen2 Landing
              Parquet Sales Files
                      |
                      v
          Unity Catalog External Volume
                      |
                      v
              Databricks PySpark Job
                      |
                      v
                 BRONZE LAYER
                bronze_sales
                      |
                      v
                 SILVER LAYER
                silver_sales
                      |
                +-----+-----+
                |           |
                v           v
          GOLD SALES   GOLD CUSTOMER
          gold_sales   gold_customer
```

### Component Responsibilities

**ADLS Gen2**
- Stores source files.
- Stores Bronze, Silver, and Gold datasets.

**Unity Catalog**
- Governs access to tables and storage locations.
- Provides centralized metadata and security.

**Databricks**
- Executes the PySpark transformations.
- Schedules the pipeline using Databricks Workflows.

---

## 4. Source Data

The input sales dataset contains:

| Source Column | Description |
|---|---|
| Row ID | Unique identifier for the source row |
| Order ID | Order number |
| Order Date | Order creation date |
| Ship Date | Shipping date |
| Ship Mode | Shipping method |
| Customer ID | Customer identifier |
| Customer Name | Customer full name |
| Segment | Customer segment |
| Country | Customer country |
| City | Customer city |

Source files are expected to be stored in **Parquet format** in ADLS Gen2.

Example source path exposed through a Unity Catalog external Volume:

```text
/Volumes/abc_sales/landing/sales_files
```

---

## 5. Medallion Architecture

### 5.1 Bronze Layer

The Bronze layer contains source data with minimal transformation.

Main responsibilities:
- Read source Parquet files.
- Rename columns to `snake_case`.
- Convert date columns to Spark `date` type.
- Add metadata columns.
- Add partition columns.

Example renaming:

```text
Order ID       -> order_id
Customer Name  -> customer_name
Ship Mode      -> ship_mode
```

Metadata columns:

```text
file_path
execution_datetime
```

Partition columns:

```text
order_year
order_month
order_day
```

---

### 5.2 Silver Layer

The Silver layer contains cleaned and validated data.

Main responsibilities:
- Validate mandatory fields.
- Validate shipping date logic.
- Trim customer names.
- Split customer name into first and last name.

Example:

```text
customer_name = "Ravi Kumar Singh"

customer_first_name = "Ravi"
customer_last_name  = "Kumar Singh"
```

The following validation rules are included as **project assumptions**, because they were not explicitly provided in the assignment:

```text
order_id must not be null
customer_id must not be null
order_date must not be null
ship_date must be null or greater than/equal to order_date
```

---

### 5.3 Gold Sales

The Gold Sales dataset contains the final order-level attributes requested in the assignment.

Columns:

```text
order_id
order_date
shipment_date
shipment_mode
city
file_path
execution_datetime
order_year
order_month
order_day
```

Mapping:

```text
ship_date -> shipment_date
ship_mode -> shipment_mode
```

---

### 5.4 Gold Customer

The Gold Customer dataset contains one customer-level record with order metrics.

Required attributes:

```text
customer_id
customer_first_name
customer_last_name
customer_segment
country
orders_last_1_month
orders_last_6_months
orders_last_12_months
orders_all_time
```

The assignment specifies the latest date in the dataset as:

```text
2018-12-30
```

This date is used as the reference date for rolling metrics.

Example windows:

```text
Last 1 month:
2018-11-30 to 2018-12-30

Last 6 months:
2018-06-30 to 2018-12-30

Last 12 months:
2017-12-30 to 2018-12-30
```

Order quantity is calculated using:

```python
F.countDistinct("order_id")
```

This is used because the source dataset does not contain a separate quantity field.

For this assignment, the project assumes that customer name, segment, and country remain consistent for a given `customer_id`.

---

## 6. Project Structure

```text
abc-sales/
|
├── README.md
├── pyproject.toml
|
├── sql/
│   └── 01_unity_catalog_setup.sql
|
├── src/
│   └── abc_sales/
│       ├── __init__.py
│       ├── config.py
│       ├── schemas.py
│       ├── io_utils.py
│       ├── transformations.py
│       └── main.py
|
└── tests/
    ├── conftest.py
    ├── test_io.py
    └── test_transformations.py
```

### File Explanation

#### `config.py`
Contains catalog, schema, source path, target paths, table names, and partition columns.

#### `schemas.py`
Contains the explicit PySpark schema for source data.

#### `io_utils.py`
Contains reusable read and write functions:
```python
read_parquet()
write_parquet_table()
```

#### `transformations.py`
Contains:
```python
to_bronze()
to_silver()
to_gold_sales()
to_gold_customer()
```

#### `main.py`
Controls the end-to-end execution sequence.

---

## 7. Pipeline Execution Flow

```python
source_df = read_parquet(...)

bronze_df = to_bronze(source_df)

silver_df = to_silver(bronze_df)

gold_sales_df = to_gold_sales(silver_df)

gold_customer_df = to_gold_customer(silver_df)
```

Each result is written back to ADLS and registered in Unity Catalog.

---

## 8. Read and Write Strategy

### Read

```python
spark.read.parquet(...)
```

An explicit schema is applied during ingestion.

### Write

```python
df.write     .format("parquet")     .mode("overwrite")     .option("path", target_path)     .saveAsTable(table_name)
```

The assignment requests Parquet, so Parquet is used throughout this implementation.

For simplicity, the assignment version uses **overwrite mode**. This makes reruns deterministic and ensures the Customer dataset is rewritten on every execution.

In production, Bronze could later be changed to incremental Auto Loader ingestion with checkpointing.

---

## 9. Partitioning Strategy

Transactional tables are partitioned by:

```text
order_year
order_month
order_day
```

Applied to:
```text
bronze_sales
silver_sales
gold_sales
```

The Gold Customer table is not partitioned by order date because its grain is one row per customer.

---

## 10. Logging

The project uses Python logging:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("abc_sales")
```

Example:

```python
logger.info("Reading source data")
logger.info("Creating Bronze layer")
logger.info("Creating Silver layer")
logger.info("Creating Gold Sales")
logger.info("Creating Gold Customer")
logger.info("Pipeline completed successfully")
```

Errors are logged using:

```python
logger.exception("Pipeline failed")
```

This includes the error message and stack trace.

---

## 11. Error Handling

The main pipeline is wrapped in `try/except`:

```python
try:
    # pipeline logic

except Exception:
    logger.exception("Pipeline failed")
    raise
```

The exception is raised again so Databricks marks the job as failed.

---

## 12. Unit Testing

The project uses `pytest`.

Tests cover:
- Successful Parquet read.
- Wrong file path.
- Silver transformation.
- Customer name split.
- Gold Sales columns.
- Gold Customer metrics.
- Edge cases.

Run:

```bash
pytest -v
```

---

## 13. Setup

### Step 1: Configure ADLS Gen2

Create folders/containers for:

```text
landing
bronze
silver
gold
```

### Step 2: Configure Unity Catalog

Create:

```text
Catalog: abc_sales

Schemas:
abc_sales.landing
abc_sales.sales
```

Example external Volume:

```sql
CREATE EXTERNAL VOLUME IF NOT EXISTS abc_sales.landing.sales_files
LOCATION 'abfss://landing@<storage-account>.dfs.core.windows.net/abc_sales/sales';
```

### Step 3: Update `config.py`

Example:

```python
SOURCE_PATH = "/Volumes/abc_sales/landing/sales_files"

BRONZE_PATH = "abfss://bronze@<storage-account>.dfs.core.windows.net/abc_sales/sales"

SILVER_PATH = "abfss://silver@<storage-account>.dfs.core.windows.net/abc_sales/sales"

GOLD_SALES_PATH = "abfss://gold@<storage-account>.dfs.core.windows.net/abc_sales/sales"

GOLD_CUSTOMER_PATH = "abfss://gold@<storage-account>.dfs.core.windows.net/abc_sales/customer"
```

---

## 14. Running in Databricks

Databricks already provides a Spark session named `spark`.

Run:

```python
from abc_sales.main import run_pipeline

run_pipeline(spark)
```

No separate `SparkSession` creation is needed when running inside a Databricks notebook.

---

## 15. Scheduling with Databricks Workflows

1. Open **Databricks Workflows**.
2. Create a Job.
3. Add a Python task.
4. Configure the task to run the project.
5. Select the compute.
6. Add a schedule.

Example:

```text
Daily at 2:00 AM
```

---

## 16. Assumptions

The following assumptions are documented because they are not all explicitly stated in the use case:

1. `order_id`, `customer_id`, and `order_date` are mandatory.
2. `ship_date` can be null.
3. When present, `ship_date` cannot be earlier than `order_date`.
4. Order quantity means `count(distinct order_id)`.
5. Customer name, segment, and country remain consistent for each customer.
6. The reference date is `2018-12-30`, as specified in the assignment.
7. The assignment version uses full overwrite mode for simple reruns.

These assumptions should be confirmed with the business team in a production implementation.

---

## 17. Possible Production Enhancements

Future improvements could include:
- Auto Loader for incremental Bronze ingestion.
- Checkpointing.
- Delta Lake instead of plain Parquet.
- Quarantine table for invalid records.
- Audit/control table with row counts and job status.
- Schema evolution handling.
- Config-driven business rules.
- Databricks Asset Bundles.
- CI/CD across Dev, Test, and Prod.
- Pipeline failure alerts.
- Slowly Changing Dimensions for changing customer attributes.

---

## 18. CI/CD Approach

```text
Developer commit
      |
      v
Git repository
      |
      v
Run linting
      |
      v
Run unit tests
      |
      v
Package application
      |
      v
Deploy to Databricks DEV
      |
      v
Promote to TEST / PROD
```

Possible tools:
- GitHub or Azure DevOps
- Pytest
- Databricks CLI
- Databricks Asset Bundles

---

## 19. Key Design Decisions

### Why normal PySpark functions?

Normal functions such as:

```python
to_bronze()
to_silver()
to_gold_sales()
to_gold_customer()
```

make the code easier to understand, test, reuse, and explain.

### Why Unity Catalog?

Unity Catalog provides centralized governance for tables, volumes, external storage, access control, and metadata.

### Why `countDistinct(order_id)`?

The source does not contain a quantity field.

Example:

```text
O100
O100
O101
```

There are three rows but only two distinct orders, so:

```python
F.countDistinct("order_id")
```

returns `2`.

---

## 20. Simple Interview Explanation

> The source sales files are stored in ADLS Gen2 in Parquet format and exposed to Databricks through a Unity Catalog external Volume. A Databricks PySpark job reads the files and processes them through Bronze, Silver, and Gold layers. Bronze standardizes the source structure and adds metadata, Silver performs data cleaning and validation, and Gold produces Sales and Customer business datasets. The Gold Customer table calculates one-, six-, twelve-month, and all-time distinct order counts using the reference date specified in the assignment. The datasets are written back to ADLS and registered in Unity Catalog. Python logging is used for monitoring, Pytest is used for testing, and Databricks Workflows schedules the pipeline.

---

## 21. Summary

This solution demonstrates:

- Medallion architecture
- ADLS Gen2 storage
- Unity Catalog governance
- Parquet storage
- Python and PySpark
- Metadata columns
- Date-based partitioning
- Gold Sales and Customer datasets
- Logging
- Error handling
- Unit testing
- Modular code
- Databricks scheduling
- CI/CD recommendations
