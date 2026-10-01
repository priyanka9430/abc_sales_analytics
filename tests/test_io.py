from copy import error

import pytest

from abc_sales.io_utils import read_parquet

# This testcase is testing  Parquet read function in two situations:
# 1. The path is wrong :  the function should fail.
# 2. The path is valid :  the function should successfully read the Parquet data.

def test_read_parquet_wrong_path(spark, tmp_path):

   
    wrong_path = str(tmp_path / "wrong_folder")


    with pytest.raises(Exception):
        read_parquet(spark=spark,path=wrong_path)




def test_read_parquet_success(spark, tmp_path):

    path = str(tmp_path / "sales")

    data = [ (1, "O-100") ]

    columns = [ "row_id", "order_id" ]

    source_df = spark.createDataFrame( data, columns )

    source_df.write.mode("overwrite").parquet(path)

    result_df = read_parquet( spark, path )

    # Validate result
    assert result_df.count() == 1
