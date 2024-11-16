# -*- coding: utf-8 -*-
'''author = zhipeng he'''
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.url import URL
import xmltodict
import sys

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

def parse_pubmed_xml(file_path):
    articles_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        doc = xmltodict.parse(file.read())
        for item in doc['PubmedArticleSet']['PubmedArticle']:
            citation = item['MedlineCitation']
            article = citation['Article']
            pubmed_id = int(citation['PMID']['#text'])
            title = article.get('ArticleTitle', '')
            journal = article.get('Journal', {}).get('Title', '')
            year = article.get('Journal', {}).get('JournalIssue', {}).\
                get('PubDate', {}).get('Year', '')
            year = int(year) if year.isdigit() else None
            publisher = citation.get('MedlineJournalInfo', {}).get('MedlineTA', '')
            page_info = ''
            if 'Pagination' in article:
                page_info = article['Pagination'].get('MedlinePgn', '')
            
            # Initialize the article data
            article_data = {
                'pubmed_id': pubmed_id,
                'title': title,
                'journal': journal,
                'year': year,
                'publisher': publisher,
                'article_length': page_info,
                'authors': [],
                'keywords': []
            }
            # Process authors
            if 'AuthorList' in article:
                author_list = article['AuthorList'].get('Author', [])
                if isinstance(author_list, dict):
                    author_list = [author_list]
                for author in author_list:
                    last_name = author.get('LastName', '')
                    fore_name = author.get('ForeName', '')
                    name = f"{last_name} {fore_name}".strip()
                    if name:
                        article_data['authors'].append(name)
            # Process keywords
            if 'KeywordList' in citation:
                keyword_list = citation['KeywordList'].get('Keyword', [])
                if isinstance(keyword_list, dict):
                    keyword_list = [keyword_list]
                for keyword in keyword_list:
                    if isinstance(keyword, dict):
                        keyword_text = keyword.get('#text', '')
                    else:
                        keyword_text = keyword
                    if keyword_text:
                        article_data['keywords'].append(keyword_text)
            elif 'MeshHeadingList' in citation:
                mesh_headings = citation['MeshHeadingList'].get('MeshHeading', [])
                if isinstance(mesh_headings, dict):
                    mesh_headings = [mesh_headings]
                for mesh in mesh_headings:
                    keyword = mesh['DescriptorName'].get('#text', '')
                    if keyword:
                        article_data['keywords'].append(keyword)
            articles_data.append(article_data)
    return articles_data

def insert_data(session, article_data):
    try:
        with session.begin():
            article = Articles(
                pubmed_id=article_data['pubmed_id'],
                title=article_data['title'],
                journal=article_data['journal'],
                year=article_data['year'],
                publisher=article_data['publisher'],
                article_length=article_data['article_length']
            )
            session.merge(article)
            for author_name in article_data['authors']:
                author = Authors(pubmed_id=article_data['pubmed_id'], name=author_name)
                session.add(author)
            for keyword in article_data['keywords']:
                key_word = Keywords(pubmed_id=article_data['pubmed_id'], keyword=keyword)
                session.add(key_word)
        session.commit()
    except SQLAlchemyError as error:
        session.rollback()
        print(f"Error inserting data for PubMed ID {article_data['pubmed_id']}: {str(error)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 assignment3.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    print(f"Processing file: {input_file}")

    engine = connect_to_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        for article_data in parse_pubmed_xml(input_file):
            print(f"Inserting data for article with PubMed ID: {article_data['pubmed_id']}")
            insert_data(session, article_data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

