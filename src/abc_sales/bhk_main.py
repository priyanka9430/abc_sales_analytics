import logging
from unicodedata import name

from pyspark.sql import SparkSession

from abc_sales.config import ( BRONZE_PATH, BRONZE_TABLE, GOLD_CUSTOMER_PATH, GOLD_CUSTOMER_TABLE, GOLD_SALES_PATH, GOLD_SALES_TABLE, PARTITION_COLUMNS, SILVER_PATH, SILVER_TABLE, SOURCE_PATH )

from abc_sales.io_utils import read_parquet, write_parquet_table
from abc_sales.schemas import RAW_SCHEMA
from abc_sales.transformations import ( to_bronze,to_silver, to_gold_sales, to_gold_customer )

logging.basicConfig( level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


logger = logging.getLogger("abc_sales")


def run_pipeline(spark):
# Run Source => Bronze => Silver => Gold.

    try:
        # Read source
        logger.info("Reading source data from %s", SOURCE_PATH)

        source_df = read_parquet( spark=spark, path=SOURCE_PATH, schema=RAW_SCHEMA)

        # Bronze
        logger.info("Creating Bronze")
        bronze_df = to_bronze(source_df)

        write_parquet_table( df=bronze_df, table_name=BRONZE_TABLE, path=BRONZE_PATH, mode="overwrite", partition_columns=PARTITION_COLUMNS )

        # Silver
        logger.info("Creating Silver")
        bronze_table_df = spark.table(BRONZE_TABLE)
        silver_df = to_silver(bronze_table_df)

        write_parquet_table( df=silver_df, table_name=SILVER_TABLE, path=SILVER_PATH, mode="overwrite", partition_columns=PARTITION_COLUMNS)

        # Gold Sales
        logger.info("Creating Gold Sales")
        silver_table_df = spark.table(SILVER_TABLE)
        gold_sales_df = to_gold_sales(silver_table_df)

        write_parquet_table( df=gold_sales_df, table_name=GOLD_SALES_TABLE, path=GOLD_SALES_PATH, mode="overwrite", partition_columns=PARTITION_COLUMNS)

        # Gold Customer
        logger.info("Creating Gold Customer")
        gold_customer_df = to_gold_customer(silver_table_df)

        write_parquet_table( df=gold_customer_df, table_name=GOLD_CUSTOMER_TABLE, path=GOLD_CUSTOMER_PATH, mode="overwrite", partition_columns=None )

        logger.info("Pipeline completed successfully")

    except Exception:
        logger.exception("Pipeline failed")
        raise


def main():
    spark = ( SparkSession.builder.appName("abc sales pipeline").getOrCreate() )

    run_pipeline(spark)


if __name__ == "__main__":
    main()
