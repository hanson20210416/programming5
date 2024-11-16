from sqlalchemy import create_engine, Column, Integer, String, text, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.engine.url import URL
import xmltodict

Base = declarative_base()
def create_tables():
    class articles(Base):
        __tablename__ = 'articles'
        pubmed_id = Column(Integer, primary_key=True)
        title = Column(String(1000))
        journal = Column(String(200))
        year = Column(Integer)
        publisher = Column(String(200))
        article_length = Column(Integer)

    class authors(Base):
        __tablename__ = 'authors'
        pubmed_id = Column(Integer, primary_key=True)
        name = Column(String(100))

    class keywords(Base):
        __tablename__ = 'keywords'
        pubmed_id = Column(Integer, primary_key=True)
        keyword = Column(String(100))

def connect_to_db():
    with open ('/homes/zhe/my.cnf','r') as file:
        next(file)
        config = {}
        for line in file:
            key,value = line.strip().split('=')
            config[key.strip()] = value.strip()
        print(config)
        directory = "mysql+mysqldb://"+config['user']+':'+config['password']+\
                "@mariadb.bin.bioinf.nl/"+config['database']
    url = URL.create(directory)
    engine = create_engine(url)
    return engine.connect()
    
def delete_table():
    connect_to_db()
    if engine:
        try:
            engine.execute(f'DROP TABLE IF EXISTS {articles}{authors}{keywords};')
            print(f'Table {articles}{authors}{keywords} deleted successfully!')
        except Exception as e:
            print(f'Error deleting table: {e}')
    pass
   
# Step 3: Parse XML file
def parse_pubmed_xml(file_path):
    articles_data = []
    with open(filepath , 'r') as file:
        doc = xmltodict.parse(file.read())
        for item in doc['PubmedArticleSet']['PubmedArticle']['MedlineCitation']:
            pubmed_id = item['PMID']['#text']
            title = item['Article'].get('ArticleTitle')
            journal = item['Article']['Journal'].get('Title')
            year = item['Article']['Journal']['JournalIssue']['PubDate'].get('Year', 'N/A')
            publisher = item['MedlineJournalInfo'].get('Country', {}).get('MedlineTA', {})
            page_info = item['Article']['Pagination'].get('MedlinePgn')
            article_data = {
                'pubmed_id': pubmed_id,
                'title': title,
                'journal': journal,
                'year': year,
                'publisher': publisher,
                'authors': None,
                'keywords': None,
                'article_length': page_info
            }
            articles_data.append(article_data)
        return articles_data

def get_authors(filepath):
    with open(filepath , 'r') as file:
        doc = xmltodict.parse(file.read())
        for item in doc['PubmedArticleSet']['PubmedArticle']['MedlineCitation']:
            if item['AuthorList']['@CompleteYN'] == 'Y':
                authors = []
                author_list = item['AuthorList']['Author']
                # Ensure author_list is always a list
            if isinstance(author_list, dict):
                author_list = [author_list]

            for author in author_list:
                last_name = author['LastName']
                fore_name = author['ForeName']
                initials = author['Initials']
                # Store author information in a dictionary
                author_info = {
                    'LastName': last_name,
                    'ForeName': fore_name,
                    'Initials': initials}
                authors.append(author_info)
            # Print the list of authors
            # for author in authors:
            #     print(author)
        else:
            print("Author list is not complete.")
                
                
def get_keywords():
    '''
    Input: 1. research - article info in dictionary format (from .xml file)

    Function return a list of keywords (In STRING format!)

    Output: 1. article_keywords_str - list of keywords in STR format
    '''
    article_keywords = set()
    for elem in research["MedlineCitation"]['MeshHeadingList']['MeshHeading']:
        article_keywords.add(elem['DescriptorName']['#text'])

        # If tag 'QualifierName' exist do:
        try:
            # if value == str
            try:
                article_keywords.add(elem['QualifierName']['#text'])
            # else: value == dict
            except:
                for e in elem['QualifierName']:
                    article_keywords.add(e['#text'])
        except:
            None
    article_keywords_str = ', '.join(article_keywords)

    return article_keywords_str
    

def insert_article_data(connection, article):
    query = """
        INSERT INTO articles (pubmed_id, title, journal, year, publisher)
        VALUES (:pubmed_id, :title, :journal, :year, :publisher)
        ON DUPLICATE KEY UPDATE
            title = :title,
            journal = :journal,
            year = :year,
            publisher = :publisher,
            page_count = :article_length
    """
    result = connection.execute(query, article)
    return result

if __name__ == "__main__":
    connection = connect_to_db()
    filepath = '/data/datasets/NCBI/PubMed/pubmed21n1022.xml'
    create_tables()
    articles_data = parse_pubmed_xml(filepath)
    for article in articles_data:
        insert_article_data(connection, article)  
    connection.close()
