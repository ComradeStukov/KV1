# -*- encoding: utf-8 -*-

__author__ = "chenty"


test = True

db_url = "sqlite:///:memory:"
echo = True

if test:
    # db_url = "sqlite:////tmp/kv1.db"
    # db_url = "sqlite:///:memory:"
    db_url = "mysql+mysqlconnector:/kv1:HoyZv2sPzShdMFK4@localhost:3306/KV1"
    echo = True
