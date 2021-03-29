import pymongo
from settings import DB_NAME, DB_STREETS_COLLECTION
from typing import List, Dict
import datetime
from bson.son import SON
import os


# Generic Database connection

def db_connection():
    dbconn = pymongo.MongoClient(host=os.environ['MONGODB_HOST'],
                                 port=os.environ['MONGODB_PORT'])
    return dbconn


def bulk_upsert(conn, db, collection, items: List[Dict]):
    operations = []
    for item in items:
        if '_id' not in item:
            raise ValueError('_id field missing from item. required for upsert')
        operations.append(pymongo.UpdateOne({'_id': item['_id']}, {'$set': item}, upsert=True))

        # Send in batches of 1000
        if len(operations) == 1000:
            conn[db][collection].bulk_write(operations, ordered=False)
            operations = []

    if len(operations) > 0:
        conn[db][collection].bulk_write(operations, ordered=False)


def search_streets(conn, term):
    today = todays_date()
    future_date = today + datetime.timedelta(days=8)
    search_term = f'.*{term}.*'.replace(" ", "_")
    collection = conn[DB_NAME][DB_STREETS_COLLECTION]
    results = collection.aggregate(
        [
            {'$match': {'_id': {'$regex': search_term, "$options": "-i"}, 'date': {'$gt': today, '$lt': future_date}}},
            {'$group': {'_id': '$street', 'city': {'$first': '$city'}, 'count': {'$sum': 1}}},
            {'$sort': SON([('city', 1), ('street', 1)])}
        ]
    )
    return list(results)


def get_days(conn, city, street):
    today = todays_date()

    collection = conn[DB_NAME][DB_STREETS_COLLECTION]
    results = collection.find(
        {
            "_id": {"$regex": "^" + street + "_[0-9]{4}-[0-9]{2}-[0-9]{2}$", "$options": "-i"},
            "date": {"$gt": today},
            "city": {"$regex": "^" + city + "$", "$options": "-i"}
        }
    )
    return list(results)


def streets_paged(conn, city, page):
    today = todays_date()
    future_date = today + datetime.timedelta(days=8)
    limit = 100
    collection = conn[DB_NAME][DB_STREETS_COLLECTION]
    skip = 0
    if page > 1:
        skip = (page - 1) * limit

    results = collection.aggregate(
        [
            {'$match': {'date': {'$gt': today, '$lt': future_date}, 'city': city.lower()}},
            {'$sort': SON([('_id', 1)])},
            {'$group': {'_id': '$street', 'city': {'$first': '$city'}, 'count': {'$sum': 1}}},
            {'$sort': SON([('_id', 1)])},
            {"$limit": skip + limit},
            {"$skip": skip}
        ]
    )

    return list(results)


def todays_date():
    today = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    return today
