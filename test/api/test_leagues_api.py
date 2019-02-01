"""This is a test for the NBASeasonsIngestor. """
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


from fantalytix_sqlalchemy.orm.common.league import League
from fantalytix_sqlalchemy.orm.common.season import Season
from ..settings import CONNECTION

from fantalytix_python_ingestion import api

class TestLeagueAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = api.create_app()
        self.app.config['DATABASE'] = CONNECTION 
        self.app.config['TESTING'] = True 
        self.app.config['ENVIRONMENT'] = 'development' 
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_leagues_route(self):
        resp = self.client.delete('/leagues/')
        resp = self.client.get('/leagues/')
        self.assertEqual(len(resp.get_json()), 0)

        resp = self.client.post('/leagues/', json={
            '0': {
                "name":"National Basketball Association", 
                "abbreviation":"NBA", 
                "sport":"basketball"
            },
            '1': {
                "name":"American Basketball Association", 
                "abbreviation":"ABA", 
                "sport":"basketball"
            }
        })

        self.assertEqual(resp.get_json()['num_created'], 2)
        resp = self.client.get('/leagues/')
        self.assertEqual(resp.get_json()['0']['abbreviation'], 'ABA')

        resp = self.client.delete('/leagues/')
        self.assertEqual(resp.get_json()['num_deleted'], 2)
        resp = self.client.get('/leagues/')
        self.assertEqual(len(resp.get_json()), 0)

if __name__ == '__main__':
    unittest.main()
