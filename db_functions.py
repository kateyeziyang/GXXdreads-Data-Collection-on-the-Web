"""
Helper functions for manipulating database
"""

import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
db_key = os.getenv("DB_KEY")
client = pymongo.MongoClient(db_key)


def get_filter_str(args):
    """
    Generate mongodb filter string such that field contains args (no need to be equal!)
    :param args: input args with format {"field1": "attr1", "field2": "attr2", ...}
    :return: mongodb filter string
    """
    my_list = {}
    for k, v in args.items():
        value_str = ".*" + v + ".*"
        my_list[k] = {'$regex': value_str, "$options": 'i'}
    return my_list


def get_entries(args, _collection):
    """
    Get filtered results
    :param args: input args with format {"field1": "attr1", "field2": "attr2", ...}
    :param _collection: name of collection
    :return: a list of dictionary
    """
    collection = client.data[_collection]
    my_list = get_filter_str(args)
    result = collection.find(my_list, {"_id": 0})
    return [elem for elem in result]


def add_entries(doc, mode, _collection):
    """
    Add new document
    :param doc: document to be inserted
    :param mode: decide which mode (many, one)
    :param _collection: name of collection 
    :return:
    """
    collection = client.data[_collection]
    if mode:
        collection.insert_many(doc)
    else:
        collection.insert_one(doc)


def del_entries(args, _collection):
    """
    Delete one document
    :param args: input args with format {"field1": "attr1", "field2": "attr2", ...}
    :param _collection: name of collection 
    :return: 
    """
    collection = client.data[_collection]
    my_list = get_filter_str(args)
    collection.delete_one(my_list)


def update_entries(doc, args, _collection):
    """
    Update document(s)
    :param doc: document to be inserted
    :param args: input args with format {"field1": "attr1", "field2": "attr2", ...}
    :param _collection: name of collection 
    :return: 
    """
    collection = client.data[_collection]
    my_list = get_filter_str(args)
    result = collection.find_one(my_list, {"_id": 0})
    if result:
        set_dict = {"$set": doc}
        collection.update_one(my_list, set_dict)
    else:
        collection.insert_one(doc)


def advanced_search(args, mode, field, _collection):
    """
    And and Or Search.
    :param args: input args with format {"field1": "attr1", "field2": "attr2", ...}
    :param mode: decide which mode (many, one)
    :param field: field to be matched
    :param _collection: name of collection 
    :return: a list of dictionary
    """
    collection = client.data[_collection]
    my_list = []
    for k, v in args.items():
        value_str = ".*"+v+".*"
        my_list.append({field: {"$regex": value_str, "$options": 'i'}})
    if mode:
        result = collection.find({"$and": my_list}, {"_id": 0})
        return [elem for elem in result]
    else:
        result = collection.find({"$or": my_list}, {"_id": 0})
        return [elem for elem in result]


def get_most_similar_books():
    collection = client.data['books']
    result = collection.aggregate([
        {"$unwind": "$similar_books"},
        {"$group": {"_id": "$_id", "count": {"$sum": 1}, "title": {"$first": '$title'}, }},
        {"$project": {"_id": 0}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ])
    my_list = [r for r in result]
    return my_list


def get_most_similar_authors():
    collection = client.data['authors']
    result = collection.aggregate([
        {"$unwind": "$related_authors"},
        {"$group": {"_id": "$_id", "count": {"$sum": 1}, "name": {"$first": '$name'}, }},
        {"$project": {"_id": 0}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ])
    my_list = [r for r in result]
    return my_list


def get_all_books(_collection):
    collection = client.data[_collection]
    result = collection.find({}, {"_id": 0, "title": 1, "author": 1})
    return [elem for elem in result]


def get_all_authors(_collection):
    collection = client.data[_collection]
    result = collection.find({}, {"_id": 0, "name": 1})
    return [elem for elem in result]
