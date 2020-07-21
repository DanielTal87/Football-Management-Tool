#!/usr/bin/python3
from services.loggerServices.loggerService import LoggerService

logger = LoggerService().logger


def create_match(self, data):
    return self.client.FMT["matches"].insert_one(data).inserted_id


def get_match(self, data):
    return self.client.FMT["matches"].find_one(data)


def parse_match_from_request(request):
    return {
        "home_team": request.get("home_team"),
        "away_team": request.get("away_team"),
        "date": request.get("date")
    }


def parse_match_from_db(request):
    return {
        "id": str(request.get("_id")),
        "home_team": request.get("home_team"),
        "away_team": request.get("away_team"),
        "date": request.get("date", None),
        "number_of_wins": request.get("number_of_wins", None),
        "score": request.get("score", None),
        "is_draw": request.get("is_draw", None),
        "team_won": request.get("team_won", None),
        "team_lost": request.get("team_lost", None)
    }
