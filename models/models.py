LeagueSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "season": {"type": "number"},
        "teams": {"type": "array"},
        "matches": {"type": "array"}
    },
    "required": ["name", "season"]
}

TeamSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "season": {"type": "number"},
        "number_of_wins": {"type": "number"},
        "matches_wins": {"type": "array"},
        "number_of_losses": {"type": "number"},
        "matches_loss": {"type": "array"},
        "number_of_draws": {"type": "number"},
        "matches_draw": {"type": "array"},
        "number_of_scored_goals": {"type": "number"},
        "number_of_received_goals": {"type": "number"}
    },
    "required": ["name", "season"]
}

MatchSchema = {
    "type": "object",
    "properties": {
        "home_team": {"type": "string"},
        "away_team": {"type": "string"},
        "score": {"type": "string"},
        "is_draw": {"type": "boolean"},
        "team_won": {"type": "string"},
        "team_lost": {"type": "string"},
        "date": {"type": "string"}
    },
    "required": ["home_team", "away_team"]
}
