#!/usr/bin/python3

from sanic import Sanic
from sanic.response import json as rjson
from bson import ObjectId
from jsonschema import validate as validate_schema, ValidationError
from datetime import datetime
from re import match as regex_match

from services.loggerServices.loggerService import LoggerService
from services.mongoDbService.leagueProvider import (parse_league_from_request, parse_league_from_db)
from services.mongoDbService.teamProvider import (parse_team_from_request, parse_team_from_db, find_team_most_scored,
                                                  find_team_least_scored, find_team_most_wins, find_team_least_wins)
from services.mongoDbService.matchProvider import (parse_match_from_db, parse_match_from_request,
                                                   parse_ended_match_from_request)
from services.mongoDbService.mongoDbService import MongoDbService
from models.models import (LeagueSchema, TeamSchema, MatchSchema)

logger = LoggerService().logger
app = Sanic()
db = MongoDbService()

"""
League Routes
"""


@app.post('/league')
async def post_handler_league(request):
    """
    Create a new League
    :param request:
        name : String - the league name
        season : Number - the season year
    :return
    request example
        {
            "name": Spanish
            "season": 2020
        }
    """
    logger.info(f'Server/Create League - start | request: {request.json}')
    try:
        logger.debug(
            f'Server/Create League - calling validate_schema | request: {request.json}, schema: {LeagueSchema}')
        validate_schema(instance=request.json, schema=LeagueSchema)
        logger.debug('Server/Create League - input validation succeeded')

        logger.debug(
            f'Server/Create League - calling leagueProvider/parse_league_from_request | request: {request.json}, schema: {LeagueSchema}')
        parsed_request = parse_league_from_request(request.json)
        logger.debug(
            f'Server/Create League - leagueProvider/parse_league_from_request succeeded | parsed request: {parsed_request}')

        logger.debug(f'Server/Create League - calling MongoDbService/create_league | request: {parsed_request}')
        _id = db.create_league(parsed_request)
        logger.debug(f'Server/Create League - MongoDbService/create_league succeeded | league id: {_id}')

    except ValidationError as error:
        logger.error(f'Server/Create League failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Create League failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Create League succeeded - id: {_id}')
        return rjson({
            'status': "success",
            'message': 'the league added',
            'id': str(_id)
        }, status=200)

    finally:
        logger.info(f'Server/Create League - end')


@app.get('/league/<name:string>/<season:number>')
async def get_handler_league_by_name_season(request, name, season):
    """
    Get a League by name & season
    :param
        name : String - the league name
        season : Number - the season year
    :return
    response example
        {
            "name": Spanish
            "season": 2020,
            "teams": ["real madrid", "hapoel jerusalem"],
            "matches": [match_id_#1, match_id_#2, match_id_#3]
        }
    """
    logger.info(f'Server/Get League by name & season - start | name: {name}, season: {season}')
    try:
        parsed_request = {
            "name": name,
            "season": season
        }
        logger.debug(
            f'Server/Get League by name & season - calling validate_schema | request: {parsed_request}, schema: {LeagueSchema}')
        validate_schema(instance=parsed_request, schema=LeagueSchema)
        logger.debug('Server/Get League by name & season - input validation succeeded')

        logger.debug(
            f'Server/Get League by name & season - calling MongoDbService/find_league | request: {parsed_request}')
        _league = db.find_league(parsed_request)
        logger.debug(f'Server/Get League by name & season - MongoDbService/find_league succeeded | league: {_league}')

        logger.debug(
            f'Server/Get League by name & season - calling leagueProvider/parse_league_from_db | league: {_league}')
        parsed_league = parse_league_from_db(_league)
        logger.debug(
            f'Server/Get League by name & season - leagueProvider/parse_league_from_db succeeded | parsed league: {parsed_league}')

    except ValidationError as error:
        logger.error(f'Server/Get League by name & season failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Get League by name & season failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get League by name & season succeeded - id: {parsed_league}')
        return rjson({
            'status': "success",
            'message': 'success',
            'league': str(parsed_league)
        }, status=200)

    finally:
        logger.info(f'Server/Get League by name & season - end')


