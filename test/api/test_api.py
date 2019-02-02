import unittest

from ..settings import CONNECTION

from fantalytix_python_ingestion import api

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = api.create_app()
        self.app.config['DATABASE'] = CONNECTION 
        self.app.config['TESTING'] = True 
        self.app.config['ENVIRONMENT'] = 'development' 
        self.client = self.app.test_client()
        self.LEAGUE_API_URL = '/api/leagues'

    def tearDown(self):
        pass

    def test_leagues(self):
        resp = self.client.delete(self.LEAGUE_API_URL)

        resp = self.client.get(self.LEAGUE_API_URL)
        self.assertEqual(resp.get_json()['count'], 0)

        data = [
            {
                "name":"National Basketball Association", 
                "abbreviation":"NBA", 
                "sport":"basketball"
            },
            {
                "name":"American Basketball Association", 
                "abbreviation":"ABA", 
                "sport":"basketball"
            }
        ]

        resp = self.client.post(self.LEAGUE_API_URL, json={'data': data})
        self.assertEqual(resp.get_json()['count'], 2)

        resp = self.client.get(self.LEAGUE_API_URL)
        self.assertEqual(resp.get_json()['data'][0], data[0])
        self.assertEqual(resp.get_json()['count'], 2)

        resp = self.client.delete(self.LEAGUE_API_URL)
        self.assertEqual(resp.get_json()['count'], 2)

        resp = self.client.get(self.LEAGUE_API_URL)
        self.assertEqual(resp.get_json()['count'], 0)

    def test_league_abbreviation(self):
        import pdb
        pdb.set_trace()
        resp = self.client.delete(self.LEAGUE_API_URL)

        resp = self.client.get(self.LEAGUE_API_URL + '/NBA')
        self.assertEqual(resp.get_json()['count'], 0)

        data = [
            {
                "name":"National Basketball Association", 
                "abbreviation":"NBA", 
                "sport":"basketball"
            },
            {
                "name":"American Basketball Association", 
                "abbreviation":"ABA", 
                "sport":"basketball"
            }
        ]

        resp = self.client.post(self.LEAGUE_API_URL, json={'data': data})
        new_resp = self.client.get(resp.get_json()['data'][0]['links']['href'])
        new_data = data[0].copy()
        new_data['links'] = self.LEAGUE_API_URL + '/NBA'
        self.assertEqual(new_resp.get_json()['data'], [new_data])

        resp = self.client.delete(self.LEAGUE_API_URL + '/NBA')

if __name__ == '__main__':
    unittest.main()
