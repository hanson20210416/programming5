import pandas as pd
from sqlalchemy import create_engine
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg, length, col

with open('/homes/zhe/my.cnf', 'r') as file:
    next(file)
    config = dict(line.strip().split('=') for line in file)

username = config['user']
password = config['password']
host = "mariadb.bin.bioinf.nl"
database = config['database']

# Create the SQLAlchemy connection string
connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}"
engine = create_engine(connection_string)

db_table1 = "articles"
db_table2 = "authors"

# Initialize Spark session
spark = SparkSession.builder.appName("assignment4").getOrCreate()

# Query and load data for articles using SQLAlchemy
query_articles = f"SELECT * FROM {db_table1}"
pandas_df_articles = pd.read_sql(query_articles, engine)
df_articles = spark.createDataFrame(pandas_df_articles)

# Query and load data for authors using SQLAlchemy
query_authors = f"SELECT * FROM {db_table2}"
pandas_df_authors = pd.read_sql(query_authors, engine)
df_authors = spark.createDataFrame(pandas_df_authors)

# Analysis code remains the same
df_authors.select('pubmed_id').describe().show()
print("How large a list of authors does the average published article have?")
author_count_per_article = df_authors.groupBy("pubmed_id").agg(count("name").alias("author_count"))
avg_authors_per_article = author_count_per_article.agg(avg("author_count")).collect()[0][0]
print(f"The average number of authors per article is {avg_authors_per_article}\n")

df_authors.select('name').describe().show()
print("What is the author with the most publications in the XML file?")
print(f'From the max of the describe table, Alvarez Ramon is the author with the most publications\n')

df_articles.select('year').describe().show()
print("What is the month with the highest number of papers published?")
print('Since the MySQL table does not have a month column, I could not do this, but the year column exists. \
The method for finding the highest month would be similar to finding the highest year.')
print(f'Based on the describe table, the year with the highest number of papers published is NaN\n')

print("What is the longest article title you have in your file?")
# Calculate the length of each title
df_articles = df_articles.withColumn("title_length", length(col("title")))
longest_title = df_articles.orderBy(col("title_length").desc()).select("title", "title_length").first()
print(f"The longest title is: '{longest_title['title']}' with a length of {longest_title['title_length']} characters.\n")
