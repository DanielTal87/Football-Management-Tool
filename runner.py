#!/usr/bin/python3

import logging

from server.server import app
from services.mongoDbService.mongoDbService import MongoDbService
from services.singletonService.singletonServiceMetaClass import SingletonMetaClass

try:
    logging.info('#################### Football Management Tool - Server Started ####################')
    mongodb = MongoDbService()
    app.run(host='0.0.0.0', port=8080, debug=False, access_log=True)
    logging.info('#################### Football Management Tool Server - Finished ####################')
except KeyError as e:
    SingletonMetaClass.clear()
