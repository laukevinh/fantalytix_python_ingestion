"""This is a test for the NBASeasonScheduleIngestor. """
import unittest
from datetime import date, datetime, timezone
from urllib.request import urlopen
from urllib.parse import urljoin

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, SEASON_SUMMARY_URL, SEASON_SCHEDULE_URL)

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .season_summary_page_parser import SeasonSummaryPageParser

from fantalytix_python_ingestion.ingestion.sports_reference.basketball\
    .nba_season_schedule_ingestor import NBASeasonScheduleIngestor

from fantalytix_sqlalchemy.orm.common.league import League
from fantalytix_sqlalchemy.orm.common.season import Season
from fantalytix_sqlalchemy.orm.common.team import Team
from fantalytix_sqlalchemy.orm.nba.nba_game import NBAGame
from fantalytix_sqlalchemy.test.settings import CONNECTION

class TestNBASeasonScheduleIngestor(unittest.TestCase):

    def setUp(self):
        """Set up league, season, and all teams since each season schedule 
        page will have all of these components. Teams are extracted using 
        the SeasonSummaryPageParser for convenience.
        """
        self.engine = create_engine(CONNECTION)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        with urlopen(urljoin(BASE_URL, SEASON_SCHEDULE_URL.format(
            league='NBA', end_year='2019', month='october'))) as resp:
            self.page = resp.read().decode('utf-8')

        league = League(
            name='National Basketball Association',
            abbreviation='NBA',
            sport='basketball',
            created_by='pycrawl',
            creation_date=datetime.now(tz=timezone.utc),
            last_updated_by=None,
            last_updated_date=None
        )
        self.session.add(league)
        self.session.commit()

        self.session.add(Season(
            league_id=league.id,
            start_date=date(2018, 10, 16),
            end_date=date(2019, 4, 10),
            start_year=date(2018, 1, 1),
            end_year=date(2019, 1, 1),
            created_by='pycrawl',
            creation_date=datetime.now(tz=timezone.utc),
            last_updated_by=None,
            last_updated_date=None)
        )
        self.session.commit()

        with urlopen(urljoin(BASE_URL, SEASON_SUMMARY_URL.format(
            league='NBA', end_year='2019'))) as resp:
            season_summary_page = resp.read().decode('utf-8')
        parser = SeasonSummaryPageParser(season_summary_page)
        for team in parser.get_data():
            self.session.add(Team(
                name=team['team_name'],
                abbreviation=team['abbreviation'],
                status='active')
            )
        self.session.commit()

    def tearDown(self):
        self.session.query(League).delete()
        self.session.query(Season).delete()
        self.session.query(Team).delete()
        self.session.query(NBAGame).delete()
        self.session.commit()
        self.session.close()

    def test_ingest_all(self):
        ingestor = NBASeasonScheduleIngestor()

        try:
            ingestor.ingest_all(self.page, self.session, date(2019, 1, 1))
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        self.assertEqual(self.session.query(NBAGame).count(), 110)

        gsw = self.session.query(Team).filter_by(abbreviation="GSW").one()
        nop = self.session.query(Team).filter_by(abbreviation="NOP").one()

        nbagame = self.session.query(NBAGame).filter_by(
            game_date=datetime(2018, 10, 31, 22, 30),
            home_team_id=gsw.id
            ).one()
        self.assertEqual(nbagame.away_team_id, nop.id)
        self.assertEqual(nbagame.home_score, 131)
        self.assertEqual(nbagame.away_score, 121)

if __name__ == '__main__':
    unittest.main()
