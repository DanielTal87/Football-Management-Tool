#!/usr/bin/python3
from services.loggerServices.loggerService import LoggerService

logger = LoggerService().logger


def create_team(self, data):
    return self.client.FMT["teams"].insert_one(data).inserted_id


def get_team(self, data):
    return self.client.FMT["teams"].find_one(data)


def parse_team_from_request(request):
    return {
        "name": request.get("name"),
        "season": request.get("season")
    }


def parse_team_from_db(request):
    return {
        "id": str(request.get("_id")),
        "name": request.get("name"),
        "season": request.get("season"),
        "number_of_wins": request.get("number_of_wins", None),
        "matches_wins": request.get("matches_wins", []),
        "number_of_losses": request.get("number_of_losses", None),
        "matches_loss": request.get("matches_loss", []),
        "number_of_draws": request.get("number_of_draws", None),
        "matches_draw": request.get("matches_draw", []),
        "number_of_scored_goals": request.get("number_of_scored_goals", None),
        "number_of_received_goals": request.get("number_of_received_goals", None)
    }
