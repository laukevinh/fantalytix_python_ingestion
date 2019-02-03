import unittest

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from fantalytix_sqlalchemy.orm.common.league import League

from ..settings import CONNECTION

from fantalytix_python_ingestion import api

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        """Setup Flask's test client. Setup sqlalchemy to initialize db."""
        self.app = api.create_app()
        self.app.config['DATABASE'] = CONNECTION 
        self.app.config['TESTING'] = True 
        self.app.config['ENVIRONMENT'] = 'development' 
        self.client = self.app.test_client()
        self.LEAGUE_API_URL = '/api/leagues'
        self.LEAGUE_NBA_API_URL = self.LEAGUE_API_URL + '/NBA'
        self.LEAGUE_ABA_API_URL = self.LEAGUE_API_URL + '/ABA'

        self.engine = create_engine(CONNECTION)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.add(League(
            name='National Basketball Association',
            abbreviation='NBA',
            sport='basketball',
            created_by='pycrawl')
        )
        self.session.commit()

    def tearDown(self):
        self.session.query(League).delete()
        self.session.commit()
        self.session.close()

    def test_leagues_get(self):
        resp = self.client.get(self.LEAGUE_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'data': [{
                    "name": 'National Basketball Association',
                    "abbreviation": 'NBA',
                    "sport": 'basketball',
                    "links": {
                        "rel": "NBA",
                        "href": self.LEAGUE_NBA_API_URL
                    }
                }],
                'count': 1,
                'links': {
                    "rel": 'self',
                    'href': self.LEAGUE_API_URL
                },
            }
        )

    def test_leagues_delete(self):
        resp = self.client.delete(self.LEAGUE_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'count': 1,
            }
        )

    def test_leagues_post(self):
        data = [{
            "name":"American Basketball Association", 
            "abbreviation":"ABA", 
            "sport":"basketball",
            "created_by": 'pycrawl'
        }]

        resp = self.client.post(self.LEAGUE_API_URL, json={'data': data})
        self.assertEqual(
            resp.get_json(), 
            {
                'data': [{
                    "name": 'American Basketball Association',
                    "abbreviation": 'ABA',
                    "sport": 'basketball',
                    "links": {
                        "rel": "ABA",
                        "href": self.LEAGUE_ABA_API_URL
                    }
                }],
                'count': 1,
                'links': {
                    "rel": 'self',
                    'href': self.LEAGUE_API_URL
                },
            }
        )

    def test_leagues_abbreviation_get(self):
        resp = self.client.get(self.LEAGUE_NBA_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'data': [{
                    "name": 'National Basketball Association',
                    "abbreviation": 'NBA',
                    "sport": 'basketball',
                }],
                'count': 1,
                'links': {
                    "rel": 'self',
                    'href': self.LEAGUE_NBA_API_URL
                },
            }
        )

    def test_leagues_abbreviation_delete(self):
        resp = self.client.delete(self.LEAGUE_NBA_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'count': 1,
            }
        )


    def test_leagues_abbreviation_post(self):
        data = [{
            "name":"American Basketball Association", 
            "abbreviation":"ABA", 
            "sport":"basketball",
            "created_by": 'pycrawl'
        }]

        resp = self.client.post(self.LEAGUE_NBA_API_URL, json={'data': data})
        self.assertEqual(resp.status_code, 405)

if __name__ == '__main__':
    unittest.main()
