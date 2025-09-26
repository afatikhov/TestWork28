from pymongo import ASCENDING, AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.database import Database
from config import settings

client_async: AsyncMongoClient = AsyncMongoClient(settings.get_url_mg)

mg_db_async: Database = client_async.test

QuotesData: AsyncCollection = mg_db_async.QuotesData