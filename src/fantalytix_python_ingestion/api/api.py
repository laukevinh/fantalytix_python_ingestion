from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify
)

from fantalytix_sqlalchemy.orm.common import League

from .db import get_db, expose

from .utils import get_or_create, commit_or_400

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
        
        fields_to_expose = ('name', 'abbreviation', 'sport')

        results = expose(instances, fields_to_expose)

        for result in results:
            result["links"] = {
                "rel": result['abbreviation'],
                "href": url_for('api.leagues_abbreviation', abbreviation=result['abbreviation'])
            }

        commit_or_400(db, msg="Could not create objects")

        return jsonify({
            "data": results,
            "count": len(results),
            "links": {
                "rel": 'self',
                "href": url_for('api.leagues')
            }
        })

    elif request.method == 'DELETE':
        db = get_db()
        num_deleted = db.query(League).delete()

        commit_or_400(db, msg="Could not delete objects")

        return jsonify({'count': num_deleted})

    fields_to_expose = ('name', 'abbreviation', 'sport')

    results = expose(get_db().query(League).all(), fields_to_expose)

    for result in results:
        result["links"] = {
            "rel": result['abbreviation'],
            "href": url_for('api.leagues_abbreviation', abbreviation=result['abbreviation'])
        }

    return jsonify({
        'data': results, 
        'count': len(results), 
        'links': {
            "rel": 'self',
            "href": url_for('api.leagues')
        }
    })

@bp.route('/leagues/<string:abbreviation>', methods=['GET', 'DELETE'])
def leagues_abbreviation(abbreviation):
    """GET returns one record. POST not allowed. DELETE removes this record."""
    if request.method == 'DELETE':
        db = get_db()
        num_deleted = db.query(League).filter_by(
            abbreviation=abbreviation).delete()

        commit_or_400(db, msg="Could not delete objects")

        return jsonify({'count': num_deleted})

    fields_to_expose = ('name', 'abbreviation', 'sport')

    results = expose(
        get_db().query(League).filter_by(abbreviation=abbreviation), 
        fields_to_expose
    )

    return jsonify({
        'data': results, 
        'count': len(results), 
        'links': {
            'rel': 'self',
            'href': url_for('api.leagues_abbreviation', abbreviation=abbreviation)
        }
    })
