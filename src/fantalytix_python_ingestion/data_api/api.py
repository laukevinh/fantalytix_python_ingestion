from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)

from fantalytix_sqlalchemy.orm.common import League

from .db import get_db, expose

from .utils import get_or_create, commit_or_400

from .schema import LeagueSchema

leagues_schema = LeagueSchema(strict=True, many=True)
league_schema = LeagueSchema(strict=True)
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/leagues', methods=['GET', 'POST', 'DELETE'])
def leagues():
    """GET returns all data. POST adds data if it does not exist.
    DELETE removes all data.
    """
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return ("POST must have 'application/json' header "
                    "and be valid json", 400)

        db = get_db()

        instances = []
        for row in data['data']:
            instance, created = get_or_create(db, League, **row)
            if created:
                instances.append(instance)
        
        commit_or_400(db, msg='Could not create objects')

        results = leagues_schema.dump(instances)

        return jsonify(results.data)

    elif request.method == 'DELETE':
        db = get_db()
        num_deleted = db.query(League).delete()

        commit_or_400(db, msg='Could not delete objects')

        return jsonify({'count': num_deleted})

    results = leagues_schema.dump(get_db().query(League).all())

    return jsonify(results.data)

@bp.route('/leagues/<string:abbreviation>', methods=['GET', 'DELETE'])
def leagues_abbreviation(abbreviation):
    """GET returns one record. POST not allowed. DELETE removes this record."""
    if request.method == 'DELETE':
        db = get_db()

        try:
            num_deleted = db.query(League).filter_by(
                abbreviation=abbreviation).delete()
        except:
            return ('Object to delete not found', 400)

        commit_or_400(db, msg='Could not delete objects')

        return jsonify({'count': num_deleted})

    results = league_schema.dump(
        get_db().query(League).filter_by(abbreviation=abbreviation).first()
    )

    return jsonify(results.data)
