import pandas as pd
from pyspark.sql import SparkSession
from sqlalchemy import create_engine




# Initialize SparkSession
spark = SparkSession.builder.appName("CSV to DataFrame").getOrCreate()

# Load CSV file into DataFrame
df = spark.read.csv("/homes/zhe/Desktop/programming/p5/week6/db.csv", header=True, inferSchema=True)

# Show the DataFrame content
df.show()
# # Create SparkSession
# spark = SparkSession.builder \
#            .appName('assignment6') \
#            .getOrCreate()

# # Load the `authors` table into a Spark DataFrame
# authors_df = spark.read \
#     .format("jdbc") \
#     .option("url", f"jdbc:mysql://{host}/{database}") \
#     .option("dbtable", db_table2) \
#     .option("user", username) \
#     .option("password", password) \
#     .option("driver", "org.mariadb.jdbc.Driver") \
#     .load()

# # Show the data and schema of `authors_df`
# authors_df.show()
# authors_df.printSchema()

# # Perform any desired processing on `authors_df` below
# # For example, counting the number of unique authors by name:
# author_counts = authors_df.groupBy("name").count()
# author_counts.show()

# Close the Spark session at the end of the script
spark.stop()
