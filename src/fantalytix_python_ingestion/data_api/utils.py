import functools

def log_caller(func):
    @functools.wraps(func)
    def log_before(*args, **kwargs):
        import inspect
        print(' * called from', inspect.stack()[1].function) 
        return func(*args, **kwargs)
    return log_before

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance, True

def commit_or_400(session, msg='Could not process request', status=400):
    try:
        session.commit()
    except:
        session.rollback()
        return (msg, status)

def crossdomain(origin=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapped_function(*args, **kwargs):
            resp = f(*args, **kwargs)
            resp.headers.add('Access-Control-Allow-Origin', origin)
            return resp
        return wrapped_function
    return decorator