@app.get('/league/<league_id:string>')
async def get_handler_league_by_id(request, league_id):
    """
    Get a League
    :param
        name : String - the league name
        season : Number - the season year
    :return
    request example
        {
            "name": Spanish
            "season": 2020,
            "teams": ["real madrid", "hapoel jerusalem"],
            "matches": [match_id_#1, match_id_#2, match_id_#3]
        }
    """
    logger.info(f'Server/Get League by id - start | id: {league_id}')
    try:
        parsed_request = {
            "_id": ObjectId(league_id)
        }

        logger.debug(f'Server/Get League by id - calling MongoDbService/find_league | request: {parsed_request}')
        _league = db.find_league(parsed_request)
        logger.debug(f'Server/Get League by id - MongoDbService/find_league succeeded | league: {_league}')

        logger.debug(f'Server/Get League by id - calling leagueProvider/parse_league_from_db | league: {_league}')
        parsed_league = parse_league_from_db(_league)
        logger.debug(
            f'Server/Get League by id - leagueProvider/parse_league_from_db succeeded | parsed league: {parsed_league}')

    except Exception as error:
        logger.error(f'Server/Get League by id failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get League by id succeeded - league: {parsed_league}')
        return rjson({
            'status': "success",
            'message': 'success',
            'league': str(parsed_league)
        }, status=200)

    finally:
        logger.info(f'Server/Get League by id - end')


@app.post('/league/add_team')
async def post_handler_add_league(request):
    """
    Add team to a league
    :param request:
        league_id : String - the league id
        team_id : String - the team id
    :return
    request example
        {
            "name": Spanish
            "season": 2020
        }
    """
    logger.info(f'Server/Add Team To League - start | request: {request.json}')
    try:
        parsed_request = {
            "league_id": ObjectId(request.json.get("league_id")),
            "team_id": ObjectId(request.json.get("team_id"))
        }

        logger.debug(
            f'Server/Add Team To League - calling MongoDbService/add_team_to_league | parsed request: {parsed_request}')
        _id = db.add_team_to_league(parsed_request)
        logger.debug(f'Server/Add Team To League - MongoDbService/add_team_to_league succeeded | league id: {_id}')

    except ValidationError as error:
        logger.error(f'Server/Add Team To League failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Add Team To League failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Add Team To League succeeded - id: {_id}')
        return rjson({
            'status': "success",
            'message': 'the team added to the league',
            'id': str(_id)
        }, status=200)

    finally:
        logger.info(f'Server/Add Team To League - end')


@app.get('/league/most_goals/<name:string>/<season:number>')
async def get_handler_team_that_score_the_most(request, name, season):
    """
    Get the team most score in league
    :param
        name : String - the league name
        season : Number - the season year
    :return

    """
    logger.info(f'Server/Get Team that score the most in league - start | name: {name}, season: {season}')
    try:
        parsed_request = {
            "name": name,
            "season": season
        }
        logger.debug(
            f'Server/Get Team that score the most in league - calling validate_schema | request: {parsed_request}, schema: {LeagueSchema}')
        validate_schema(instance=parsed_request, schema=LeagueSchema)
        logger.debug('Server/Get Team that score the most in league - input validation succeeded')

        logger.debug(
            f'Server/Get Team that score the most in league - calling MongoDbService/find_league | request: {parsed_request}')
        _league = db.find_league(parsed_request)
        logger.debug(
            f'Server/Get Team that score the most in league - MongoDbService/find_league succeeded | league: {_league}')

        logger.debug(
            f'Server/Get Team that score the most in league - calling leagueProvider/parse_league_from_db | league: {_league}')
        parsed_league = parse_league_from_db(_league)
        logger.debug(
            f'Server/Get Team that score the most in league - leagueProvider/parse_league_from_db succeeded | parsed league: {parsed_league}')

        logger.debug(
            f'Server/Get Team that score the most in league - calling MongoDbService/find_teams_from_league | league: {parsed_league}')
        teams = db.find_teams_from_league(parsed_league)
        logger.debug(
            f'Server/Get Team that score the most in league - MongoDbService/find_teams_from_league succeeded | parsed league: {parsed_league}')

        logger.debug(
            f'Server/Get Team that score the most in league - calling teamProvider/find_team_most_scored | teams: {teams}')
        team_scored_most = find_team_most_scored(teams)
        logger.debug(
            f'Server/Get Team that score the most in league - teamProvider/find_team_most_scored succeeded | most scored team: {team_scored_most}')

    except ValidationError as error:
        logger.error(f'Server/Get Team that score the most in league failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Get Team that score the most in league failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Team that score the most in league succeeded - id: {parsed_league}')
        return rjson({
            'status': "success",
            'message': f'The team that scored the most goals in {parsed_request["name"]}, Amount of goals: {team_scored_most["number_of_scored_goals"]}',
            'team name': str(team_scored_most['name'])
        }, status=200)

    finally:
        logger.info(f'Server/Get Team that score the most in league - end')


