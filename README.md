# Football-Management-Tool

## Description
The football association required you to build a software solution for managing its games scores.

## Requirements
1. Python 3.7.X
2. PyMongo

## How to run
1. In the project directory, run: `pip3 install -r requirement.txt`
2. Connect MongoDB at url: `localhost`, port `27017`
2. Add Data To The DB `python3 add_data_to_db.py`
2. Classification Engine Command `python3 runner.py`

## Routes
#### Leagues
1. Create League - ```POST /league```, body: `{ "name" : "Israel", "season": 2020 }`
2. Get League by name & season - ```Get /league/<name:string>/<season:number>```
3. Get League by id - ```Get /league/<league_id:string>```
4. Add Team to League - ```POST /league/add_team```, body: `{ "league_id" : league_id, "team_id": team_id }`
5. Get Team that scored the most goals - ```Get /league/most_goals/<name:string>/<season:number>```
6. Get Team that scored the least goals - ```Get /league/least_goals/<name:string>/<season:number>```
7. Get Team that has the most wins - ```Get /league/most_wins/<name:string>/<season:number>```
8. Get Team that has the most wins - ```Get /league/least_wins/<name:string>/<season:number>```

#### Teams
1. Create Team - ```POST /team```, body: `{ "name" : "hapoel jerusalem", "season": 2020 }`
2. Get Team by name & season - ```Get /team/<name:string>/<season:number>```
3. Get Team by id - ```Get /team/<league_id:string>```

#### Matches
1. Create Future Match - ```POST /future_match```, body: `{ "home_team" : "hapoel jerusalem", "away_team" : "real madrid", "date": "2020-03-20" }`
2. Create Ended Match - ```POST /ended_match```, body: `{ "home_team" : "hapoel jerusalem", "away_team" : "real madrid", "score": "7-1", "date": "2020-03-20" }`
3. Get Match by name & season - ```Get /team/<name:string>/<season:number>```
4. Get Match by id - ```Get /team/<league_id:string>```

