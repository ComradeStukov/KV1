# -*- encoding: utf-8 -*-

__author__ = "chenty"

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database import config


engine = create_engine(config.db_url, echo=config.echo)
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))
