from pymongo import ASCENDING, MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from src.config import settings

client: MongoClient = MongoClient(settings.get_url_mg)

mg_db: Database = client.test

QuotesData: Collection = mg_db.QuotesData

def init_db():
    QuotesData.create_index(
        [
            ("author", 1),
            ("text", 1),
            ("tags", 1),
            ("created_at", 1)
        ],
        unique=True
    )