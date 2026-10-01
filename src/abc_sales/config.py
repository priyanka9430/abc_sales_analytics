CATALOG = "abc_sales"
SCHEMA = "sales"

BRONZE_TABLE = f"{CATALOG}.{SCHEMA}.bronze_sales"
SILVER_TABLE = f"{CATALOG}.{SCHEMA}.silver_sales"
GOLD_SALES_TABLE = f"{CATALOG}.{SCHEMA}.gold_sales"
GOLD_CUSTOMER_TABLE = f"{CATALOG}.{SCHEMA}.gold_customer"

# Source is exposed through a Unity Catalog external Volume.
SOURCE_PATH = "/Volumes/abc_sales/landing/sales_files"


BRONZE_PATH = (
    "abfss://bronze@cdl.dfs.core.windows.net/abc_sales/sales"
)

SILVER_PATH = (
    "abfss://silver@cdl.dfs.core.windows.net/abc_sales/sales"
)

GOLD_SALES_PATH = (
    "abfss://gold@cdl.dfs.core.windows.net/abc_sales/sales"
)

GOLD_CUSTOMER_PATH = (
    "abfss://gold@cdl.dfs.core.windows.net/abc_sales/customer"
)

PARTITION_COLUMNS = ["order_year", "order_month", "order_day"]
DATE_FORMAT = "yyyy-MM-dd"
