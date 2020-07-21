#!/usr/bin/python3

import pymongo
from pymongo.errors import DuplicateKeyError

from services.configServices.configService import ConfigService
from services.loggerServices.loggerService import LoggerService
from services.mongoDbService.collectionProvider import create_collections
from services.mongoDbService.leagueProvider import (create_league, get_league)
from services.mongoDbService.teamProvider import (create_team, get_team)

config = ConfigService().config
logger = LoggerService().logger


class MongoDbService:
    def __init__(self):
        logger.info(f'MongoDbService/init - start')
        self.client = pymongo.MongoClient(config['mongodb']['url'], config['mongodb']['port'])
        logger.debug(f'MongoDbService/init - calling collectionProvider/create_collections')
        create_collections(self)
        logger.info(f'MongoDbService/init - end')

    def create_league(self, data):
        logger.info(f'MongoDbService/create_league - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/create_league - calling leagueProvider/create_league')
            _id = create_league(self, data)
            logger.debug(f'MongoDbService/create_league - leagueProvider/create_league succeeded | id: {_id}')

        # League already exists
        except DuplicateKeyError as error:
            logger.error(f'MongoDbService/create_league failed - duplicate key error | error: {error}')
            raise Exception('League is already exists - name and season must be unique')

        except Exception as error:
            logger.error(f'MongoDbService/create_league failed | error: {error}')
            raise

        else:
            return _id

    def get_league(self, data):
        logger.info(f'MongoDbService/get_league - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/get_league - calling leagueProvider/get_league')
            _league = get_league(self, data)
            logger.debug(f'MongoDbService/get_league - leagueProvider/get_league succeeded | league: {_league}')

            if _league is None:
                raise Exception('The league is not exists')

        except Exception as error:
            logger.error(f'MongoDbService/get_league failed | error: {error}')
            raise

        else:
            return _league

    def create_team(self, data):
        logger.info(f'MongoDbService/create_team - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/create_team - calling teamProvider/create_team')
            _id = create_team(self, data)
            logger.debug(f'MongoDbService/create_team - teamProvider/create_team succeeded | id: {_id}')

        # Team already exists
        except DuplicateKeyError as error:
            logger.error(f'MongoDbService/create_team failed - duplicate key error | error: {error}')
            raise Exception('Team is already exists - name and season must be unique')

        except Exception as error:
            logger.error(f'MongoDbService/create_team failed | error: {error}')
            raise

        else:
            return _id

    def get_team(self, data):
        logger.info(f'MongoDbService/get_team - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/get_team - calling teamProvider/get_team')
            _team = get_team(self, data)
            logger.debug(f'MongoDbService/get_team - teamProvider/get_team succeeded | team: {_team}')

            if _team is None:
                raise Exception('The team is not exists')

        except Exception as error:
            logger.error(f'MongoDbService/get_team failed | error: {error}')
            raise

        else:
            return _team