@app.get('/league/least_goals/<name:string>/<season:number>')
async def get_handler_team_that_score_the_least(request, name, season):
    """
    Get the team least score in league
    :param
        name : String - the league name
        season : Number - the season year
    :return

    """
    logger.info(f'Server/Get Team that score the least in league - start | name: {name}, season: {season}')
    try:
        parsed_request = {
            "name": name,
            "season": season
        }
        logger.debug(
            f'Server/Get Team that score the least in league - calling validate_schema | request: {parsed_request}, schema: {LeagueSchema}')
        validate_schema(instance=parsed_request, schema=LeagueSchema)
        logger.debug('Server/Get Team that score the least in league - input validation succeeded')

        logger.debug(
            f'Server/Get Team that score the least in league - calling MongoDbService/find_league | request: {parsed_request}')
        _league = db.find_league(parsed_request)
        logger.debug(
            f'Server/Get Team that score the least in league - MongoDbService/find_league succeeded | league: {_league}')

        logger.debug(
            f'Server/Get Team that score the least in league - calling leagueProvider/parse_league_from_db | league: {_league}')
        parsed_league = parse_league_from_db(_league)
        logger.debug(
            f'Server/Get Team that score the least in league - leagueProvider/parse_league_from_db succeeded | parsed league: {parsed_league}')

        logger.debug(
            f'Server/Get Team that score the least in league - calling MongoDbService/find_teams_from_league | league: {parsed_league}')
        teams = db.find_teams_from_league(parsed_league)
        logger.debug(
            f'Server/Get Team that score the least in league - MongoDbService/find_teams_from_league succeeded | parsed league: {parsed_league}')

        logger.debug(
            f'Server/Get Team that score the least in league - calling teamProvider/find_team_most_scored | teams: {teams}')
        team_scored_least = find_team_least_scored(teams)
        logger.debug(
            f'Server/Get Team that score the least in league - teamProvider/find_team_most_scored succeeded | most scored team: {team_scored_least}')

    except ValidationError as error:
        logger.error(f'Server/Get Team that score the least in league failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Get Team that score the least in league failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Team that score the least in league succeeded - id: {parsed_league}')
        return rjson({
            'status': "success",
            'message': f'The team that scored the least goals in {parsed_request["name"]}, Amount of goals: {team_scored_least["number_of_scored_goals"]}',
            'team name': str(team_scored_least['name'])
        }, status=200)

    finally:
        logger.info(f'Server/Get Team that score the least in league - end')


