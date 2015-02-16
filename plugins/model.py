# This file contains all the data classes which are filled by the process
# and used by the other plugins

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from config import wowconfig
from sqlalchemy.engine import create_engine

Base = declarative_base()

class Realm(Base):
    __tablename__ = 'realms'
    
    name = Column(String, primary_key=True)
    online = Column(Boolean)
    lastseen = Column(DateTime)
    lastchecked = Column(DateTime)
    areas = relationship("PvPArea", backref="realm")

class PvPArea(Base):
    __tablename__ = 'pvpareas'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    faction = Column(String)
    status = Column(String)
    next = Column(DateTime)
    realm_id = Column(String, ForeignKey('realms.name'), primary_key=True)

engine = create_engine(wowconfig["database"])
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
