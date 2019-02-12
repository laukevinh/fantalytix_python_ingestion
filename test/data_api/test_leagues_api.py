from .test_api import TestAPI

class TestLeaguesAPI(TestAPI):

    def setUp(self):
        super().setUp()
        super().setUpLeaguesTable()

    def tearDown(self):
        super().tearDownLeaguesTable()
        super().tearDown()

    def test_leagues_get(self):
        resp = self.client.get(self.LEAGUE_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'data': [{
                    'name': 'National Basketball Association',
                    'abbreviation': 'NBA',
                    'sport': 'basketball',
                    'links': {
                        'rel': '/api/leagues/abbreviation',
                        'href': '/api/leagues/abbreviation/NBA'
                    }
                },
                {
                    'name': 'Basketball Association of America',
                    'abbreviation': 'BAA',
                    'sport': 'basketball',
                    'links': {
                        'rel': '/api/leagues/abbreviation',
                        'href': '/api/leagues/abbreviation/BAA'
                    }
                }],
                'count': 2,
                'links': {
                    'rel': 'self',
                    'href': '/api/leagues'
                },
            }
        )

    def test_leagues_abbreviation_get(self):
        resp = self.client.get(self.LEAGUE_NBA_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'name': 'National Basketball Association',
                'abbreviation': 'NBA',
                'sport': 'basketball',
                'links': {
                    'rel': 'self',
                    'href': '/api/leagues/abbreviation/NBA'
                }
            }
        )

if __name__ == '__main__':
    unittest.main()
