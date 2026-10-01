CREATE CATALOG IF NOT EXISTS abc_sales;

CREATE SCHEMA IF NOT EXISTS abc_sales.landing;
CREATE SCHEMA IF NOT EXISTS abc_sales.sales;


-- storage account name : cdl (ADLS Gen2)
-- container name : landing

CREATE EXTERNAL VOLUME IF NOT EXISTS abc_sales.landing.sales_files
LOCATION 'abfss://landing@cdl.dfs.core.windows.net/abc_sales/sales';

