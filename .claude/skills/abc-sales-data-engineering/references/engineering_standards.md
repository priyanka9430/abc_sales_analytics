# Engineering Standards

- Keep business transformations separate from I/O.
- Use a central logger rather than `print` in production pipeline code.
- Raise project-specific exceptions for read/write failures.
- Never embed credentials.
- Keep tests deterministic and small.
- Use `countDistinct(order_id)` for order metrics.
- Use dynamic `max(order_date)` for rolling windows.
- Preserve multi-token surnames/rest-of-name when splitting Customer Name.
- Treat single-token Customer Name as first name + null last name.
- Keep README run/test/debug instructions synchronized with actual commands.