@app.get('/league/most_wins/<name:string>/<season:number>')
async def get_handler_team_that_wins_the_most(request, name, season):
    """
    Get the team most wins in league
    :param
        name : String - the league name
        season : Number - the season year
    :return

    """
    logger.info(f'Server/Get Team that win the most in league - start | name: {name}, season: {season}')
    try:
        parsed_request = {
            "name": name,
            "season": season
        }
        logger.debug(
            f'Server/Get Team that win the most in league - calling validate_schema | request: {parsed_request}, schema: {LeagueSchema}')
        validate_schema(instance=parsed_request, schema=LeagueSchema)
        logger.debug('Server/Get Team that score the most in league - input validation succeeded')

        logger.debug(
            f'Server/Get Team that win the most in league - calling MongoDbService/find_league | request: {parsed_request}')
        _league = db.find_league(parsed_request)
        logger.debug(
            f'Server/Get Team that win the most in league - MongoDbService/find_league succeeded | league: {_league}')

        logger.debug(
            f'Server/Get Team that win the most in league - calling leagueProvider/parse_league_from_db | league: {_league}')
        parsed_league = parse_league_from_db(_league)
        logger.debug(
            f'Server/Get Team that win the most in league - leagueProvider/parse_league_from_db succeeded | parsed league: {parsed_league}')

        logger.debug(
            f'Server/Get Team that win the most in league - calling MongoDbService/find_teams_from_league | league: {parsed_league}')
        teams = db.find_teams_from_league(parsed_league)
        logger.debug(
            f'Server/Get Team that win the most in league - MongoDbService/find_teams_from_league succeeded | parsed league: {parsed_league}')

        logger.debug(
            f'Server/Get Team that win the most in league - calling teamProvider/find_team_most_wins | teams: {teams}')
        team_win_most = find_team_most_wins(teams)
        logger.debug(
            f'Server/Get Team that win the most in league - teamProvider/find_team_most_wins succeeded | team win most: {team_win_most}')

    except ValidationError as error:
        logger.error(f'Server/Get Team that win the most in league failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Get Team that win the most in league failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Team that win the most in league succeeded - id: {parsed_league}')
        return rjson({
            'status': "success",
            'message': f'The team that win the most wins in {parsed_request["name"]}, Amount of wins: {team_win_most["number_of_wins"]}',
            'team name': str(team_win_most['name'])
        }, status=200)

    finally:
        logger.info(f'Server/Get Team that win the most in league - end')


@app.get('/league/least_wins/<name:string>/<season:number>')
async def get_handler_team_that_wins_the_least(request, name, season):
    """
    Get the team least wins in league
    :param
        name : String - the league name
        season : Number - the season year
    :return

    """
    logger.info(f'Server/Get Team that win the least in league - start | name: {name}, season: {season}')
    try:
        parsed_request = {
            "name": name,
            "season": season
        }
        logger.debug(
            f'Server/Get Team that win the least in league - calling validate_schema | request: {parsed_request}, schema: {LeagueSchema}')
        validate_schema(instance=parsed_request, schema=LeagueSchema)
        logger.debug('Server/Get Team that score the least in league - input validation succeeded')

        logger.debug(
            f'Server/Get Team that win the least in league - calling MongoDbService/find_league | request: {parsed_request}')
        _league = db.find_league(parsed_request)
        logger.debug(
            f'Server/Get Team that win the least in league - MongoDbService/find_league succeeded | league: {_league}')

        logger.debug(
            f'Server/Get Team that win the least in league - calling leagueProvider/parse_league_from_db | league: {_league}')
        parsed_league = parse_league_from_db(_league)
        logger.debug(
            f'Server/Get Team that win the least in league - leagueProvider/parse_league_from_db succeeded | parsed league: {parsed_league}')

        logger.debug(
            f'Server/Get Team that win the least in league - calling MongoDbService/find_teams_from_league | league: {parsed_league}')
        teams = db.find_teams_from_league(parsed_league)
        logger.debug(
            f'Server/Get Team that win the least in league - MongoDbService/find_teams_from_league succeeded | parsed league: {parsed_league}')

        logger.debug(
            f'Server/Get Team that win the least in league - calling teamProvider/find_team_least_wins | teams: {teams}')
        team_win_least = find_team_least_wins(teams)
        logger.debug(
            f'Server/Get Team that win the least in league - teamProvider/find_team_least_wins succeeded | team win most: {team_win_least}')

    except ValidationError as error:
        logger.error(f'Server/Get Team that win the least in league failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Get Team that win the least in league failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Team that win the least in league succeeded - id: {parsed_league}')
        return rjson({
            'status': "success",
            'message': f'The team that win the least in {parsed_request["name"]}, Amount of wins: {team_win_least["number_of_wins"]}',
            'team name': str(team_win_least['name'])
        }, status=200)

    finally:
        logger.info(f'Server/Get Team that win the least in league - end')


