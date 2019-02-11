import json

from marshmallow import post_dump

from flask_marshmallow import Schema
from flask_marshmallow.fields import Hyperlinks, URLFor

from flask import url_for

class BaseSchema(Schema):

    __link_rel__ = {
        'collection': None,
        'record': None
    }

    def fix_nested_self_link_rels(self, data):
        for entry in data:
            entry['links']['rel'] = self.__link_rel__['record']

    def wrap(self, data):
        return {
            'data': data,
            'count': len(data),
            'links': {
                'rel': 'self',
                'href': self.__link_rel__['collection']
            }
        }

    @post_dump(pass_many=True)
    def wrap_links_if_many(self, data, many):
        if many is True:
            self.fix_nested_self_link_rels(data)
            return self.wrap(data)
        return data

class LeagueSchema(BaseSchema):
    __link_rel__ = {
        'collection': '/api/leagues',
        'record': '/api/leagues/abbreviation'
    }

    class Meta:
        fields = ('name', 'abbreviation', 'sport', 'links')

    links = Hyperlinks({
        'rel': 'self',
        'href': URLFor('api.leagues_abbreviation', abbreviation='<abbreviation>')
    })
