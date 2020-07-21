#!/usr/bin/python3

import logging
import datetime


class LoggerService:
    def __init__(self):
        self.logger = logging.getLogger("FMT")
        logging.basicConfig(filename=f'logs/FMT-{datetime.date.today()}.log',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
