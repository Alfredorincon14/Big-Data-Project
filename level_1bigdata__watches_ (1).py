# -*- coding: utf-8 -*-
"""Level 1bigdata _Watches .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cmDhEoq3PC-4YMkR2kpJZgUigBP-FR0Z
"""

# Install Java, Spark, and Findspark
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q http://www-us.apache.org/dist/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz
!tar xf spark-2.4.5-bin-hadoop2.7.tgz
!pip install -q findspark

# Set Environment Variables
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-2.4.5-bin-hadoop2.7"

# Start a SparkSession
import findspark
findspark.init()

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()

# Read in data from S3 Buckets
from pyspark import SparkFiles
url = "https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Watches_v1_00.tsv.gz"
spark.sparkContext.addFile(url)
df = spark.read.csv(SparkFiles.get("amazon_reviews_us_Watches_v1_00.tsv.gz"), sep="\t", header=True)

# Show DataFrame
df.show()



df.count()

# Print our schema
df.printSchema()

"""
CREATE TABLE review_id_table (
  review_id TEXT PRIMARY KEY NOT NULL,
  customer_id INTEGER,
  product_id TEXT,
  product_parent INTEGER,
  review_date DATE -- this should be in the formate yyyy-mm-dd
);
""" 

review_id_table=df.select(["review_id", "customer_id","product_id","product_parent","review_date"])
review_id_table.show()

from pyspark.sql.types import IntegerType

review_id_table = review_id_table.withColumn("customer_id", review_id_table["customer_id"].cast(IntegerType()))

# Describe our data
review_id_table.printSchema()



from pyspark.sql.types import DateType

review_id_table = review_id_table.withColumn("review_date", review_id_table["review_date"].cast(DateType()))

review_id_table.show()

review_id_table.printSchema()

# Configure settings for RDS
mode = "append"
jdbc_url="jdbc:postgresql://mypostgressdb.cg3dgtmsvez9.us-east-2.rds.amazonaws.com:5432/my_data_class_db"
config = {"user":"root", 
          "password": "7540240AA", 
          "driver":"org.postgresql.Driver"}

review_id_table.write.jdbc(url=jdbc_url, table='review_id_table', mode=mode, properties=config)