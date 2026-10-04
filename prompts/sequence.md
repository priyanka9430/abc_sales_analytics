# Claude Prompt Sequence

## Fastest option: one-shot

Run only `00_master_prompt.md`. It tells Claude to build/repair and validate the entire project.

## Guided option: run in this order

1. `01_requirements_and_plan.md` - understand requirements and map them to files.
2. `02_build_pipeline.md` - create/repair the PySpark pipeline.
3. `03_build_tests.md` - add and run tests.
4. `04_validate_and_fix.md` - check the full acceptance criteria and fix gaps.
5. `05_databricks_run.md` - make the demo/run path Databricks-ready.

## Recommended Claude Code invocation

From the project root, start Claude Code and paste the content of the selected prompt. Because the repository contains `.claude/skills/abc-sales-data-engineering/SKILL.md`, Claude Code can discover the skill at project scope.

## Recommended first prompt

```text
Use the abc-sales-data-engineering skill and execute prompts/00_master_prompt.md against this repository. Work end to end and modify files as needed. Validate before you finish.
```

## After future requirement changes

Use:

```text
Use the abc-sales-data-engineering skill. Compare the new requirement with project_requirements/, update the requirement summary and acceptance criteria first, then change the implementation and tests. Preserve backward-compatible behavior unless the new requirement explicitly replaces it. Run validation when finished.
```
