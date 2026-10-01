from pyspark.sql import functions as F
from pyspark.sql.window import Window

from abc_sales.config import DATE_FORMAT


def to_bronze(df):
    #Standardize source columns and partition columns(year, month, day) for downstream processing.
    df.select(
        F.col("Row ID").alias("row_id"),
        F.col("Order ID").alias("order_id"),
        F.col("Order Date").alias("order_date"),
        F.col("Ship Date").alias("ship_date"),
        F.col("Ship Mode").alias("ship_mode"),
        F.col("Customer ID").alias("customer_id"),
        F.col("Customer Name").alias("customer_name"),
        F.col("Segment").alias("segment"),
        F.col("Country").alias("country"),
        F.col("City").alias("city"),
        F.input_file_name().alias("file_path"),
        F.current_timestamp().alias("execution_datetime"),
    ).withColumn(
        "order_date", F.to_date(F.col("order_date"), DATE_FORMAT),
    ).withColumn(
        "ship_date", F.to_date(F.col("ship_date"), DATE_FORMAT),
    ).withColumn("order_year", F.year(F.col("order_date"))).withColumn("order_month", F.month(F.col("order_date")))  .withColumn("order_day", F.dayofmonth(F.col("order_date"))) 
    

    return df


def to_silver(df):
# Validate and clean Bronze records.
# NOTEquality/business rule are assumed.

    # Validate that the order_id, customer_id, and order_date are not null
    valid_condition = (
        F.col("order_id").isNotNull() & F.col("customer_id").isNotNull()
        & F.col("order_date").isNotNull()
    )

    # Validate that the ship date is either null or greater than or equal to the order date
    valid_shipping_condition = (
        F.col("ship_date").isNull()  | (F.col("ship_date") >= F.col("order_date"))
    )

    # Remove leading and trailing whitespace from the customer_name column
    silver_df = (
        df.filter(valid_condition & valid_shipping_condition)
        .withColumn("customer_name", F.trim(F.col("customer_name")))
    )

    # Split the customer_name into first and last name using split on a space
    name_parts = F.split(F.col("customer_name"), " ", 2)

    silver_df = ( silver_df.withColumn("customer_first_name", name_parts.getItem(0)).withColumn("customer_last_name", name_parts.getItem(1)))

    return silver_df


def to_gold_sales(df):
# Create the Gold Sales dataset. 

   df.select(
        "order_id",
        "order_date",
        F.col("ship_date").alias("shipment_date"),
        F.col("ship_mode").alias("shipment_mode"),
        "city",
        "file_path",
        "execution_datetime",
        "order_year",
        "order_month",
        "order_day",
    )
   
   return df



def to_gold_customer(df):


    latest_date_df = df.agg( F.max("order_date").alias("latest_order_date") )

    df_with_latest_date = df.crossJoin(latest_date_df)
 

    metrics_df = (
        df_with_latest_date
        .groupBy("customer_id")
        .agg(
            F.countDistinct(
                F.when(  
                    F.col("order_date")  >= F.add_months(F.col("latest_order_date"), -1),
                    F.col("order_id"),
                )
            ).alias("orders_last_1_month"),

            F.countDistinct(
                F.when(
                    F.col("order_date") >= F.add_months(F.col("latest_order_date"), -6),
                    F.col("order_id"),
                )
            ).alias("orders_last_6_months"),

            F.countDistinct(
                F.when(
                    F.col("order_date") >= F.add_months(F.col("latest_order_date"), -12),
                    F.col("order_id"),
                )
            ).alias("orders_last_12_months"),

            F.countDistinct("order_id").alias("orders_all_time"),
            F.max("latest_order_date").alias("as_of_date"),
        )
    )

    return metrics_df
