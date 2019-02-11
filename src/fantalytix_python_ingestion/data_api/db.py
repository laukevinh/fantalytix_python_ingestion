from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import current_app, g

from .utils import log_caller

def get_db():
    if current_app.config.get('DATABASE') is None:
        raise Exception("Database not configured")

    if 'db' not in g:
        engine = create_engine(current_app.config.get('DATABASE'))
        Session = scoped_session(sessionmaker(bind=engine))
        g.db = Session

    return g.db

@log_caller
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