"""
Team Routes
"""


@app.post('/team')
async def post_handler_team(request):
    """
    Create a new Team
    :param request:
        name : String - the team name
        season : Number - the season year
    :return
    request example
        {
            "name": Real Madrid
            "season": 2020
        }
    """
    logger.info(f'Server/Create Team - start | request: {request.json}')
    try:
        logger.debug(f'Server/Create Team - calling validate_schema | request: {request.json}, schema: {TeamSchema}')
        validate_schema(instance=request.json, schema=TeamSchema)
        logger.debug('Server/Create Team - input validation succeeded')

        logger.debug(
            f'Server/Create Team - calling teamProvider/parse_team_from_request | request: {request.json}, schema: {TeamSchema}')
        parsed_request = parse_team_from_request(request.json)
        logger.debug(
            f'Server/Create League - teamProvider/parse_team_from_request succeeded | parsed request: {parsed_request}')

        logger.debug(f'Server/Create Team - calling MongoDbService/create_team | request: {parsed_request}')
        _id = db.create_team(parsed_request)
        logger.debug(f'Server/Create Team - MongoDbService/create_team succeeded | team id : {_id}')

    except ValidationError as error:
        logger.error(f'Server/Create Team failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Create Team failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Create Team succeeded - id: {_id}')
        return rjson({
            'status': "success",
            'message': 'the team added',
            'id': str(_id)
        }, status=200)

    finally:
        logger.info(f'Server/Create Team - end')


@app.get('/team/<name:string>/<season:number>')
async def get_handler_team_by_name_season(request, name, season):
    """
    Get a Team by name & season
    :param
        name : String - the team name
        season : Number - the season year
    :return
    response example
        {
            "name": Spanish
            "season": 2020,
            "teams": ["real madrid", "hapoel jerusalem"],
            "matches": [match_id_#1, match_id_#2, match_id_#3]
        }
    """
    logger.info(f'Server/Get team by name & season - start | name: {name}, season: {season}')
    try:
        parsed_request = {
            "name": name,
            "season": season
        }
        logger.debug(
            f'Server/Get Team by name & season - calling validate_schema | request: {parsed_request}, schema: {TeamSchema}')
        validate_schema(instance=parsed_request, schema=TeamSchema)
        logger.debug('Server/Get Team by name & season - input validation succeeded')

        logger.debug(f'Server/Get Team by name & season - calling MongoDbService/find_teams_from_league | request: {parsed_request}')
        _team = db.find_teams_from_league(parsed_request)
        logger.debug(f'Server/Get Team by name & season - MongoDbService/find_teams_from_league succeeded | team: {_team}')

        logger.debug(f'Server/Get Team by name & season - calling teamProvider/parse_team_from_db | team: {_team}')
        parsed_team = parse_team_from_db(_team)
        logger.debug(f'Server/Get Team by name & season - teamProvider/find_teams_from_league succeeded | team: {parsed_team}')

    except ValidationError as error:
        logger.error(f'Server/Get Team by name & season failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Get Team by name & season failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Team by name & season succeeded - id: {parsed_team}')
        return rjson({
            'status': "success",
            'message': 'success',
            'team': str(parsed_team)
        }, status=200)

    finally:
        logger.info(f'Server/Get Team by name & season - end')


