from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.url import URL
import xmltodict

Base = declarative_base()

class Articles(Base):
    __tablename__ = 'articles'
    pubmed_id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    journal = Column(String(400))
    year = Column(Integer)
    publisher = Column(String(100))
    article_length = Column(String(100))
    authors = relationship("Authors", back_populates="article")
    keywords = relationship("Keywords", back_populates="article")

class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pubmed_id = Column(Integer, ForeignKey('articles.pubmed_id'))
    name = Column(String(100))
    article = relationship("Articles", back_populates="authors")

class Keywords(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pubmed_id = Column(Integer, ForeignKey('articles.pubmed_id'))
    keyword = Column(String(100))
    article = relationship("Articles", back_populates="keywords")

def connect_to_db():
    with open('/homes/zhe/my.cnf', 'r') as file:
        next(file)
        config = dict(line.strip().split('=') for line in file)
    url = URL.create(
        "mysql+mysqldb",
        username=config['user'],
        password=config['password'],
        host="mariadb.bin.bioinf.nl",
        database=config['database'],
        query={'charset': 'utf8mb4'}
    )
    engine = create_engine(url)
    return engine

def create_tables(engine):
    try:
        Base.metadata.create_all(engine)
    except SQLAlchemyError as error:
        print(f"Error creating tables:{error}")

def delete_tables(engine):
    try:
        with engine.connect() as connection:
            # Disable foreign key checks if using SQLite
            connection.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
            # Drop tables using raw SQL
            connection.execute('DROP TABLE IF EXISTS keywords CASCADE;')
            connection.execute('DROP TABLE IF EXISTS authors CASCADE;')
            connection.execute('DROP TABLE IF EXISTS articles CASCADE;')
            # Re-enable foreign key checks if using SQLite
            connection.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))
    except SQLAlchemyError as error:
        print(f"Error deleting tables: {error}")


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
