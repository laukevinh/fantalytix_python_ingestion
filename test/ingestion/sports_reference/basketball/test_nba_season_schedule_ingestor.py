from .test_nba import TestNBA

from datetime import date, datetime

from urllib.request import urlopen
from urllib.parse import urljoin

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, SEASON_SCHEDULE_URL)

from fantalytix_sqlalchemy.orm.common import (
    League, Season, Team
)

from fantalytix_sqlalchemy.orm.nba import NBAGame

from fantalytix_python_ingestion.ingestion.sports_reference.basketball\
    .nba_season_schedule_ingestor import NBASeasonScheduleIngestor

class TestNBASeasonScheduleIngestor(TestNBA):

    def setUp(self):
        super().setUp()
        super().setUpTeamsTable()
        super().setUpSeasonsTable()

        with urlopen(urljoin(BASE_URL, SEASON_SCHEDULE_URL.format(
            league='NBA', end_year='2019', month='october'))) as resp:
            self.page = resp.read().decode('utf-8')

    def tearDown(self):
        super().tearDownNBAGamesTable()
        super().tearDown()

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

        home_team = self.session.query(Team).filter_by(abbreviation="GSW").one()
        nbagame = self.session.query(NBAGame).filter_by(
            game_date=datetime(2018, 10, 31, 22, 30),
            home_team=home_team
            ).one()

        self.assertEqual(nbagame.away_team.abbreviation, "NOP")
        self.assertEqual(nbagame.home_score, 131)
        self.assertEqual(nbagame.away_score, 121)
        self.assertEqual(self.session.query(NBAGame).count(), 110)

if __name__ == '__main__':
    unittest.main()
