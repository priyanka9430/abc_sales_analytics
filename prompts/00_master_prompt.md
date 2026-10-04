# Master Prompt - Build / Repair / Validate End to End

Paste this into Claude Code from the repository root:

```text
Use the abc-sales-data-engineering skill in this repository.

Read project_requirements/requirement_summary.md, project_requirements/acceptance_criteria.md, project_requirements/assumptions_and_decisions.md, and the original requirement files under project_requirements/.

Then inspect the existing repository and complete the ABC Sales data engineering project end to end. Do not only explain what should be done: create or update the actual files.

Required outcome:
1. Python/PySpark installable package under src/abc_sales.
2. Parquet Bronze -> Silver -> Gold pipeline for ADLS Gen2 storage account cdl.
3. Configurable Unity Catalog registration.
4. Bronze/Silver/Gold Sales partitioned by order year/month/day.
5. Silver quality rules: order_id/customer_id/order_date mandatory; ship_date null or >= order_date; trim strings.
6. Gold Sales with order_id, order_date, shipment_date, shipment_mode, city plus operational metadata/partitions.
7. Gold Customer with one row per customer, name split, segment/country, distinct order counts for rolling 1/6/12 months and all time anchored to max(order_date); full overwrite and no date partitioning.
8. file_path and execution_datetime metadata carried through produced layers.
9. Logging, error handling, modularity, reproducibility, packaging, and pipeline-stage segregation.
10. Unit tests for valid read/write, wrong path, Silver rules, edge cases, name splitting, Gold Sales columns, and Gold Customer metrics.
11. Human-readable sample data and a Spark generator for the required Parquet source.
12. Databricks-ready scripts/notebooks and a README with setup, run, tests, debugging, and Claude Skill instructions.

Validation before completion:
- run: python scripts/validate_python.py
- run: python .claude/skills/abc-sales-data-engineering/scripts/validate_project.py --project-root .
- if PySpark/Java is available, run: pytest tests -v
- fix failures before finishing

Keep explicit requirement behavior unchanged unless a conflict is documented in project_requirements/assumptions_and_decisions.md. Never add credentials or secrets. At the end, report files changed, tests/validation performed, any environment limitation, and the exact next command I should run in Databricks.
```
