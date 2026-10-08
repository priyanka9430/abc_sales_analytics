from datetime import datetime


# imports the transformation functions we want to test.
from abc_sales.transformations import ( to_gold_customer, to_gold_sales, to_silver)

#create small dummy bronze dataFrame with few sample records 
def create_bronze_test_df(spark):


    data = [
        (
            1, "O-100", "C-1", "Asha Mehta", "Consumer", "India",
            "Pune", "Standard", datetime(2018, 12, 30),
            datetime(2019, 1, 2), "file1.parquet",
            datetime(2026, 9, 30), 2018, 12, 30,
        ),
        (
            2, "O-101", "C-1", "Asha Mehta", "Consumer", "India",
            "Pune", "Standard", datetime(2018, 7, 1),
            datetime(2018, 7, 3), "file1.parquet",
            datetime(2026, 9, 30), 2018, 7, 1,
        ),
        (
            3, "O-102", "C-2", "Ravi Kumar Singh", "Corporate", "India",
            "Mumbai", "Express", datetime(2017, 1, 1),
            datetime(2017, 1, 3), "file2.parquet",
            datetime(2026, 9, 30), 2017, 1, 1,
        )
    ]

    columns = [
        "row_id", "order_id", "customer_id", "customer_name", "segment",
        "country", "city", "ship_mode", "order_date", "ship_date",
        "file_path", "execution_datetime", "order_year", "order_month",
        "order_day"
    ]

   
    df = spark.createDataFrame(data, columns)

    return df


def test_to_silver_splits_customer_name(spark):
    result = to_silver(create_bronze_test_df(spark))

    row = ( result.filter("customer_id = 'C-2'").select("customer_first_name", "customer_last_name").first() )

    # The test passes only if first name is Ravi.
    assert row.customer_first_name == "Ravi"
    # The test passes only if last name is Kumar Singh.
    assert row.customer_last_name == "Kumar Singh"

#If your code accidentally returned:
    # first_name = Ravi
    # last_name  = Kumar
    # the test would fail.



# So this test is checking: did my Gold Sales transformation produce all required columns and no unexpected columns?
def test_to_gold_sales_has_required_columns(spark):
    silver_df = to_silver(create_bronze_test_df(spark))
    result = to_gold_sales(silver_df)

#  columns that you expect Gold Sales to contain.
    expected = {
        "order_id",
        "order_date",
        "shipment_date",
        "shipment_mode",
        "city",
        "file_path",
        "execution_datetime",
        "order_year",
        "order_month",
        "order_day",
    }

    assert set(result.columns) == expected


# C-1 has two orders:
#     O-100 -> 2018-12-30
#     O-101 -> 2018-07-01
# The latest date is: 2018-12-30

def test_gold_customer_metrics(spark):
    silver_df = to_silver(create_bronze_test_df(spark))
    result = to_gold_customer(silver_df)

    customer = result.filter("customer_id = 'C-1'").first()

    assert customer.orders_all_time == 2
    assert customer.orders_last_1_month == 1
    assert customer.orders_last_6_months == 2
    assert customer.orders_last_12_months == 2
