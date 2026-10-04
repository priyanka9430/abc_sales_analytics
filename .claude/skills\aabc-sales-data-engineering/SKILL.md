---
name: abc-sales-data-engineering
description: Build, validate, explain, or extend the ABC Sales PySpark/Databricks ETL assignment using ADLS Gen2 cdl, Unity Catalog, Bronze/Silver/Gold Parquet, rolling customer metrics, logging, packaging, sample data, and pytest. Use when working on this repository or implementing the ABC Sales data engineering project.
---

# ABC Sales Data Engineering Skill

Use this skill to implement the repository, not merely to describe an implementation.

## Read first

Before changing code, read only the references needed for the task:

- [Requirements](references/requirements.md) - functional/technical behavior.
- [Architecture](references/architecture.md) - layer responsibilities and file layout.
- [Engineering standards](references/engineering_standards.md) - implementation conventions.
- [Acceptance checklist](references/acceptance_checklist.md) - final validation.

If the repository also contains `project_requirements/`, treat the original uploaded documents there as the source of truth. Do not silently change explicit business rules.

## Required workflow

1. **Implement layer by layer.** Build Bronze, then Silver, then Gold Sales/Customer. Keep each layer callable independently.
2. **Generate or maintain sample data.** Keep a small human-readable sample and a Spark path to produce Parquet.
3. **Add/maintain tests.** Cover I/O, transformations, edge cases, and wrong paths. Tests must validate behavior.
4. **Validate.** Run syntax/structure validation. If PySpark is available, run `pytest tests -v`. Fix failures before declaring completion.
5. **Report changes.** Summarize files changed, tests run, assumptions, and any environment-dependent validation not executed.

## Non-negotiable project behavior

- Python + PySpark.
- Parquet storage.
- Bronze -> Silver -> Gold medallion architecture.
- ADLS Gen2 default storage account `cdl`.
- Unity Catalog registration supported but configurable.
- `file_path` and `execution_datetime` metadata carried through layers.
- `snake_case` Data Lake columns.
- Bronze/Silver/Gold Sales partitioned by `order_year`, `order_month`, `order_day`.
- `order_id`, `customer_id`, and `order_date` are mandatory in Silver.
- `ship_date` may be null; otherwise it must be on/after `order_date`.
- Gold Sales exposes `order_id`, `order_date`, `shipment_date`, `shipment_mode`, and `city`, plus operational metadata/partition columns.
- Gold Customer is one row per customer and overwritten each run.
- Gold Customer splits customer names into first and last name.
- Gold Customer counts distinct `order_id` for rolling 1/6/12-month windows and all-time.
- Rolling windows anchor to `max(order_date)` dynamically; do not hard-code 2018-12-30 in production logic.
- Use consistent logging and re-raise exceptions so Databricks jobs fail visibly.
- Package code under `src/abc_sales` and keep the project installable.

## Important design decisions

The Customer Gold grain has no `order_date`, so do not force Year/Month/Day partitions onto it. It must be a full overwrite. The other date-grained layers are partitioned.

Use the latest customer transaction to select descriptive attributes. Split the customer name at the first whitespace; preserve the remaining tokens as last name. A single-token name has a null last name.

The assignment does not define incremental source semantics. Keep deterministic overwrite behavior unless the user explicitly supplies incremental requirements.

## Coding rules

- Prefer small functions with explicit inputs/outputs.
- Keep Spark transformations in `transformations.py`, storage concerns in `io_utils.py`, configuration in `config.py`, and orchestration in `main.py`.
- Avoid unnecessary framework abstractions and hidden side effects.
- Never swallow exceptions.
- Do not introduce secrets, account keys, SAS tokens, or credentials into source control.
- Do not remove tests to make a build pass.
- Do not replace Parquet with Delta unless the user changes the requirement.

## Validation commands

From the repository root:

```bash
python scripts/validate_python.py
pytest tests -v
```

Validate expected structure with:

```bash
python .claude/skills/abc-sales-data-engineering/scripts/validate_project.py --project-root .
```

If `pytest` cannot run because PySpark/Java is unavailable, state that clearly and still run syntax/structure validation.

## Completion response

When executing this skill, finish with a concise summary containing:

- what was created or changed;
- key requirement decisions;
- validation/tests executed and result;
- exact next command for Databricks or local execution.
