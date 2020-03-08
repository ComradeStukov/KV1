# -*- coding: utf-8 -*-

# The MIT License (MIT)
# Copyright (c) 2020 SBofGaySchoolBuPaAnything
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

__author__ = "chenty"

import traceback

from database.base import Session


# Return code of interfaces
base_return_code = {
    "OK": 0,
    "INVALID_DATA": 1,
}

def get_session(func):
    """
    Decorator function
    Get a database session and invoke the function with it
    :param func: The function
    :return: The function after decoration
    """
    def ret_func(*args, **kwargs):
        # Try to get the session
        try:
            session = Session()
        except Exception:
            traceback.print_exc()
            return -2, None
        try:
            # Invoke the function, and whether it should be commit, its return code and result
            commit, code, res = func(*args, session=session, **kwargs)
            # Commit it, if required, otherwise rollback
            if commit:
                session.commit()
            else:
                session_rollback(session)
            return code, res
        except Exception:
            # Roll back when meets an exception
            session_rollback(session)
            traceback.print_exc()
            return -1, None
    return ret_func

def session_rollback(session):
    """
    Roll back, ignoring exception
    :param session: The database session
    :return: None
    """
    try:
        session.rollback()
    except Exception:
        traceback.print_exc()
    return

def end_session():
    """
    Remove the session factory
    :return:
    """
    Session.remove()
    return
