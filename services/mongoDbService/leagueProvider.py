#!/usr/bin/python3
from services.loggerServices.loggerService import LoggerService

logger = LoggerService().logger


def create_league(self, data):
    return self.client.FMT["leagues"].insert_one(data).inserted_id


def find_league(self, data):
    return self.client.FMT["leagues"].find_one(data)


def add_team_to_league(self, league_id, team_id):
    return self.client.FMT["leagues"].update_one({'_id': league_id}, {'$push': {'teams': team_id}})

def parse_league_from_request(request):
    return {
        "name": request.get("name"),
        "season": request.get("season"),
        "teams": request.get("teams", [])
    }


def parse_league_from_db(request):
    return {
        "id": str(request.get("_id")),
        "name": request.get("name"),
        "season": request.get("season"),
        "teams": request.get("teams")
    }
