import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[2]").appName("abc-sales-tests").getOrCreate()
    )

    yield session
    session.stop()
