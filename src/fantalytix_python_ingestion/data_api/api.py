from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)

from fantalytix_sqlalchemy.orm.common import League

from .db import get_db

from .utils import crossdomain

from .schema import LeagueSchema

league_schema = LeagueSchema(strict=True)
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/leagues', methods=['GET'])
@crossdomain(origin='http://localhost:3000')
def leagues():
    results = league_schema.dump(get_db().query(League).all(), many=True)

    return jsonify(results.data)

@bp.route('/leagues/abbreviation/<string:abbreviation>', methods=['GET'])
@crossdomain(origin='http://localhost:3000')
def leagues_abbreviation(abbreviation):
    try:
        results = league_schema.dump(
            get_db().query(League).filter_by(abbreviation=abbreviation).first()
        )
    except AttributeError:
        return jsonify({})

    return jsonify(results.data)
