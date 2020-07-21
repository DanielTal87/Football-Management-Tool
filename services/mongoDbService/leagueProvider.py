#!/usr/bin/python3
from services.loggerServices.loggerService import LoggerService

logger = LoggerService().logger


def create_league(self, data):
    return self.client.FMT["leagues"].insert_one(data).inserted_id


def get_league(self, data):
    return self.client.FMT["leagues"].find_one(data)


def parse_league_from_request(request):
    return {
        "name": request.get("name"),
        "season": request.get("season")
    }


def parse_league_from_db(request):
    return {
        "id": str(request.get("_id")),
        "name": request.get("name"),
        "season": request.get("season"),
        "teams": request.get("teams", []),
        "matches": request.get("teams", [])
    }
