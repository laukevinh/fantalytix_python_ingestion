import json

from flask_marshmallow import Schema
from flask_marshmallow.fields import Hyperlinks, URLFor

from flask import url_for

class FantalytixSchema(Schema):

    def wrap(self, results, self_href):
        return results._replace(
            data={
                'data': results.data,
                'count': len(results.data),
                'links': {
                    'rel': 'self',
                    'href': self_href
                }
            }
        )

    def dump(self, arg):
        if self.many is True:
            results = super().dump(arg)
            self.add_links(results)
            return self.wrap(results, self_href=url_for(self.ENDPOINT))

        return super().dump(arg)

class LeagueSchema(FantalytixSchema):
    class Meta:
        fields = ('name', 'abbreviation', 'sport', 'links')

    links = Hyperlinks({
        'rel': 'self',
        'href': URLFor('api.leagues_abbreviation', abbreviation='<abbreviation>')
    })

    ENDPOINT = 'api.leagues'

    def add_links(self, results):
        for result in results.data:
            result['links']['rel'] = result['abbreviation']

class SeasonSchema(Schema):
    class Meta:
        fields = ('league', 'start_date', 'end_date', 'start_year', 'end_year')

    links = Hyperlinks({
        'rel': 'self',
        'href': URLFor('api.season_league_year', 
            league='<league_abbreviation>', 
            year='<end_year>'
        )
    })

    ENDPOINT = 'api.seasons'

    def add_links(self, results):
        for results in results.data:
            result['links']['rel'] = result['league']
