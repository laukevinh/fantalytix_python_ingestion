import json

from flask_marshmallow import Schema
from flask_marshmallow.fields import fields

class LeagueSchema(Schema):

    class Meta:
        fields = ('name', 'abbreviation', 'sport')

class SeasonSchema(Schema):

    league = fields.Nested('LeagueSchema')
    class Meta:
        fields = ('league', 'start_year', 'end_year')
