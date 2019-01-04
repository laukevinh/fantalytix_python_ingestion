"""This is a test for the NBALeaguesIngestor. """
import unittest
from urllib.request import urlopen
from urllib.parse import urljoin

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, LEAGUES_URL)

from fantalytix_python_ingestion.ingestion.sports_reference.basketball\
    .nba_leagues_ingestor import NBALeaguesIngestor

from fantalytix_sqlalchemy.orm.common.league import League
from fantalytix_sqlalchemy.test.settings import CONNECTION

class TestNBALeaguesIngestor(unittest.TestCase):
    
    def setUp(self):
        self.engine = create_engine(CONNECTION)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        with urlopen(urljoin(BASE_URL, LEAGUES_URL)) as resp:
            self.page = resp.read().decode('utf-8')

    def tearDown(self):
        self.session.query(League).delete()
        self.session.commit()
        self.session.close()

    def test_ingest_all(self):
        ingestor = NBALeaguesIngestor()

        try:
            ingestor.ingest_all(self.page, self.session)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

        self.assertEqual(self.session.query(League).count(), 3)

if __name__ == '__main__':
    unittest.main()
