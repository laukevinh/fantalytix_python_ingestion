import unittest

from datetime import date

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from fantalytix_sqlalchemy.orm.common import League

from ..settings import CONNECTION

from fantalytix_python_ingestion import data_api

class TestAPI(unittest.TestCase):

    def setUp(self):
        """Setup Flask's test client. Setup sqlalchemy to initialize db."""
        self.app = data_api.create_app()
        self.app.config['DATABASE'] = CONNECTION 
        self.app.config['TESTING'] = True 
        self.app.config['ENVIRONMENT'] = 'development' 
        self.client = self.app.test_client()

        self.engine = create_engine(CONNECTION)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def setUpLeaguesTable(self):
        self.LEAGUE_API_URL = '/api/leagues'
        self.LEAGUE_NBA_API_URL = self.LEAGUE_API_URL + '/abbreviation/NBA'
        self.LEAGUE_BAA_API_URL = self.LEAGUE_API_URL + '/abbreviation/BAA'
        self.LEAGUE_ABA_API_URL = self.LEAGUE_API_URL + '/abbreviation/ABA'

        self.session.add(League(
            name='National Basketball Association',
            abbreviation='NBA',
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

    def tearDownLeaguesTable(self):
        self.session.query(League).delete()

if __name__ == '__main__':
    unittest.main()
