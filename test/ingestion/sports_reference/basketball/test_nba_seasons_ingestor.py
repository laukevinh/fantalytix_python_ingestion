import unittest
from datetime import date, datetime, timezone
from urllib.request import urlopen
from urllib.parse import urljoin

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, LEAGUES_URL)

from fantalytix_python_ingestion.ingestion.sports_reference.basketball\
    .nba_seasons_ingestor import NBASeasonsIngestor

from fantalytix_sqlalchemy.orm.common import League, Season
from ....settings import CONNECTION

class TestNBASeasonsIngestor(unittest.TestCase):
    
    def setUp(self):
        self.engine = create_engine(CONNECTION)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        with urlopen(urljoin(BASE_URL, LEAGUES_URL)) as resp:
            self.page = resp.read().decode('utf-8')

        self.session.add(League(
            name='National Basketball Association',
            abbreviation='NBA',
            sport='basketball',
            created_by='pycrawl')
        )

        self.session.add(League(
            name='American Basketball Association',
            abbreviation='ABA',
            sport='basketball',
            created_by='pycrawl')
        )

        self.session.add(League(
            name='Basketball Association of America',
            abbreviation='BAA',
            sport='basketball',
            created_by='pycrawl')
        )

        self.session.commit()

    def tearDown(self):
        self.session.query(League).delete()
        self.session.query(Season).delete()
        self.session.commit()
        self.session.close()

    def get_current_season_start_year(self):
        if date.today().month > 6:
            return date.today().year
        else:
            return date.today().year - 1

    def test_ingest_all(self):
        """Test ingest_all twice. First, test that ingestion occurs when 
        database is empty. Second, modify one row with incorrect data to 
        test that ingest_all updates with correct data.
        """
        ingestor = NBASeasonsIngestor()

        try:
            ingestor.ingest_all(self.page, self.session)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        self.assertEqual(self.session.query(League).count(), 3)

        count_BAA_seasons = 3
        count_ABA_seasons = 9
        FIRST_NBA_SEASON_YEAR = 1949
        count_NBA_seasons = (self.get_current_season_start_year() 
                            - FIRST_NBA_SEASON_YEAR
                            + 1)
        count_total_seasons = (count_BAA_seasons 
                              + count_ABA_seasons 
                              + count_NBA_seasons)

        self.assertEqual(self.session.query(Season).count(), 
            count_total_seasons)

        season = self.session.query(Season).filter_by(
            start_year=date(2018, 1, 1)
        ).one()
        season.end_year = date(2020, 1, 1)
        self.session.commit()

        try:
            ingestor.ingest_all(self.page, self.session)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        count_updated_rows = self.session.query(Season).filter_by(
            last_updated_by=ingestor.signature).count()
        self.assertEqual(count_updated_rows, 1)

    def test_ingest_one(self):
        league = self.session.query(League).filter_by(
            abbreviation='NBA'
        ).first()
        season = Season(
            league=league,
            start_date=None,
            end_date=None,
            start_year=date(2018, 1, 1),
            end_year=date(2019, 1, 1),
            created_by='pycrawl',
        )
        self.session.add(season)

        ingestor = NBASeasonsIngestor()

        try:
            ingestor.ingest_one(self.page, self.session)
        except:
            raise

        self.assertEqual(self.session.query(League).count(), 3)
        self.assertEqual(self.session.query(Season).count(), 2)
        season_query = self.session.query(Season).filter_by(
            league_id=league.id,
            start_year=date(2017, 1, 1),
            end_year=date(2018, 1, 1)
        ).one()
        self.assertTrue(season_query is not None)

    def test_ingest_recent_when_last_entry_is_2016_17(self):
        league = self.session.query(League).filter_by(
            abbreviation='NBA'
        ).one()
        season = Season(
            league=league,
            start_date=None,
            end_date=None,
            start_year=date(2016, 1, 1),
            end_year=date(2017, 1, 1),
            created_by='pycrawl'
        )
        self.session.add(season)
        self.session.commit()

        ingestor = NBASeasonsIngestor()

        try:
            ingestor.ingest_recent(self.page, self.session)
            self.session.commit()
        except:
            self.session.rollback()
            raise

        years_to_current = (self.get_current_season_start_year() 
                           - season.start_year.year 
                           + 1)
        self.assertEqual(self.session.query(Season).count(), years_to_current)

    def test_map_to_season_unknown_league_throws_exception(self):
        season_row = {
            'league': 'NHL',
            'start_year': date(2017, 1, 1),
            'end_year': date(2018, 1, 1),
            'url': 'https://www.hockey-reference.com/leagues/NHL_2018.html'
        }

        ingestor = NBASeasonsIngestor()

        self.assertRaises(exc.SQLAlchemyError, ingestor.map_to_season, 
            season_row, self.session)

if __name__ == '__main__':
    unittest.main()
