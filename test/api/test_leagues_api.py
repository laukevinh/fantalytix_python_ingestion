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
                        'rel': 'NBA',
                        'href': self.LEAGUE_NBA_API_URL
                    }
                },
                {
                    'name': 'Basketball Association of America',
                    'abbreviation': 'BAA',
                    'sport': 'basketball',
                    'links': {
                        'rel': 'BAA',
                        'href': self.LEAGUE_BAA_API_URL
                    }
                }],
                'count': 2,
                'links': {
                    'rel': 'self',
                    'href': self.LEAGUE_API_URL
                },
            }
        )

    def test_leagues_delete(self):
        resp = self.client.delete(self.LEAGUE_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'count': 2,
            }
        )

    def test_leagues_post(self):
        data = [{
            'name':'American Basketball Association', 
            'abbreviation':'ABA', 
            'sport':'basketball',
            'created_by': 'pycrawl'
        }]

        resp = self.client.post(self.LEAGUE_API_URL, json={'data': data})
        self.assertEqual(
            resp.get_json(), 
            {
                'data': [{
                    'name': 'American Basketball Association',
                    'abbreviation': 'ABA',
                    'sport': 'basketball',
                    'links': {
                        'rel': 'ABA',
                        'href': self.LEAGUE_ABA_API_URL
                    }
                }],
                'count': 1,
                'links': {
                    'rel': 'self',
                    'href': self.LEAGUE_API_URL
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
                    'href': self.LEAGUE_NBA_API_URL
                }
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
            'name':'American Basketball Association', 
            'abbreviation':'ABA', 
            'sport':'basketball',
            'created_by': 'pycrawl'
        }]

        resp = self.client.post(self.LEAGUE_NBA_API_URL, json={'data': data})
        self.assertEqual(resp.status_code, 405)

if __name__ == '__main__':
    unittest.main()
