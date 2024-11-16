from sqlalchemy import create_engine, Column, Integer, String, text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.engine.url import URL
import xmltodict

Base = declarative_base()

class Articles(Base):
    __tablename__ = 'articles'
    pubmed_id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    journal = Column(String(200))
    year = Column(Integer)
    publisher = Column(String(200))
    article_length = Column(String(200))
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
        database=config['database']
    )
    engine = create_engine(url)
    return engine

def create_tables(engine):
    Base.metadata.create_all(engine)

def delete_tables(engine):
    Base.metadata.drop_all(engine)

def parse_pubmed_xml(file_path):
    articles_data = []
    with open(file_path, 'r') as file:
        doc = xmltodict.parse(file.read())
        for item in doc['PubmedArticleSet']['PubmedArticle']:
            citation = item['MedlineCitation']
            article = citation['Article']
            pubmed_id = int(citation['PMID']['#text'])
            title = article.get('ArticleTitle', '')
            journal = article.get('Journal', {}).get('Title', '')
            year = article.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {}).get('Year', '')
            year = int(year) if year.isdigit() else None
            publisher = citation.get('MedlineJournalInfo', {}).get('MedlineTA','')           
            # Safely get the page info
            page_info = ''
            if 'Pagination' in article:
                page_info = article['Pagination'].get('MedlinePgn', '')
            
            article_data = {
                'pubmed_id': pubmed_id,
                'title': title,
                'journal': journal,
                'year': year,
                'publisher': publisher,
                'article_length': page_info
            }
            authors = []
            if 'AuthorList' in article:
                author_list = article['AuthorList'].get('Author', [])
                if isinstance(author_list, dict):
                    author_list = [author_list]
                for author in author_list:
                    last_name = author.get('LastName', '')
                    fore_name = author.get('ForeName', '')
                    name = f"{last_name} {fore_name}".strip()
                    if name:
                        authors.append(name)
            article_data['authors'] = authors           
            # Get keywords
            keywords = []
            if 'MeshHeadingList' in citation:
                mesh_headings = citation['MeshHeadingList'].get('MeshHeading', [])
                if isinstance(mesh_headings, dict):
                    mesh_headings = [mesh_headings]
                for mesh in mesh_headings:
                    keyword = mesh['DescriptorName'].get('#text', '')
                    if keyword:
                        keywords.append(keyword)
            article_data['keywords'] = keywords       
            articles_data.append(article_data)
    return articles_data

def insert_data(session, article_data):
    try:
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
            kw = Keywords(pubmed_id=article_data['pubmed_id'], keyword=keyword)
            session.add(kw)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting data for PubMed ID {article_data['pubmed_id']}: {str(e)}")

if __name__ == "__main__":
    engine = connect_to_db()
    delete_tables(engine)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    filepath = '/data/datasets/NCBI/PubMed/pubmed21n1022.xml'
    for  article_data in parse_pubmed_xml(filepath):
        insert_data(session, article_data)
    session.close()
   
