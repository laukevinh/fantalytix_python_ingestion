"""This class uses the fantalytix_python_crawler package to parse and 
SQLAlchemy package to preserve the data. The fantalytix_sqlalchemy package
contains the models.
"""
from datetime import date, datetime, timezone

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .leagues_page_parser import LeaguesPageParser

from fantalytix_sqlalchemy.orm.common.league import League

class NBALeaguesIngestor:

    def __init__(self):
        self.signature = self.__repr__()
        self.league_cache = dict()
        self.ABBREVIATION_TO_NAME = {
            'NBA': 'National Basketball Association',
            'ABA': 'American Basketball Association',
            'BAA': 'Basketball Association of America'
        }

    def get_name_by_abbreviation(self, abbreviation):
        return self.ABBREVIATION_TO_NAME.get(abbreviation) or abbreviation

    def get_league_by_abbreviation(self, abbreviation, session):
        """Gets the league object from the cache if available. If the 
        league has not yet been retrieved, or if the league is no longer 
        associated with the session, refresh with a new query. This is 
        different from the NBASeasonsIngestor's version of 
        get_league_by_abbreviation. This returns one_or_none while the 
        other returns one.
        """
        league = self.league_cache.get(abbreviation)
        if league is None or league not in session:
            league = session.query(League)\
                .filter_by(abbreviation=abbreviation)\
                .one_or_none()
            self.league_cache[abbreviation] = league
        return league

    def get_league_or_none(self, season_row, session):
        return self.get_league_by_abbreviation(season_row['league'], session)

    def map_to_league(self, season_row, session):
        """Because basketball-reference does not have a page showing the full 
        name of each league, the names are coded here as a temporary fix.
        """
        return League(
            name=self.get_name_by_abbreviation(season_row['league']),
            abbreviation=season_row['league'],
            sport='basketball',
            created_by='pycrawl',
            creation_date=datetime.now(tz=timezone.utc),
            last_updated_by=None,
            last_updated_date=None
        )

    def update_league(self, league):
        """Updates the league object if its information is different from the 
        dictionary. 
        """
        if league.name != self.get_name_by_abbreviation(league.abbreviation):
            league.name = self.get_name_by_abbreviation(league.abbreviation)
            league.last_updated_by = self.signature
            league.last_updated_date = datetime.now(tz=timezone.utc)
        return league

    def ingest_all(self, html, session):
        """This method iterates through each season row starting from the top 
        of the page, adds any new league that does not exist and updates the 
        name of any existing league if it changed. Leagues that no longer 
        exist are not removed.
        """
        parser = LeaguesPageParser(html)
        for season_row in parser.get_data():
            league = self.get_league_or_none(season_row, session)
            if league is None:
                session.add(self.map_to_league(season_row, session))
            else:
                self.update_league(league)

    def __repr__(self):
        return "<NBALeaguesIngestor(object)>"
