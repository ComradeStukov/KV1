# -*- encoding: utf-8 -*-

__author__ = "chenty"


test = True

db_url = "sqlite:///:memory:"
echo = True

if test:
    db_url = "sqlite:////tmp/kv1.db"
    echo = True
