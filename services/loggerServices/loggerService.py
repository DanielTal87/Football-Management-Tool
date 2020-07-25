#!/usr/bin/python3

import logging
import datetime

from services.singletonService.singletonServiceMetaClass import SingletonMetaClass


class LoggerService(metaclass=SingletonMetaClass):
    def __init__(self):
        self.logger = logging.getLogger("FMT")
        logging.basicConfig(filename=f'logs/FMT-{datetime.date.today()}.log',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
