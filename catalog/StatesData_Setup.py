import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(300))


class States(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="states")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class StatesName(Base):
    __tablename__ = 'statesname'
    id = Column(Integer, primary_key=True)
    district = Column(String(350), nullable=False)
    headquartes = Column(String(150))
    revenue_division = Column(Integer)
    mandals = Column(Integer)
    population = Column(String(250))
    area = Column(String(250))
    density = Column(String(250))
    statesid = Column(Integer, ForeignKey('states.id'))
    states = relationship(
        States, backref=backref('statesname', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="statesname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'district': self.district,
            'hadquartes': self.headquartes,
            'revenue_division': self.revenue_division,
            'mandals': self.mandals,
            'population': self.population,
            'area': self.area,
            'density': self.density,
            'id': self.id
        }

engin = create_engine('sqlite:///statesdatabase.db')
Base.metadata.create_all(engin)
