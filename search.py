import os
from queries import basic_search, get_unique_values, advanced_search
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

client = Elasticsearch(hosts=["http://localhost"], http_auth=("elastic", os.getenv('ELASTCSEARCH_PASSWORD')), port=os.getenv('ELASTCSEARCH_PORT'))

INDEX = os.getenv('ELASTCSEARCH_INDEX')

def search(query, year, yearmust, movie, moviemust, composer, composermust, lyricist, lyricistmust, singer, singermust):
    query_body = advanced_search(query, year, yearmust, movie, moviemust, composer, composermust, lyricist, lyricistmust, singer, singermust)
    print('Making Advanced Search ')
    res = client.search(index=INDEX, body=query_body)
    return res

def getUniqueDetails():
    query_body = get_unique_values()
    print('Get Details Invoked')
    res = client.search(index=INDEX, body=query_body)
    return res