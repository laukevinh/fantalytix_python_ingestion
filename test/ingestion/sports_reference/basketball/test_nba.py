import unittest

from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fantalytix_sqlalchemy.orm.common import (
    League, Season, Team
)

from fantalytix_sqlalchemy.orm.nba import NBAGame

from ....settings import CONNECTION

class TestNBA(unittest.TestCase):
    
    def setUp(self):
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
        self.session.add(League(
            name='National Basketball Association',
            abbreviation='NBA',
            sport='basketball',
            created_by='pycrawl')
        )
        self.session.add(League(
            name='American Basketball Association',
            abbreviation='ABA',
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

    def setUpSeasonsTable(self):
        self.setUpLeaguesTable()

        league = self.session.query(League).filter_by(abbreviation='NBA').one()
        self.session.add(Season(
            league=league,
            start_date=date(2018, 10, 16),
            end_date=date(2019, 4, 10),
            start_year=date(2018, 1, 1),
            end_year=date(2019, 1, 1))
        )
        self.session.commit()

    def tearDownSeasonsTable(self):
        self.session.query(Season).delete()
        self.tearDownLeaguesTable()

    def setUpTeamsTable(self):
        teams = [
            {'abbreviation': 'MIL', 'team_name': 'milwaukee bucks'}, 
            {'abbreviation': 'TOR', 'team_name': 'toronto raptors'}, 
            {'abbreviation': 'IND', 'team_name': 'indiana pacers'}, 
            {'abbreviation': 'PHI', 'team_name': 'philadelphia 76ers'}, 
            {'abbreviation': 'BOS', 'team_name': 'boston celtics'}, 
            {'abbreviation': 'BRK', 'team_name': 'brooklyn nets'}, 
            {'abbreviation': 'DET', 'team_name': 'detroit pistons'}, 
            {'abbreviation': 'ORL', 'team_name': 'orlando magic'}, 
            {'abbreviation': 'CHO', 'team_name': 'charlotte hornets'}, 
            {'abbreviation': 'MIA', 'team_name': 'miami heat'}, 
            {'abbreviation': 'WAS', 'team_name': 'washington wizards'}, 
            {'abbreviation': 'ATL', 'team_name': 'atlanta hawks'}, 
            {'abbreviation': 'CHI', 'team_name': 'chicago bulls'}, 
            {'abbreviation': 'CLE', 'team_name': 'cleveland cavaliers'}, 
            {'abbreviation': 'NYK', 'team_name': 'new york knicks'}, 
            {'abbreviation': 'GSW', 'team_name': 'golden state warriors'}, 
            {'abbreviation': 'DEN', 'team_name': 'denver nuggets'}, 
            {'abbreviation': 'POR', 'team_name': 'portland trail blazers'}, 
            {'abbreviation': 'OKC', 'team_name': 'oklahoma city thunder'}, 
            {'abbreviation': 'HOU', 'team_name': 'houston rockets'}, 
            {'abbreviation': 'UTA', 'team_name': 'utah jazz'}, 
            {'abbreviation': 'LAC', 'team_name': 'los angeles clippers'}, 
            {'abbreviation': 'SAS', 'team_name': 'san antonio spurs'}, 
            {'abbreviation': 'SAC', 'team_name': 'sacramento kings'}, 
            {'abbreviation': 'LAL', 'team_name': 'los angeles lakers'}, 
            {'abbreviation': 'MIN', 'team_name': 'minnesota timberwolves'}, 
            {'abbreviation': 'NOP', 'team_name': 'new orleans pelicans'}, 
            {'abbreviation': 'DAL', 'team_name': 'dallas mavericks'}, 
            {'abbreviation': 'MEM', 'team_name': 'memphis grizzlies'}, 
            {'abbreviation': 'PHO', 'team_name': 'phoenix suns'}
        ]
        for team in teams:
            self.session.add(Team(
                name=team['team_name'],
                abbreviation=team['abbreviation'],
                status='active')
            )
        self.session.commit()

    def tearDownTeamsTable(self):
        self.session.query(Team).delete()
    
    def tearDownNBAGamesTable(self):
        self.session.query(NBAGame).delete()
        self.tearDownTeamsTable()
        self.tearDownSeasonsTable()

if __name__ == '__main__':
    unittest.main()

