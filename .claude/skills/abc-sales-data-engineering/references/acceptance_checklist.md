# Acceptance Checklist

Before finishing:

1. `SKILL.md` exists and metadata is valid.
2. Original requirement files remain under `project_requirements/`.
3. `src/abc_sales` is packageable.
4. Bronze/Silver/Gold paths default to storage account `cdl`.
5. Bronze/Silver/Gold Sales use Year/Month/Day partitions.
6. Customer Gold full-overwrites and is not date-partitioned.
7. Metadata is present in every produced dataset.
8. Tests cover I/O, wrong path, transformations, name split, Gold outputs, rolling metrics.
9. Run `pytest tests -v` when PySpark is available.
10. README explains setup, execution, tests, debugging, and Claude Skill usage.
