def read_parquet(spark, path, schema=None):
#Read Parquet files from given path.
    reader = spark.read

    if schema is not None:
        reader = reader.schema(schema)

    return reader.parquet(path)


def write_parquet_table( df, table_name, path, mode="overwrite", partition_columns=None ):
# Write a DataFrame as a Parquet table at an ADLS location.
    writer = (
        df.write.format("parquet").mode(mode).option("path", path)
    )

    if partition_columns:
        writer = writer.partitionBy(*partition_columns)

    writer.saveAsTable(table_name)
