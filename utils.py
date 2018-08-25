from datetime import datetime
from dateutil.parser import parse


def unify_datetime(dt):
    if isinstance(dt, datetime):
        try:
            dt = datetime.strftime(dt, '%Y-%m-%d %H:%M')
        except Exception as ex:
            print('Got an exception while unifying datetime: {0}'.format(ex))
    elif isinstance(dt, str):
        pass

    return parse(dt, ignoretz=True)
