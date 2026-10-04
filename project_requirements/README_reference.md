# ABC Sales Data Engineering Pipeline

## Overview

This project implements a simple end-to-end sales data pipeline using **Python, PySpark, Databricks, ADLS Gen2, and Unity Catalog**.

The source sales data is stored in **ADLS Gen2 storage account `cdl`** in Parquet format. The pipeline follows a **Bronze -> Silver -> Gold** medallion architecture and creates two final Gold datasets:

- `gold_sales`
- `gold_customer`

### Main Files

- `config.py` - source/target paths, Unity Catalog table names, partition columns.
- `schemas.py` - source PySpark schema.
- `io_utils.py` - reusable Parquet read/write functions.
- `transformations.py` - Bronze, Silver, Gold Sales, and Gold Customer transformations.
- `main.py` - runs the complete pipeline.
- `tests/` - unit tests.

---

# 1. Storage Setup

The ADLS Gen2 storage account name is:

```text
cdl
```

Example ADLS paths:

```text
abfss://landing@cdl.dfs.core.windows.net/abc_sales/
abfss://bronze@cdl.dfs.core.windows.net/abc_sales/
abfss://silver@cdl.dfs.core.windows.net/abc_sales/
abfss://gold@cdl.dfs.core.windows.net/abc_sales/sales/
abfss://gold@cdl.dfs.core.windows.net/abc_sales/customer/
```

---

# 2. Setup Instructions

## Prerequisites

You need:

- Databricks workspace
- access to ADLS Gen2 storage account `cdl`
- Unity Catalog enabled
- permission to read and write required ADLS locations
- Pytest

## Upload Source Data

Place the source Parquet file in the landing location, for example:

```text
abfss://landing@cdl.dfs.core.windows.net/abc_sales/sales.parquet
```

---

# 3. How to Run the Tool

Run the pipeline using:

```python
from abc_sales.main import run_pipeline

run_pipeline(spark)
```

## Schedule in Databricks

Use Databricks Workflows:

1. Open Workflows.
2. Create a new Job.
3. Add a Python task.
4. Configure the task to run the project.
5. Select compute.
6. Add the required schedule.

Example:

```text
Job: ABC Sales Pipeline
Schedule: Daily at 2:00 AM
```

---

# 4. How to Run Tests

Run all unit tests from the project root:

Tests include:

- valid Parquet read
- wrong file path
- Silver transformation
- customer-name split
- Gold Sales output columns
- Gold Customer metrics

To run only I/O tests:

```bash
pytest tests/test_io.py -v
```

To run only transformation tests:

```bash
pytest tests/test_transformations.py -v
```

To run one test:

```bash
pytest tests/test_transformations.py::test_gold_customer_metrics -v
```

## How to Run Tests in Databricks

Attach the `run_tests` notebook to Databricks compute.

Install pytest:

```python
%pip install pytest

import os
import sys

project_root = os.getcwd()
sys.path.insert(0, f"{project_root}/src")

pytest.main([
    "tests/test_io.py",
    "-v"
])
```

---

# 5. Debugging

The project uses Python logging.

configuration:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("abc_sales")
```

Example logging:

```python
logger.info("Reading source data")
logger.info("Creating Bronze layer")
logger.info("Creating Silver layer")
logger.info("Creating Gold Sales")
logger.info("Creating Gold Customer")
logger.info("Pipeline completed successfully")
```

Example output:

```text
2026-10-01 02:00:00 INFO Reading source data
2026-10-01 02:00:10 INFO Creating Bronze layer
2026-10-01 02:00:20 INFO Creating Silver layer
2026-10-01 02:00:30 INFO Creating Gold Sales
2026-10-01 02:00:40 INFO Creating Gold Customer
2026-10-01 02:00:50 INFO Pipeline completed successfully
```

## Error Handling

The pipeline uses `try/except`:

```python
try:
    # pipeline code

except Exception:
    logger.exception("Pipeline failed")
    raise
```

`logger.exception()` records the error and stack trace.

The exception is raised again so Databricks marks the job as failed.

---

# 6. Assumptions

1. Source data is provided in Parquet format.
2. `order_id`, `customer_id`, and `order_date` are mandatory.
3. `ship_date` can be null.
4. If present, `ship_date` cannot be earlier than `order_date`.
5. Order quantity means number of distinct `order_id` values.
