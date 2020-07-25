#!/usr/bin/python3
from services.loggerServices.loggerService import LoggerService

logger = LoggerService().logger


def create_match(self, data):
    return self.client.FMT["matches"].insert_one(data).inserted_id


def update_match(self, data):
    return self.client.FMT["matches"].update_one(data, upsert=True).inserted_id


def find_match(self, data):
    return self.client.FMT["matches"].find_one(data)


def parse_match_from_request(request):
    return {
        "home_team": request.get("home_team"),
        "away_team": request.get("away_team"),
        "date": request.get("date")
    }


def parse_ended_match_from_request(request):
    match = parse_match_from_request(request)
    match["score"] = request.get("score").replace(' ', '')
    return match


def parse_ended_match_to_db(request):
    parsed_match = {
        "home_team": request.get("home_team"),
        "away_team": request.get("away_team"),
        "date": request.get("date"),
        "score": request.get("score")
    }
    home_team_score = parsed_match["score"].split('-')[0]
    away_team_score = parsed_match["score"].split('-')[1]
    #   parse match result
    if home_team_score == away_team_score:
        parsed_match['is_draw'] = True
        parsed_match['team_won_score'] = home_team_score
    else:
        parsed_match['is_draw'] = False
        if home_team_score > away_team_score:
            parsed_match['team_won'] = parsed_match['home_team']
            parsed_match['team_won_score'] = home_team_score
            parsed_match['team_lost'] = parsed_match['away_team']
            parsed_match['team_lose_score'] = away_team_score
        else:
            parsed_match['team_won'] = parsed_match['away_team']
            parsed_match['team_won_score'] = away_team_score
            parsed_match['team_lost'] = parsed_match['home_team']
            parsed_match['team_lose_score'] = home_team_score

    return parsed_match


def parse_match_from_db(request):
    return {
        "id": str(request.get("_id")),
        "home_team": request.get("home_team"),
        "away_team": request.get("away_team"),
        "date": request.get("date", None),
        "score": request.get("score", None),
        "is_draw": request.get("is_draw", None),
        "team_won": request.get("team_won", None),
        "team_lost": request.get("team_lost", None)
    }
