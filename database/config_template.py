# -*- encoding: utf-8 -*-

__author__ = "chenty"


test = True

# db_url = "sqlite:"
# db_url = "sqlite:////tmp/kv1.db"
# db_url = "mysql+mysqlconnector:/kv1:PASSWORD@localhost:3306/KV1"

db_url = "sqlite:///:memory:"
echo = True

if test:
    db_url = "sqlite:///:memory:"
    echo = True
