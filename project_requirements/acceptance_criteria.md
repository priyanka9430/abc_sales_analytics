# Acceptance Criteria

The project is complete when all of the following are true.

## Structure

- [ ] `src/abc_sales` is an installable Python package.
- [ ] `pyproject.toml` defines build metadata and dependencies.
- [ ] Bronze, Silver, Gold Sales, and Gold Customer logic is separated into reusable functions.
- [ ] Source requirement documents are preserved under `project_requirements/`.
- [ ] A Claude Skill exists at `.claude/skills/abc-sales-data-engineering/SKILL.md`.
- [ ] Prompts and execution sequence exist under `prompts/`.

## Data pipeline

- [ ] Source is read from Parquet.
- [ ] Bronze normalizes names to snake_case and adds metadata.
- [ ] Bronze is partitioned by order year/month/day.
- [ ] Silver enforces mandatory columns and ship-date rule.
- [ ] Silver is partitioned by order year/month/day.
- [ ] Gold Sales has required business attributes plus metadata/partition columns.
- [ ] Gold Sales is partitioned by order year/month/day.
- [ ] Gold Customer has one row per customer and is overwritten every run.
- [ ] Gold Customer calculates distinct-order metrics for 1/6/12 months and all time using the dataset maximum order date.
- [ ] Gold Customer is intentionally unpartitioned because it has no order date at its declared grain.

## Operations

- [ ] Logging shows stage start/success/failure.
- [ ] Exceptions are logged and re-raised.
- [ ] ADLS `cdl` paths are configurable.
- [ ] Unity Catalog registration can be enabled/disabled.
- [ ] Sample data can be converted to Parquet with Spark.
- [ ] Databricks notebooks/scripts are supplied for sample generation, pipeline execution, and test execution.

## Testing

- [ ] `pytest tests -v` succeeds in an environment with PySpark/Java.
- [ ] Wrong-path handling is tested.
- [ ] I/O round-trip is tested.
- [ ] Silver quality rules are tested.
- [ ] Customer name parsing is tested.
- [ ] Gold Sales columns are tested.
- [ ] Customer rolling metrics are tested against the 2018-12-30 sample maximum date.
