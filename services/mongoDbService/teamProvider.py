#!/usr/bin/python3
from services.loggerServices.loggerService import LoggerService

logger = LoggerService().logger


def create_team(self, data):
    return self.client.FMT["teams"].insert_one(data).inserted_id


def update_team(self, data):
    return self.client.FMT["teams"].update_one(data, upsert=True).inserted_id


def update_team_with_draw(self, data, goals_scored, match_id):
    return self.client.FMT["teams"].update_one(data, {'$inc': {'number_of_scored_goals': int(goals_scored),
                                                               'number_of_received_goals': int(goals_scored),
                                                               'number_of_draws': 1},
                                                      '$push': {'matches_draw': match_id}},
                                               upsert=False)


def update_winning_team(self, data, goals_scored, goals_received, match_id):
    return self.client.FMT["teams"].update_one(data, {'$inc': {'number_of_scored_goals': int(goals_scored),
                                                               'number_of_received_goals': int(goals_received),
                                                               'number_of_wins': 1},
                                                      '$push': {'matches_wins': match_id}},
                                               upsert=False)


def update_losing_team(self, data, goals_scored, goals_received, match_id):
    return self.client.FMT["teams"].update_one(data, {'$inc': {'number_of_scored_goals': int(goals_scored),
                                                               'number_of_received_goals': int(goals_received),
                                                               'number_of_losses': 1},
                                                      '$push': {'matches_loss': match_id}},
                                               upsert=False)


def find_team(self, data):
    return self.client.FMT["teams"].find_one(data)


def parse_team_from_request(request):
    return {
        "name": request.get("name"),
        "season": request.get("season")
    }


def init_team(request):
    return {
        "name": request.get("name"),
        "season": request.get("season"),
        "number_of_wins": request.get("number_of_wins", 0),
        "matches_wins": request.get("matches_wins", []),
        "number_of_losses": request.get("number_of_losses", 0),
        "matches_loss": request.get("matches_loss", []),
        "number_of_draws": request.get("number_of_draws", 0),
        "matches_draw": request.get("matches_draw", []),
        "number_of_scored_goals": request.get("number_of_scored_goals", 0),
        "number_of_received_goals": request.get("number_of_received_goals", 0)
    }


def find_team_most_scored(teams):
    return max(teams, key=lambda d: d['number_of_scored_goals'])


def find_team_least_scored(teams):
    return min(teams, key=lambda d: d['number_of_scored_goals'])


def find_team_most_wins(teams):
    return max(teams, key=lambda d: d['number_of_wins'])


def find_team_least_wins(teams):
    return min(teams, key=lambda d: d['number_of_wins'])


def parse_team_from_db(request):
    return {
        "id": str(request.get("_id")),
        "name": request.get("name"),
        "season": request.get("season"),
        "number_of_wins": request.get("number_of_wins", 0),
        "matches_wins": request.get("matches_wins", []),
        "number_of_losses": request.get("number_of_losses", 0),
        "matches_loss": request.get("matches_loss", []),
        "number_of_draws": request.get("number_of_draws", 0),
        "matches_draw": request.get("matches_draw", []),
        "number_of_scored_goals": request.get("number_of_scored_goals", 0),
        "number_of_received_goals": request.get("number_of_received_goals", 0)
    }
