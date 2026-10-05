import logging

from pyspark.sql import SparkSession

from abc_sales.sales_pipeline import run_sales_pipeline

logging.basicConfig( level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s" )


def main():
    #Application entry point.
    spark = ( SparkSession.builder.appName("abc sales pipeline").getOrCreate() )

    run_sales_pipeline(spark)


if __name__ == "__main__":
    main()