@app.get('/team/<team_id:string>')
async def get_handler_team_by_id(request, team_id):
    """
    Get a team
    :param
        name : String - the team name
        season : Number - the season year
    :return
    request example
        {
            "name": Spanish
            "season": 2020,
            "teams": ["real madrid", "hapoel jerusalem"],
            "matches": [match_id_#1, match_id_#2, match_id_#3]
        }
    """
    logger.info(f'Server/Get Team by id - start | id: {team_id}')
    try:
        parsed_request = {
            "_id": ObjectId(team_id)
        }

        logger.debug(f'Server/Get Team by id - calling MongoDbService/find_teams_from_league | request: {parsed_request}')
        _team = db.find_teams_from_league(parsed_request)
        logger.debug(f'Server/Get Team by id - MongoDbService/find_teams_from_league succeeded | team: {_team}')

        logger.debug(f'Server/Get Team by id - calling teamProvider/parse_team_from_db | team: {_team}')
        parsed_team = parse_team_from_db(_team)
        logger.debug(f'Server/Get Team by id - teamProvider/parse_team_from_db succeeded | parsed team: {parsed_team}')

    except Exception as error:
        logger.error(f'Server/Get Team by id failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Team by id succeeded - team: {parsed_team}')
        return rjson({
            'status': "success",
            'message': 'success',
            'team': str(parsed_team)
        }, status=200)

    finally:
        logger.info(f'Server/Get Team by id - end')


"""
Match Routes
"""


@app.post('/future_match')
async def post_handler_future_match(request):
    """
    Create a new Match
    :param request:
        home_team : String - the home team name
        away_team : String - the away team name
        date : String - the match date in format: YYYY-MM-DD
    :return
    request example
        {
            "home_team": Real Madrid,
            "away_team": Hapoel Jerusalem
            "season": 20/03/2020
        }
    """
    logger.info(f'Server/Create Future Match - start | request: {request.json}')
    try:
        logger.debug(
            f'Server/Create Future Match - calling validate_schema | request: {request.json}, schema: {MatchSchema}')
        validate_schema(instance=request.json, schema=MatchSchema)
        date = request.get("date", None),
        if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError('Date must be in the format: YYYY-MM-DD')
        logger.debug('Server/Create Future Match - input validation succeeded')

        logger.debug(
            f'Server/Create Future Match - calling matchProvider/parse_match_from_request | request: {request.json}, schema: {MatchSchema}')
        parsed_request = parse_match_from_request(request.json)
        logger.debug(
            f'Server/Create Future Match - matchProvider/parse_match_from_request succeeded | parsed request: {parsed_request}')

        logger.debug(f'Server/Create Future Match - calling MongoDbService/create_match | request: {parsed_request}')
        _id = db.create_match(parsed_request)
        logger.debug(f'Server/Create Future Match - MongoDbService/create_match succeeded | match id : {_id}')

    except (ValidationError, ValueError) as error:
        logger.error(f'Server/Create Future Match failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Create Future Match failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Create Future Match succeeded - id: {_id}')
        return rjson({
            'status': "success",
            'message': 'the team added',
            'id': str(_id)
        }, status=200)

    finally:
        logger.info(f'Server/Create Future Match - end')


@app.post('/ended_match')
async def post_handler_match(request):
    """
    Create a new Match
    :param request:
        home_team : String - the home team name
        away_team : String - the away team name
        score : String - the match score
        date : String - the match date in format: YYYY-MM-DD
    :return
    request example
        {
        }
    """
    logger.info(f'Server/Create Ended Match - start | request: {request.json}')
    try:
        logger.debug(
            f'Server/Create Ended Match - calling validate_schema | request: {request.json}, schema: {MatchSchema}')
        validate_schema(instance=request.json, schema=MatchSchema)
        date = request.json.get("date", None)
        if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError('Date must be in the format: YYYY-MM-DD')
        score = request.json.get("score", None).replace(' ', '')
        is_valid_score = regex_match("(0|[1-9]\d*)-(0|[1-9]\d*)", score)
        if not is_valid_score:
            raise ValueError('Score must be in the format: Number-Number')
        logger.debug('Server/Create Ended Match - input validation succeeded')

        logger.debug(
            f'Server/Create Ended Match - calling matchProvider/parse_match_from_request | request: {request.json}, schema: {MatchSchema}')
        parsed_request = parse_ended_match_from_request(request.json)
        logger.debug(
            f'Server/Create Ended Match - matchProvider/parse_match_from_request succeeded | parsed request: {parsed_request}')

        logger.debug(
            f'Server/Create Ended Match - calling MongoDbService/create_match_with_score | request: {parsed_request}')
        _id = db.create_match_with_score(parsed_request)
        logger.debug(f'Server/Create Ended Match - MongoDbService/create_match_with_score succeeded | match id : {_id}')

    except (ValidationError, ValueError) as error:
        logger.error(f'Server/Create Ended Match failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Create Ended Match failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Create Ended Match succeeded - id: {_id}')
        return rjson({
            'status': "success",
            'message': 'the match added',
            'id': str(_id)
        }, status=200)

    finally:
        logger.info(f'Server/Create Ended Match - end')


