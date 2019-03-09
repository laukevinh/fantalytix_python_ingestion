from .test_nba import TestNBA

from datetime import date

from urllib.request import urlopen
from urllib.parse import urljoin

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, LEAGUES_URL)

from fantalytix_sqlalchemy.orm.common import (
    League, Season
)

from fantalytix_python_ingestion.ingestion.sports_reference.basketball\
    .nba_seasons_ingestor import NBASeasonsIngestor

class TestNBASeasonsIngestor(TestNBA):
    
    def setUp(self):
        super().setUp()
        super().setUpLeaguesTable()

        self.COUNT_BAA_SEASONS = 3
        self.COUNT_ABA_SEASONS = 9
        self.FIRST_NBA_SEASON_START_YEAR = 1949

        with urlopen(urljoin(BASE_URL, LEAGUES_URL)) as resp:
            self.page = resp.read().decode('utf-8')

    def tearDown(self):
        super().tearDownSeasonsTable()
        super().tearDown()

    def addSeason(self, start_year, end_year):
        league = self.session.query(League).filter_by(
            abbreviation='NBA'
        ).first()
        self.session.add(Season(
            league=league,
            start_year=start_year,
            end_year=end_year)
        )
        self.session.commit()

    def get_current_season_end_year(self):
        if date.today().month > 6:
            return date.today().year + 1
        else:
            return date.today().year

    def test_ingest_all(self):
        """Insert one correct and one incorrect season row. Ingest all 
        should update the incorrect row only and retreive all other 
        missing rows. 
        """
        self.addSeason(date(2018, 1, 1), date(2018, 1, 1))
        self.addSeason(date(2017, 1, 1), date(2018, 1, 1))

        ingestor = NBASeasonsIngestor()

        try:
            ingestor.ingest_all(self.page, self.session)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        count_total_seasons = ( self.COUNT_BAA_SEASONS
                              + self.COUNT_ABA_SEASONS
                              + self.get_current_season_end_year() 
                              - self.FIRST_NBA_SEASON_START_YEAR
                              )

        self.assertEqual(
            self.session.query(Season).count(), 
            count_total_seasons
        )

        self.assertEqual(
            self.session.query(Season).filter_by(
                    last_updated_by=ingestor.signature
                ).count(),
            1
        )

if __name__ == '__main__':
    unittest.main()
