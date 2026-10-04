# Assumptions and Design Decisions

## 1. Rolling-window definition

The requirement says "last month / last 6 months / last 12 months starting from the dataset latest day." The implementation uses calendar-month boundaries with Spark `add_months(max(order_date), -N)` and an inclusive lower bound.

With sample maximum date `2018-12-30`:

- 1 month: `order_date >= 2018-11-30`
- 6 months: `order_date >= 2018-06-30`
- 12 months: `order_date >= 2017-12-30`

## 2. Order quantity

`Quantity of orders` means the number of distinct `order_id` values, not the sum of the source `Quantity` product-unit column. This follows the supplied README assumption.

## 3. Customer attributes

If a customer appears on multiple transactions, descriptive Customer attributes come from the latest transaction by `order_date`, with `order_id` as a deterministic tie-breaker.

Customer Name is split at the first whitespace boundary:

- `Alice Johnson` -> first `Alice`, last `Johnson`
- `Ana Maria de Souza` -> first `Ana`, last `Maria de Souza`
- `Madonna` -> first `Madonna`, last `NULL`

## 4. Partitioning Customer Gold

The source asks for Year/Month/Day Order Date partitioning, while the Customer Gold grain intentionally omits Order Date and is rewritten every run. Therefore:

- Bronze: partitioned by order date
- Silver: partitioned by order date
- Gold Sales: partitioned by order date
- Gold Customer: full overwrite, unpartitioned

This avoids adding a misleading order date to an aggregated customer dataset.

## 5. Write modes

The assignment does not define incremental ingestion semantics. For deterministic assignment reruns, Bronze, Silver, and Gold Sales default to `overwrite`; Gold Customer is also `overwrite` as explicitly required. A production incremental strategy can be added later when source-arrival semantics are defined.

## 6. Unity Catalog

Files remain Parquet at ADLS locations. The project optionally registers those locations as Unity Catalog external tables. The Databricks workspace must already have storage credentials/external locations granting access to the `cdl` containers.

## 7. Gold source layer

The functional wording says the Bronze dataset is split into Sales and Customer in Gold, while the technical requirement also mandates a Silver layer and the README defines Silver transformations. The implementation derives both Gold datasets from **Silver**, so invalid records removed by the declared business rules cannot re-enter Gold. Bronze remains the raw-normalized lineage layer.
