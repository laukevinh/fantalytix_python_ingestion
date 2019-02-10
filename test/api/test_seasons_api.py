from .test_api import TestAPI

class TestSeasonsAPI(TestAPI):

    def setUp(self):
        super().setUp()
        super().setUpLeaguesTable()
        super().setUpSeasonsTable()

    def tearDown(self):
        super().tearDownLeaguesTable()
        super().tearDownSeasonsTable()
        super().tearDown()

    def test_seasons_get(self):
        resp = self.client.get(self.SEASON_API_URL)
        self.assertEqual(
            resp.get_json(), 
            {
                'data': [{
                    'league': {
                        'name': 'National Basketball Association',
                        'abbreviation': 'NBA',
                        'sport': 'basketball',
                        'links': {
                            'rel': 'NBA',
                            'href': self.LEAGUE_NBA_API_URL
                        }
                    },
                    'start_date': '2018-10-16',
                    'end_date': '2019-04-10',
                    'start_year': '2018-01-01',
                    'end_year': '2019-01-01',
                    'links': {
                        'rel': '/NBA/2019',
                        'href': self.LEAGUE_NBA_2019_API_URL
                    }
                }],
                'count': 1,
                'links': {
                    'rel': 'self',
                    'href': self.SEAON_API_URL
                },
            }
        )

if __name__ == '__main__':
    unittest.main()
