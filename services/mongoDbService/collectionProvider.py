#!/usr/bin/python3
import pymongo

from services.loggerServices.loggerService import LoggerService

logger = LoggerService().logger
COLLECTIONS_NAMES = ['leagues', 'teams', 'matches']

"""
The Collection Provider add to the MongoDB all the collections and index them
"""


def create_collections(self):
    existing_collection = self.client.FMT.list_collection_names()
    for collection in COLLECTIONS_NAMES:
        if collection not in existing_collection:
            create_collection(self, collection)


def create_collection(self, collection):
    try:
        self.client.FMT.create_collection(collection)
        index_collections(self, collection)
        logger.info(f'MongoDbService/create_collection - collection "{collection}" created successfully')
    except Exception as error:
        # collection already exists
        if "already exists" in error._message:
            logger.info(f'MongoDbService/create_collection - the collection "{collection}" already exist')
            pass


def index_collections(self, collection):
    switcher = {
        'leagues': create_index_leagues(self),
        'teams': create_index_teams(self),
        # 'matches': self.create_index_matches()
    }
    return switcher.get(collection, "Invalid Collection")


def create_index_leagues(self):
    self.client.FMT.leagues.create_index(
        [("name", pymongo.ASCENDING), ("season", pymongo.ASCENDING)],
        unique=True)


def create_index_teams(self):
    self.client.FMT.teams.create_index(
        [("name", pymongo.ASCENDING), ("season", pymongo.ASCENDING)],
        unique=True)


def create_index_matches(self):
    self.client.FMT.matches.create_index(
        [("name", pymongo.ASCENDING), ("season", pymongo.ASCENDING)],
        unique=True)
