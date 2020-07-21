#!/usr/bin/python3

import json
import os
from services.singletonService.singletonServiceMetaClass import SingletonMetaClass


class ConfigService(metaclass=SingletonMetaClass):
    def __init__(self):
        with open(os.path.join("config", "config.json"), "rb") as json_file:
            self.config = json.load(json_file)
