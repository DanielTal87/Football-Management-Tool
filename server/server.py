#!/usr/bin/python3

from bson import ObjectId
from jsonschema import validate, ValidationError

from services.configServices.configService import ConfigService
from models.models import (LeagueSchema, TeamSchema, MatchSchema)
from sanic import Sanic
from sanic.response import json as rjson

from services.loggerServices.loggerService import LoggerService
from services.mongoDbService.leagueProvider import (parse_league_from_request, parse_league_from_db)
from services.mongoDbService.teamProvider import (parse_team_from_request, parse_team_from_db)
from services.mongoDbService.mongoDbService import MongoDbService

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
        logger.debug(f'Server/Create League - calling validate | request: {request.json}, schema: {LeagueSchema}')
        validate(instance=request.json, schema=LeagueSchema)
        logger.debug('Server/Create League - input validation succeeded')

        logger.debug(
            f'Server/Create League - calling leagueProvider/parse_league_from_request | request: {request.json}, schema: {LeagueSchema}')
        parsed_request = parse_league_from_request(request.json)
        logger.debug(f'Server/Create League - parse_league_from_request succeeded | parsed request: {parsed_request}')

        logger.debug(f'Server/Create League - calling MongoDbService/create_league | request: {parsed_request}')
        _id = db.create_league(parsed_request)
        logger.debug(f'Server/Create League - create_league succeeded | league id: {_id}')

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
            f'Server/Get League by name & season - calling validate | request: {parsed_request}, schema: {LeagueSchema}')
        validate(instance=parsed_request, schema=LeagueSchema)
        logger.debug('Server/Get League by name & season - input validation succeeded')

        logger.debug(
            f'Server/Get League by name & season - calling MongoDbService/get_league | request: {parsed_request}')
        _league = db.get_league(parsed_request)
        parsed_league = parse_league_from_db(_league)
        logger.debug(f'Server/Get League by name & season - get_league succeeded | league: {parsed_league}')

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

        logger.debug(
            f'Server/Get League by id - calling MongoDbService/get_league | request: {parsed_request}')
        _league = db.get_league(parsed_request)
        parsed_league = parse_league_from_db(_league)
        logger.debug(f'Server/Get League by id - get_league succeeded | league: {parsed_league}')

    except Exception as error:
        logger.error(f'Server/Get League by id failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get League by id succeeded - id: {parsed_league}')
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
        logger.debug(f'Server/Create Team - calling validate | request: {request.json}, schema: {TeamSchema}')
        validate(instance=request.json, schema=TeamSchema)
        logger.debug('Server/Create Team - input validation succeeded')

        logger.debug(
            f'Server/Create Team - calling teamProvider/parse_team_from_request | request: {request.json}, schema: {TeamSchema}')
        parsed_request = parse_team_from_request(request.json)
        logger.debug(f'Server/Create Team - parse_team_from_request succeeded | parsed request: {parsed_request}')

        logger.debug(f'Server/Create Team - calling MongoDbService/create_team | request: {parsed_request}')
        _id = db.create_team(parsed_request)
        logger.debug(f'Server/Create Team - create_team succeeded | team id : {_id}')

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
            f'Server/Get Team by name & season - calling validate | request: {parsed_request}, schema: {TeamSchema}')
        validate(instance=parsed_request, schema=TeamSchema)
        logger.debug('Server/Get Team by name & season - input validation succeeded')

        logger.debug(
            f'Server/Get Team by name & season - calling MongoDbService/get_team | request: {parsed_request}')
        _team = db.get_team(parsed_request)
        parsed_team = parse_team_from_db(_team)
        logger.debug(f'Server/Get Team by name & season - get_team succeeded | team: {parsed_team}')

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

        logger.debug(
            f'Server/Get Team by id - calling MongoDbService/get_team | request: {parsed_request}')
        _team = db.get_team(parsed_request)
        parsed_team = parse_team_from_db(_team)
        logger.debug(f'Server/Get Team by id - get_team succeeded | team: {parsed_team}')

    except Exception as error:
        logger.error(f'Server/Get Team by id failed - error: {error}')
        return rjson(
            {
                'status': 'Error',
                'message': str(error)
            }, status=400)

    else:
        logger.info(f'Server/Get Team by id succeeded - id: {parsed_team}')
        return rjson({
            'status': "success",
            'message': 'success',
            'team': str(parsed_team)
        }, status=200)

    finally:
        logger.info(f'Server/Get Team by id - end')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
