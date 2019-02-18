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
            [{
                'name': 'National Basketball Association',
                'abbreviation': 'NBA',
                'sport': 'basketball',
            },
            {
                'name': 'Basketball Association of America',
                'abbreviation': 'BAA',
                'sport': 'basketball',
            }]
        )

    def test_leagues_abbreviation_get(self):
        resp = self.client.get(self.LEAGUE_NBA_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'name': 'National Basketball Association',
                'abbreviation': 'NBA',
                'sport': 'basketball',
            }
        )

if __name__ == '__main__':
    unittest.main()
