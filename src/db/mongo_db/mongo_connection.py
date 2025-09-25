from pymongo import ASCENDING, AsyncMongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from src.config import settings

client: AsyncMongoClient = AsyncMongoClient(settings.get_url_mg)

mg_db: Database = client.test

QuotesData: Collection = mg_db.QuotesData

async def init_db():
    await QuotesData.create_index(
        [
            ("author", 1),
            ("text", 1),
            ("tags", 1)
        ],
        unique=False
    )