"""This class ingests all game and game dates for a given season."""
from datetime import date, datetime, timezone

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .season_schedule_page_parser import SeasonSchedulePageParser

from fantalytix_sqlalchemy.orm.common.league import League
from fantalytix_sqlalchemy.orm.common.season import Season
from fantalytix_sqlalchemy.orm.common.team import Team
from fantalytix_sqlalchemy.orm.nba.nba_game import NBAGame

class NBASeasonScheduleIngestor:

    EMPTY_STR = ''
    STATUS_COMPLETED = 'completed'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_IN_PROGRESS = 'in_progress'

    def __init__(self):
        self.signature = self.__repr__()
        self.league_cache = dict()
        self.season_cache = dict()
        self.team_cache = dict()
        self.nba_game_cache = dict()

    def get_league_by_abbreviation(self, abbreviation, session):
        """Gets the league object from the cache if available. If the 
        object has not yet been retrieved, or if the object is no longer 
        associated with the session, refresh with a new query.
        """
        league = self.league_cache.get(abbreviation)
        if league is None or league not in session:
            league = session.query(League)\
                .filter_by(abbreviation=abbreviation)\
                .one()
            self.league_cache[abbreviation] = league
        return league

    def get_season(self, end_year, abbreviation, session):
        """Gets the season object from the cache if available. If the 
        object has not yet been retrieved, or if the object is no longer 
        associated with the session, refresh with a new query.
        """
        league = self.get_league_by_abbreviation(abbreviation, session)
        season = self.season_cache.get((end_year, league))
        if season is None or season not in session:
            season = session.query(Season).filter_by(
                end_year=end_year,
                league_id=league.id
                ).one()
            self.season_cache[(end_year, league)] = season
        return season

    def get_team_by_abbreviation(self, abbreviation, session):
        """Gets the team object from the cache if available. If the 
        object has not yet been retrieved, or if the object is no longer 
        associated with the session, refresh with a new query.
        """
        team = self.team_cache.get(abbreviation)
        if team is None or team not in session:
            team = session.query(Team)\
                .filter_by(abbreviation=abbreviation)\
                .one()
            self.team_cache[abbreviation] = team
        return team

    def get_team_by_name(self, name, session):
        """Gets the team object from the cache if available. If the 
        object has not yet been retrieved, or if the object is no longer 
        associated with the session, refresh with a new query.
        """
        name = name.lower()
        team = self.team_cache.get(name)
        if team is None or team not in session:
            team = session.query(Team)\
                .filter_by(name=name)\
                .one()
            self.team_cache[name] = team
        return team

    def get_status(self, game_date):
        if game_date > datetime.now():
            return self.STATUS_SCHEDULED
        return self.STATUS_COMPLETED

    def overtime_to_int(self, text):
        if text is None or self.EMPTY_STR:
            return 0
        return 1

    def map_to_nba_game(self, row, session, season):
        home_team = self.get_team_by_name(row['home_team_name'], session)
        away_team = self.get_team_by_name(row['visitor_team_name'], session)
        game_date = datetime.combine(row['game_date'], row['game_start_time'])
        if row['home_pts'] > row['visitor_pts']:
            winning_team = home_team
        else:
            winning_team = away_team
        return NBAGame(
            season_id=season.id,
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            game_date=game_date,
            home_score=row['home_pts'],
            away_score=row['visitor_pts'],
            overtimes=self.overtime_to_int(row['overtimes']),
            winning_team_id=winning_team.id,
            status=self.get_status(game_date),
            type=row['type']
        )

    def update_nba_game(self, row, session, nba_game):
        """Updates the nba_game object if its information is different from the 
        nba_game row.
        """
        if nba_game.home_score != row['home_pts']:
            nba_game.home_score = row['home_pts']
            updated = True
        if nba_game.away_score != row['visitor_pts']:
            nba_game.away_score = row['visitor_pts']
            updated = True
        if nba_game.overtimes != self.overtime_to_int(row['overtimes']):
            nba_game.overtimes = self.overtime_to_int(row['overtimes'])
            updated = True
        if row['home_pts'] > row['visitor_pts']:
            winning_team = nba_game.home_team
        else:
            winning_team = nba_game.away_team
        if updated:
            nba_game.winning_team_id = winning_team_id
            nba_game.last_updated_by = self.signature
            nba_game.last_updated_date = datetime.now(tz=timezone.utc)
        return nba_game

    def get_nba_game_query(self, row, session, season):
        game_date = datetime.combine(row['game_date'], row['game_start_time'])
        home_team = self.get_team_by_name(row['home_team_name'], session)
        away_team = self.get_team_by_name(row['visitor_team_name'], session)
        return session.query(NBAGame).filter_by(
            season_id=season.id,
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            game_date=game_date)

    def get_nba_game_or_none(self, row, session, season):
        return self.get_nba_game_query(row, session, season).one_or_none()

    def ingest_all(self, html, session, season_end_year, 
        league_abbreviation='NBA'):
        """This method iterates through each scheduled game row starting from 
        the top of the page, adds new games and updates existing games.
        """
        parser = SeasonSchedulePageParser(html)
        for row in parser.get_data():
            season = self.get_season(
                season_end_year, 
                league_abbreviation, 
                session)
            nba_game = self.get_nba_game_or_none(row, session, season)
            if nba_game is None:
                session.add(self.map_to_nba_game(row, session, season))
            else:
                self.update_nba_game(row, session, nba_game)

    def __repr__(self):
        return "<NBASeasonScheduleIngestor(object)>"
