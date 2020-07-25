#!/usr/bin/python3

import pymongo
from pymongo.errors import DuplicateKeyError

from services.configServices.configService import ConfigService
from services.loggerServices.loggerService import LoggerService
from services.mongoDbService.collectionProvider import create_collections
from services.mongoDbService.leagueProvider import (create_league, find_league, add_team_to_league)
from services.mongoDbService.teamProvider import (create_team, find_team, update_team_with_draw,
                                                  update_winning_team, update_losing_team, init_team,
                                                  parse_team_from_db)
from services.mongoDbService.matchProvider import (create_match, find_match, parse_ended_match_to_db, )

config = ConfigService().config
logger = LoggerService().logger


class MongoDbService:
    def __init__(self):
        logger.info(f'MongoDbService/init - start')
        self.client = pymongo.MongoClient(config['mongodb']['url'], config['mongodb']['port'])
        logger.debug(f'MongoDbService/init - calling collectionProvider/create_collections')
        create_collections(self)
        logger.info(f'MongoDbService/init - end')

    def create_league(self, data):
        logger.info(f'MongoDbService/create_league - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/create_league - calling leagueProvider/create_league')
            _id = create_league(self, data)
            logger.debug(f'MongoDbService/create_league - leagueProvider/create_league succeeded | id: {_id}')

        # League already exists
        except DuplicateKeyError as error:
            logger.error(f'MongoDbService/create_league failed - duplicate key error | error: {error}')
            raise Exception('League is already exists - name and season combination must be unique')

        except Exception as error:
            logger.error(f'MongoDbService/create_league failed | error: {error}')
            raise

        else:
            return _id

    def find_league(self, data):
        logger.info(f'MongoDbService/find_league - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/find_league - calling leagueProvider/find_league')
            _league = find_league(self, data)
            logger.debug(f'MongoDbService/find_league - leagueProvider/find_league succeeded | league: {_league}')

            if _league is None:
                raise Exception('The league is not exists')

        except Exception as error:
            logger.error(f'MongoDbService/find_league failed | error: {error}')
            raise

        else:
            return _league

    def add_team_to_league(self, parsed_request):
        logger.info(f'MongoDbService/add_team_to_league - start | parsed_request: {parsed_request}')
        try:
            league_id = parsed_request.get('league_id')
            team_id = parsed_request.get('team_id')
            logger.debug(
                f'MongoDbService/add_team_to_league - calling leagueProvider/add_team_to_league | league_id: {league_id}, team_id:{team_id}')
            _league = add_team_to_league(self, league_id, team_id)
            logger.debug(
                f'MongoDbService/add_team_to_league - leagueProvider/add_team_to_league succeeded | league: {_league}')

            if _league is None:
                raise Exception('The league is not exists')

        except Exception as error:
            logger.error(f'MongoDbService/add_team_to_league failed | error: {error}')
            raise

        else:
            return _league

    def create_team(self, data):
        logger.info(f'MongoDbService/create_team - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/create_team - calling teamProvider/create_team')
            _id = create_team(self, init_team(data))
            logger.debug(f'MongoDbService/create_team - teamProvider/create_team succeeded | id: {_id}')

        # Team already exists
        except DuplicateKeyError as error:
            logger.error(f'MongoDbService/create_team failed - duplicate key error | error: {error}')
            raise Exception('Team is already exists - name and season combination must be unique')

        except Exception as error:
            logger.error(f'MongoDbService/create_team failed | error: {error}')
            raise

        else:
            return _id

    def find_team(self, data):
        logger.info(f'MongoDbService/find_team - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/find_team - calling teamProvider/find_team')
            _team = find_team(self, data)
            logger.debug(f'MongoDbService/find_team - teamProvider/find_team succeeded | team: {_team}')

            if _team is None:
                raise Exception('The team is not exists')

        except Exception as error:
            logger.error(f'MongoDbService/find_team failed | error: {error}')
            raise

        else:
            return _team

    def create_match(self, data):
        logger.info(f'MongoDbService/create_match - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/create_match - calling matchProvider/create_match')
            _id = create_match(self, data)
            logger.debug(f'MongoDbService/create_match - matchProvider/create_match succeeded | id: {_id}')

        # Match already exists
        except DuplicateKeyError as error:
            logger.error(f'MongoDbService/create_match failed - duplicate key error | error: {error}')
            raise Exception('Match is already exists - home team, away team and date combination must be unique')

        except Exception as error:
            logger.error(f'MongoDbService/create_match failed | error: {error}')
            raise

        else:
            return _id

    def create_match_with_score(self, data):
        logger.info(f'MongoDbService/create_match_with_score - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/create_match_with_score - calling matchProvider/parse_ended_match_to_db')
            parsed_match = parse_ended_match_to_db(data)
            logger.debug(
                f'MongoDbService/create_match_with_score - matchProvider/parse_ended_match_to_db succeeded | match: {parsed_match}')

            logger.debug(f'MongoDbService/create_match_with_score - calling matchProvider/create_match')
            _id = create_match(self, parsed_match)
            logger.debug(f'MongoDbService/create_match_with_score - matchProvider/create_match succeeded | id: {_id}')

            logger.debug(f'MongoDbService/create_match_with_score - calling update_teams_with_match_result')
            self.update_teams_with_match_result(parsed_match, _id)
            logger.debug(f'MongoDbService/create_match_with_score - matchProvider/create_match succeeded')

        # Match already exists
        except DuplicateKeyError as error:
            logger.error(f'MongoDbService/create_match_with_score failed - duplicate key error | error: {error}')
            raise Exception('Match is already exists - home team, away team and date combination must be unique')

        except Exception as error:
            logger.error(f'MongoDbService/create_match_with_score failed | error: {error}')
            raise

        else:
            return _id

    def update_teams_with_match_result(self, data, match_id):
        global team_won_data, team_lost_data
        logger.info(f'MongoDbService/update_teams_with_match_result - start | data: {data}, match id = {match_id}')
        try:
            home_team_name = data.get("home_team")
            away_team_name = data.get("away_team")
            season = data.get("date").split('-')[0]
            home_team_data = {
                "name": home_team_name,
                "season": season
            }
            away_team_data = {
                "name": away_team_name,
                "season": season
            }

            if not find_team(self, home_team_data):
                create_team(self, init_team(home_team_data))

            if not find_team(self, away_team_data):
                create_team(self, init_team(away_team_data))

            if data['is_draw']:
                logger.debug(
                    f'MongoDbService/update_teams_with_match_result - calling teamProvider/update_team_with_draw | home team: {home_team_data}, away team: {away_team_data}')
                update_team_with_draw(self, home_team_data, data["team_won_score"], match_id)
                update_team_with_draw(self, away_team_data, data["team_won_score"], match_id)
                logger.debug(
                    f'MongoDbService/update_teams_with_match_result - teamProvider/update_team_with_draw succeeded')
                return True

            elif data['team_won'] == home_team_name:
                team_won_data = home_team_data
                team_lost_data = away_team_data
            else:
                team_won_data = away_team_data
                team_lost_data = home_team_data

            logger.debug(
                f'MongoDbService/update_teams_with_match_result - calling teamProvider/update_winning_team | winnig team: {team_won_data}')
            update_winning_team(self, team_won_data, data["team_won_score"], data["team_lose_score"], match_id)
            logger.debug(f'MongoDbService/update_teams_with_match_result - teamProvider/update_winning_team succeeded')

            logger.debug(
                f'MongoDbService/update_teams_with_match_result - calling teamProvider/update_losing_team | lossing team: {team_lost_data}')
            update_losing_team(self, team_lost_data, data["team_lose_score"], data["team_won_score"], match_id)
            logger.debug(f'MongoDbService/update_teams_with_match_result - teamProvider/update_losing_team succeeded')

        except Exception as error:
            logger.error(f'MongoDbService/update_teams_with_match_result failed | error: {error}')
            raise

    def find_match(self, data):
        logger.info(f'MongoDbService/find_match - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/find_match - calling matchProvider/find_match')
            _match = find_match(self, data)
            logger.debug(f'MongoDbService/find_match - matchProvider/find_match succeeded | _match: {_match}')

            if _match is None:
                raise Exception('The match is not exists')

        except Exception as error:
            logger.error(f'MongoDbService/find_match failed | error: {error}')
            raise

        else:
            return _match

    def add_match_to_team(self, data):
        logger.info(f'MongoDbService/add_match_to_team - start | data: {data}')
        try:
            logger.debug(f'MongoDbService/add_match_to_team - calling matchProvider/find_team')
            _team = find_team(self, data)
            logger.debug(
                f'MongoDbService/add_match_to_team - matchProvider/find_team succeeded | team: {_team}')

            if _team is None:
                raise Exception('The team is not exists')

        except Exception as error:
            logger.error(f'MongoDbService/add_match_to_team failed | error: {error}')
            raise

        else:
            return _team

    def find_teams_from_league(self, data):
        logger.info(f'MongoDbService/find_teams_from_league - start | data: {data}')
        try:
            teams = []
            for team in data['teams']:
                logger.debug(f'MongoDbService/find_teams_from_league - calling matchProvider/find_team')
                _team = find_team(self, team)
                logger.debug(
                    f'MongoDbService/find_teams_from_league - matchProvider/find_team succeeded | team: {_team}')

                if _team is None:
                    raise Exception('The team is not exists')

                teams.append(parse_team_from_db(_team))

        except Exception as error:
            logger.error(f'MongoDbService/find_teams_from_league failed | error: {error}')
            raise

        else:
            return teams
