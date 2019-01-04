"""This class uses the fantalytix_python_crawler package to parse and 
SQLAlchemy package to preserve the data. The fantalytix_sqlalchemy package
contains the models.
"""
from datetime import date, datetime, timezone

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .leagues_page_parser import LeaguesPageParser

from fantalytix_sqlalchemy.orm.common.league import League
from fantalytix_sqlalchemy.orm.common.season import Season

class NBASeasonsIngestor:

    def __init__(self):
        self.signature = self.__repr__()
        self.league_cache = dict()

    def get_league_by_abbreviation(self, abbreviation, session):
        """Gets the league object from the cache if available. If the 
        league has not yet been retrieved, or if the league is no longer 
        associated with the session, refresh with a new query.
        """
        league = self.league_cache.get(abbreviation)
        if league is None or league not in session:
            league = session.query(League)\
                .filter_by(abbreviation=abbreviation)\
                .one()
            self.league_cache[abbreviation] = league
        return league

    def map_to_season(self, season_row, session):
        league = self.get_league_by_abbreviation(season_row['league'], session)
        return Season(
            league_id=league.id,
            start_date=None,
            end_date=None,
            start_year=season_row['start_year'],
            end_year=season_row['end_year'],
            created_by=self.signature,
            creation_date=datetime.now(tz=timezone.utc),
            last_updated_by=None,
            last_updated_date=None
        )

    def update_season(self, season_row, session, season):
        """Updates the season object if its information is different from the 
        season row. This is done by iterating through each key in season_row, 
        determining if the season object has an attribute with the same name, 
        and updating if they aren't the same. e.g.
        >>> if season.start_year != season_row['start_year']:
        ...    season.start_year = season_row['start_year']
        ...    updated = True
        """
        updated = False
        league = self.get_league_by_abbreviation(season_row['league'], session)
        for key in season_row.keys():
            if key in season.__dict__ and season.__dict__[key] != season_row[key]:
                season.__dict__[key] = season_row[key]
                updated = True
        if updated:
            season.last_updated_by = self.signature
            season.last_updated_date = datetime.now(tz=timezone.utc)
        return season

    def get_season_query(self, season_row, session):
        league = self.get_league_by_abbreviation(season_row['league'], session)
        return session.query(Season).filter_by(
            league_id=league.id,
            start_year=season_row['start_year'])

    def season_exists(self, season_row, session):
        return session.query(self.get_season_query(season_row, session)\
            .exists()).scalar()

    def get_season(self, season_row, session):
        return self.get_season_query(season_row, session).one()

    def get_season_or_none(self, season_row, session):
        return self.get_season_query(season_row, session).one_or_none()

    def ingest_all(self, html, session):
        """This method iterates through each season row starting from the top 
        of the page, adds new seasons and updates existing seasons.
        """
        parser = LeaguesPageParser(html)
        for season_row in parser.get_data():
            season = self.get_season_or_none(season_row, session)
            if season is None:
                session.add(self.map_to_season(season_row, session))
            else:
                self.update_season(season_row, session, season)

    def ingest_one(self, html, session):
        """This method iterates through each season row starting from the top 
        of the page until it finds one that does not exist in the database, 
        then adds it.
        """
        parser = LeaguesPageParser(html)
        for season_row in parser.get_data():
            if not self.season_exists(season_row, session):
                session.add(self.map_to_season(season_row, session))
                break

    def ingest_recent(self, html, session):
        """This method adds each new season row starting from the top of the 
        page until it finds an existing season. It stops ingesting at that 
        point.
        """
        parser = LeaguesPageParser(html)
        for season_row in parser.get_data():
            if not self.season_exists(season_row, session):
                session.add(self.map_to_season(season_row, session))
            else:
                break

    def __repr__(self):
        return "<NBASeasonsIngestor(object)>"
