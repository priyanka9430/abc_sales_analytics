# Architecture Reference

```text
ADLS landing (Parquet)
        |
        v
Bronze: raw-normalized + metadata + date partitions
        |
        v
Silver: validated/cleaned + metadata + date partitions
        |
        +--------------------+
        |                    |
        v                    v
Gold Sales              Gold Customer
order grain             customer grain
partitioned             full overwrite
        |                    |
        +---------+----------+
                  v
          Unity Catalog tables
```

## Package layout

```text
src/abc_sales/
  config.py             paths, table names, runtime settings
  schemas.py            source schema
  io_utils.py           reusable Parquet I/O + UC registration
  transformations.py    pure DataFrame transformations
  main.py               Bronze/Silver/Gold orchestration
```
