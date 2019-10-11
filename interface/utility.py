# -*- encoding: utf-8 -*-

__author__ = "chenty"

import re

from database.base import Session


base_return_code = {
    "OK": 0,
    "INVALID_DATA": 1,
}

def get_session(func):
    def ret_func(*args, **kwargs):
        try:
            session = Session()
        except Exception as e:
            # Todo: Log exception.
            return -2, None
        try:
            commit, code, res = func(*args, session=session, **kwargs)
            if commit:
                session.commit()
            else:
                session_roll_back(session)
            return code, res
        except Exception as e:
            session_roll_back(session)
            raise
            # Todo: Log exception.
            return -1, None
    return ret_func

def session_roll_back(session):
    try:
        session.roll_back()
    except Exception as e:
        # Todo: Log exception.
        pass
    return

def end_session():
    Session.remove()
    return
