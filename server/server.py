#!/usr/bin/python3

from sanic import Sanic
from sanic.response import json as rjson
from bson import ObjectId
from jsonschema import validate as validate_schema, ValidationError
from datetime import datetime

from services.configServices.configService import ConfigService
from services.loggerServices.loggerService import LoggerService
from services.mongoDbService.leagueProvider import (parse_league_from_request, parse_league_from_db)
from services.mongoDbService.teamProvider import (parse_team_from_request, parse_team_from_db)
from services.mongoDbService.matchProvider import (parse_match_from_db, parse_match_from_request)
from services.mongoDbService.mongoDbService import MongoDbService
from models.models import (LeagueSchema, TeamSchema, MatchSchema)

config = ConfigService()
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
            f'Server/Get League by name & season - calling MongoDbService/get_league | request: {parsed_request}')
        _league = db.get_league(parsed_request)
        logger.debug(f'Server/Get League by name & season - MongoDbService/get_league succeeded | league: {_league}')

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

        logger.debug(f'Server/Get League by id - calling MongoDbService/get_league | request: {parsed_request}')
        _league = db.get_league(parsed_request)
        logger.debug(f'Server/Get League by id - MongoDbService/get_league succeeded | league: {_league}')

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

        logger.debug(f'Server/Get Team by name & season - calling MongoDbService/get_team | request: {parsed_request}')
        _team = db.get_team(parsed_request)
        logger.debug(f'Server/Get Team by name & season - MongoDbService/get_team succeeded | team: {_team}')

        logger.debug(f'Server/Get Team by name & season - calling teamProvider/parse_team_from_db | team: {_team}')
        parsed_team = parse_team_from_db(_team)
        logger.debug(f'Server/Get Team by name & season - teamProvider/get_team succeeded | team: {parsed_team}')

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

        logger.debug(f'Server/Get Team by id - calling MongoDbService/get_team | request: {parsed_request}')
        _team = db.get_team(parsed_request)
        logger.debug(f'Server/Get Team by id - MongoDbService/get_team succeeded | team: {_team}')

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


@app.post('/match')
async def post_handler_match(request):
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
    logger.info(f'Server/Create Match - start | request: {request.json}')
    try:
        logger.debug(f'Server/Create Match - calling validate_schema | request: {request.json}, schema: {MatchSchema}')
        validate_schema(instance=request.json, schema=MatchSchema)
        date = request.get("date", None),
        if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError('Date must be in the format: YYYY-MM-DD')
        logger.debug('Server/Create Match - input validation succeeded')

        logger.debug(
            f'Server/Create Match - calling matchProvider/parse_match_from_request | request: {request.json}, schema: {MatchSchema}')
        parsed_request = parse_match_from_request(request.json)
        logger.debug(
            f'Server/Create Match - matchProvider/parse_match_from_request succeeded | parsed request: {parsed_request}')

        logger.debug(f'Server/Create Match - calling MongoDbService/create_match | request: {parsed_request}')
        _id = db.create_team(parsed_request)
        logger.debug(f'Server/Create Match - MongoDbService/create_match succeeded | match id : {_id}')

    except (ValidationError, ValueError) as error:
        logger.error(f'Server/Create Match failed - validation error | error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error.message)
            }, status=400)

    except Exception as error:
        logger.error(f'Server/Create Match failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Create Match succeeded - id: {_id}')
        return rjson({
            'status': "success",
            'message': 'the team added',
            'id': str(_id)
        }, status=200)

    finally:
        logger.info(f'Server/Create Match - end')


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
    logger.info(f'Server/Get Match by home_team, away_team & date - start | home_team: {home_team}, away_team: {away_team}, date: {date}')
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
            f'Server/Get Match by home_team, away_team & date - calling MongoDbService/get_match | request: {parsed_request}')
        _match = db.get_match(parsed_request)
        logger.debug(f'Server/Get Match by home_team, away_team & date - MongoDbService/get_match succeeded | match: {_match}')

        logger.debug(f'Server/Get Match by home_team, away_team & date - calling matchProvider/parse_match_from_db | match: {_match}')
        parsed_match = parse_match_from_db(_match)
        logger.debug(f'Server/Get Match by home_team, away_team & date - matchProvider/parse_match_from_db succeeded | parsed_match: {parsed_match}')

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

        logger.debug(f'Server/Get Match by id - calling MongoDbService/get_match | request: {parsed_request}')
        _match = db.get_match(parsed_request)
        logger.debug(f'Server/Get Match by id - MongoDbService/get_match succeeded | match: {_match}')

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