@app.get('/match/<home_team:string>/<away_team:string>/<date:string>')
async def get_handler_match_by_name_season(request, home_team, away_team, date):
    """
    Get a Team by name & season
    :param
        home_team : String - the home team name
        away_team : String - the away team name
        date : String - the match date in format: YYYY-MM-DD
    :return
    response example
        {
            "name": Spanish
            "season": 2020,
            "teams": ["real madrid", "hapoel jerusalem"],
            "matches": [match_id_#1, match_id_#2, match_id_#3]
        }
    """
    logger.info(
        f'Server/Get Match by home_team, away_team & date - start | home_team: {home_team}, away_team: {away_team}, date: {date}')
    try:
        parsed_request = {
            "home_team": home_team,
            "away_team": away_team,
            "date": date
        }
        logger.debug(
            f'Server/Get Match by home_team, away_team & date - calling validate_schema | request: {parsed_request}, schema: {MatchSchema}')
        validate_schema(instance=parsed_request, schema=MatchSchema)
        date = request.get("date", None),
        if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError('Date must be in the format: YYYY-MM-DD')
        logger.debug('Server/Get Match by home_team, away_team & date - input validation succeeded')

        logger.debug(
            f'Server/Get Match by home_team, away_team & date - calling MongoDbService/find_match | request: {parsed_request}')
        _match = db.find_match(parsed_request)
        logger.debug(
            f'Server/Get Match by home_team, away_team & date - MongoDbService/find_match succeeded | match: {_match}')

        logger.debug(
            f'Server/Get Match by home_team, away_team & date - calling matchProvider/parse_match_from_db | match: {_match}')
        parsed_match = parse_match_from_db(_match)
        logger.debug(
            f'Server/Get Match by home_team, away_team & date - matchProvider/parse_match_from_db succeeded | parsed_match: {parsed_match}')

    except ValidationError as error:
        logger.error(f'Server/Get Match by home_team, away_team & date failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Get Match by home_team, away_team & date failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Match by home_team, away_team & date succeeded - match: {parsed_match}')
        return rjson({
            'status': "success",
            'message': 'success',
            'team': str(parsed_match)
        }, status=200)

    finally:
        logger.info(f'Server/Get Match by home_team, away_team & date - end')


@app.get('/match/<match_id:string>')
async def get_handler_team_by_id(request, match_id):
    """
    Get a team
    :param
        name : String - the team name
        season : Number - the season year
    :return
    request example
        {
            "name": Spanish
            "season": 2020,
            "teams": ["real madrid", "hapoel jerusalem"],
            "matches": [match_id_#1, match_id_#2, match_id_#3]
        }
    """
    logger.info(f'Server/Get Match by id - start | id: {match_id}')
    try:
        parsed_request = {
            "_id": ObjectId(match_id)
        }

        logger.debug(f'Server/Get Match by id - calling MongoDbService/find_match | request: {parsed_request}')
        _match = db.find_match(parsed_request)
        logger.debug(f'Server/Get Match by id - MongoDbService/find_match succeeded | match: {_match}')

        logger.debug(f'Server/Get Match by id - calling matchProvider/parse_league_from_db | match: {_match}')
        parsed_match = parse_match_from_db(_match)
        logger.debug(f'Server/Get Match by id - matchProvider/parse_league_from_db succeeded | match: {parsed_match}')

    except Exception as error:
        logger.error(f'Server/Get Match by id failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Match by id succeeded - match: {parsed_match}')
        return rjson({
            'status': "success",
            'message': 'success',
            'team': str(parsed_match)
        }, status=200)

    finally:
        logger.info(f'Server/Get Match by id - end')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
