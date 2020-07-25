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
        if "already exists" in str(error.message):
            logger.info(f'MongoDbService/create_collection - the collection "{collection}" already exist')
            pass


def create_index_leagues(self):
    self.client.FMT.leagues.create_index(
        [("name", pymongo.ASCENDING), ("season", pymongo.ASCENDING)],
        unique=True)
    return True


def create_index_teams(self):
    self.client.FMT.teams.create_index(
        [("name", pymongo.ASCENDING), ("season", pymongo.ASCENDING)],
        unique=True)
    return True


def create_index_matches(self):
    self.client.FMT.matches.create_index(
        [("home_team", pymongo.ASCENDING), ("away_team", pymongo.ASCENDING), ("date", pymongo.ASCENDING)],
        unique=True)
    return True


def index_collections(self, collection):
    if collection == 'leagues':
        create_index_leagues(self)
    elif collection == 'teams':
        create_index_teams(self)
    elif collection == 'matches':
        create_index_matches(self)
    else:
        raise Exception("Invalid Collection")
