from opensearchpy import OpenSearch
import os
from .models import Article
from opensearchpy import OpenSearch
from django.conf import settings


OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST', 'localhost')
OPENSEARCH_PORT = int(os.getenv('OPENSEARCH_PORT', 9200))

client = OpenSearch(
    hosts=[{'host': settings.OPENSEARCH_HOST, 'port': settings.OPENSEARCH_PORT}],
    http_auth=('admin', 'admin'),  # əgər auth aktivdirsə
    use_ssl=False,
    verify_certs=False
)


INDEX_NAME = 'articles'

def create_index():
    index_name = "articles"
    if not client.indices.exists(index=index_name):
        client.indices.create(
            index=index_name,
            body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "author": {"type": "keyword"},
                        "created_at": {"type": "date"}
                    }
                }
            }
        )
        print("✅ Index created:", index_name)
    else:
        print("ℹ️ Index already exists")



def index_article(article):
    client.index(
        index=INDEX_NAME,
        id=article.id,
        body={
            'title': article.title,
            'content': article.content,
            'author': article.author.username,
            'created_at': article.created_at.isoformat()
        }
    )
def search_articles(query):
    response = client.search(
        index=INDEX_NAME,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "content"]
                }
            }
        }
    )
    hits = [
        {
            "id": hit["_id"],  # burda article.id kimi işlədə bilərsən
            **hit["_source"]
        }
        for hit in response['hits']['hits']
    ]
    return hits


def index_all_articles():
    for article in Article.objects.all():
        client.index(
            index="articles",
            id=article.pk,
            body={
                "title": article.title,
                "content": article.content,
                "author": article.author.username,
                "created_at": article.created_at,
            }
        )
    print("✅ All articles indexed!")
