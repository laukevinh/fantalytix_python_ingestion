from .test_api import TestAPI

class TestSeasonsAPI(TestAPI):

    def setUp(self):
        super().setUp()
        super().setUpSeasonsTable()

    def tearDown(self):
        super().tearDownSeasonsTable()
        super().tearDown()

    def test_seasons_get(self):
        resp = self.client.get(self.SEASON_API_URL)
        self.assertEqual(
            resp.get_json(), 
            [
                {
                    'league': {
                        'name': 'National Basketball Association',
                        'abbreviation': 'NBA',
                        'sport': 'basketball',
                    },
                    'start_year': '2018-01-01',
                    'end_year': '2019-01-01',
                },
            ]
        )

    def test_seasons_league_endyear(self):
        resp = self.client.get(self.SEASON_NBA_2019_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'league': {
                    'name': 'National Basketball Association',
                    'abbreviation': 'NBA',
                    'sport': 'basketball',
                },
                'start_year': '2018-01-01',
                'end_year': '2019-01-01',
            }
        )

if __name__ == '__main__':
    unittest.main()
