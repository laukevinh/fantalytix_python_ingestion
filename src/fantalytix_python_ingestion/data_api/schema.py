import json

from flask_marshmallow import Schema

class LeagueSchema(Schema):

    class Meta:
        fields = ('name', 'abbreviation', 'sport')
