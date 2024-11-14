# If i run it , the print functions print too much values, so I suggest check my spark.ipynb
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, min, max, when, split, col
from pyspark.sql.functions import concat, col, lit
import pyspark.sql.functions as F

# Initialize SparkSession
spark = SparkSession.builder.appName("txt to DataFrame").getOrCreate()

# Load CSV file into DataFrame
df = spark.read.csv("/homes/zhe/Desktop/programming/p5/exam/dbNSFP4.9a.txt.gz.SMALL",sep='\t', header=True, inferSchema=True)

# Show the DataFrame content
df.show(5)



### question 1
# Replace '.' with null
df = df.withColumn("SIFT_score", when(col("SIFT_score") == ".", None).otherwise(col("SIFT_score")))

# Split multiple scores and take the first one
df = df.withColumn("SIFT_score", split(col("SIFT_score"), ";").getItem(0))

# Convert to double
df = df.withColumn("SIFT_score", col("SIFT_score").cast("double"))

# Recalculate statistics
sift_mean = df.select(mean("SIFT_score")).collect()[0][0]
sift_min = df.select(min("SIFT_score")).collect()[0][0]
sift_max = df.select(max("SIFT_score")).collect()[0][0]

print(f"Mean SIFT score: {sift_mean}")
print(f"Minimum SIFT score: {sift_min}")
print(f"Maximum SIFT score: {sift_max}")


###question 2

# Step 1 & 2: Merge values and create new column
# Step 1 & 2: Merge values and create new column
df1 = df.withColumn("hg19_chr_pos", 
                   concat(col("hg19_pos(1-based)").cast("string"), lit("_"),col("hg19_chr") ))

# Step 3: Remove original columns
columns_to_drop = ["hg19_chr", "hg19_pos(1-based)"]
df1 = df1.drop(*columns_to_drop)

# Verify the changes
df1.select("hg19_chr_pos").show(5)
print(df1.columns)


### Question 3
# Select the relevant columns

rankscore_columns = [col for col in df.columns if col.endswith('_rankscore')]

# Create the score_df
score_df = df.select(['codonpos']  + rankscore_columns)
df_with_avg = score_df.withColumn(
    'avg_rankscore', 
    F.expr(f"""
        aggregate(
            array({', '.join([f"if(`{col}` != '.' AND `{col}` IS NOT NULL, cast(`{col}` as double), NULL)" for col in rankscore_columns])}),
            0D, 
            (acc, x) -> acc + coalesce(x, 0D), 
            acc -> acc / size(array({', '.join([f"`{col}`" for col in rankscore_columns])}))
        )
    """)
)

# Step 2: Create a new DataFrame with 'codonpos' and 'avg_rankscore'
df2 = df_with_avg.select('codonpos', 'avg_rankscore')

# Step 3: Sort the rows by 'avg_rankscore' in descending order and show the top 10 rows
df2.sort(df2["avg_rankscore"].desc()).show(10)

# Codon Position 2 Shows the Most Predicted Effects:
# Becuase it has the highest mean at all 57 predictions score.
# This observation makes biological sense. The second position of a codon is often the most critical 
# in determining the amino acid that will be incorporated into the protein. Changes in this position 
# are highly likely to result in a different amino acid being coded for, which can significantly alter
# the protein's structure and function.
# Biological Significance:
#   The genetic code is structured in such a way that the second position of a codon is often the most 
#     informative about the chemical properties of the amino acid it encodes.
#   Changes in the second position frequently lead to more dramatic shifts in amino acid properties 
#     (e.g., from a hydrophobic to a hydrophilic amino acid) compared to changes in other positions
