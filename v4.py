from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.engine.url import URL
import xmltodict

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    pubmed_id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    journal = Column(String(200))
    year = Column(Integer)
    publisher = Column(String(200))
    article_length = Column(String(50))  
    authors = relationship("Author", back_populates="article", cascade="all, delete-orphan")
    keywords = relationship("Keyword", back_populates="article", cascade="all, delete-orphan")

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pubmed_id = Column(Integer, ForeignKey('articles.pubmed_id', ondelete="CASCADE"))
    name = Column(String(100))
    article = relationship("Article", back_populates="authors")

class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pubmed_id = Column(Integer, ForeignKey('articles.pubmed_id', ondelete="CASCADE"))
    keyword = Column(String(100))
    article = relationship("Article", back_populates="keywords")

def connect_to_db():
    with open('/homes/zhe/my.cnf', 'r') as file:
        next(file)
        config = dict(line.strip().split('=') for line in file)
    
    url = URL.create(
        "mysql+mysqldb",
        username=config['user'],
        password=config['password'],
        host="mariadb.bin.bioinf.nl",
        database=config['database']
    )
    engine = create_engine(url, echo=True)  # Set echo=True for debugging
    return engine

def create_tables(engine):
    Base.metadata.create_all(engine)

def delete_tables(engine):
    Base.metadata.drop_all(engine)

def parse_pubmed_xml(file_path):
    with open(file_path, 'r') as file:
        doc = xmltodict.parse(file.read())
    
    articles_data = []
    for item in doc['PubmedArticleSet']['PubmedArticle']:
        citation = item['MedlineCitation']
        article = citation['Article']
        
        pubmed_id = int(citation['PMID']['#text'])
        title = article.get('ArticleTitle', '')
        journal = article['Journal'].get('Title', '')
        year = article['Journal']['JournalIssue']['PubDate'].get('Year', 'N/A')
        publisher = citation['MedlineJournalInfo'].get('Country', '')
        page_info = article['Pagination'].get('MedlinePgn', '')
        
        authors = get_authors(article)
        keywords = get_keywords(citation)
        
        article_data = {
            'pubmed_id': pubmed_id,
            'title': title,
            'journal': journal,
            'year': year,
            'publisher': publisher,
            'article_length': page_info,
            'authors': authors,
            'keywords': keywords
        }
        articles_data.append(article_data)
    
    return articles_data

def get_authors(article):
    authors = []
    author_list = article.get('AuthorList', {}).get('Author', [])
    if isinstance(author_list, dict):
        author_list = [author_list]
    
    for author in author_list:
        last_name = author.get('LastName', '')
        fore_name = author.get('ForeName', '')
        initials = author.get('Initials', '')
        full_name = f"{last_name}, {fore_name} ({initials})"
        authors.append(full_name)
    
    return authors

def get_keywords(citation):
    keywords = []
    mesh_headings = citation.get('MeshHeadingList', {}).get('MeshHeading', [])
    if isinstance(mesh_headings, dict):
        mesh_headings = [mesh_headings]
    
    for heading in mesh_headings:
        descriptor = heading['DescriptorName']['#text']
        keywords.append(descriptor)
        
        qualifiers = heading.get('QualifierName', [])
        if isinstance(qualifiers, dict):
            qualifiers = [qualifiers]
        
        for qualifier in qualifiers:
            keywords.append(qualifier['#text'])
    
    return keywords

def insert_data(session, articles_data):
    for article_data in articles_data:
        article = Article(
            pubmed_id=article_data['pubmed_id'],
            title=article_data['title'],
            journal=article_data['journal'],
            year=article_data['year'],
            publisher=article_data['publisher'],
            article_length=article_data['article_length']
        )
        
        for author_name in article_data['authors']:
            author = Author(name=author_name)
            article.authors.append(author)
        
        for keyword in article_data['keywords']:
            kw = Keyword(keyword=keyword)
            article.keywords.append(kw)
        
        session.merge(article)
    
    session.commit()

if __name__ == "__main__":
    engine = connect_to_db()
    delete_tables(engine)  # Add this line to drop existing tables
    create_tables(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    filepath = '/data/datasets/NCBI/PubMed/pubmed21n1022.xml'
    articles_data = parse_pubmed_xml(filepath)
    insert_data(session, articles_data)
    
    session.close()
    engine.dispose()
