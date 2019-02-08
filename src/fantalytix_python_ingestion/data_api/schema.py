import json

from flask_marshmallow import Schema
from flask_marshmallow.fields import Hyperlinks, URLFor

from flask import url_for

class LeagueSchema(Schema):
    class Meta:
        fields = ('name', 'abbreviation', 'sport', 'links')

    links = Hyperlinks({
        'rel': 'self',
        'href': URLFor('api.leagues_abbreviation', abbreviation='<abbreviation>')
    })

    def dump_many(self, arg):
        results = super().dump(arg)
        for result in results.data:
            result['links']['rel'] = result['abbreviation']
        return results._replace(
            data={
                'data': results.data,
                'count': len(results.data),
                'links': {
                    'rel': 'self',
                    'href': url_for('api.leagues')
                }
            }
        )

    def dump(self, arg):
        if self.many is True:
            return self.dump_many(arg)
        return super().dump(arg)
