from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from StatesData_Setup import *

engine = create_engine('sqlite:///statesdatabase.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete States if exisitng.
session.query(States).delete()
# Delete StatesName if exisitng.
session.query(StatesName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
FirstUser = User(
    name="Boyapati Sravani", email="sravani3141@gmail.com")
session.add(FirstUser)
session.commit()
print ("Successfully Add First User")
# Create sample States
state1 = States(name="Andhra Pradesh",
                     user_id=1)
session.add(state1)
session.commit()

state2 = States(name="Telangana",
                     user_id=1)
session.add(state2)
session.commit

state3 = States(name="Gujarat",
                     user_id=1)
session.add(state3)
session.commit()
state4 = States(name="Arunachal Pradesh",
                     user_id=1)
session.add(state4)
session.commit()

state5 = States(name="Haryana",
                     user_id=1)
session.add(state5)
session.commit()

state6 = States(name="Goa",
                     user_id=1)
session.add(state6)
session.commit()

# Populare a bykes with models for testing
# Using different users for bykes names year also
statename1 = StatesName(
    district="prakasam", headquartes="Ongole", revenue_division="3",
    mandals="56", population="3,392,764", area="17,626 sq.km ",
    density="193 sq.km", statesid=1, user_id=1)
session.add(statename1)
session.commit()

statename2 = StatesName(
    district="prakasam", headquartes="Ongole", revenue_division=3,
    mandals=56, population="3,392,764", area="17,626 sq.km ",
    density="193 sq.km", statesid=1, user_id=1)
session.add(statename1)
session.commit()
statename2 = StatesName(
    district="Kurnool", headquartes="Kurnool", revenue_division=3,
    mandals=54, population="4,046,601", area="17,658sq.km ",
    density="229sq.km", statesid=2, user_id=1)
session.add(statename2)
session.commit()

statename3 = StatesName(
    district="Anantapur", headquartes="Anantapur", revenue_division=5,
    mandals=63, population="4,083,315", area="19,130sq.km",
    density="213sq.km", statesid=3, user_id=1)
session.add(statename3)
session.commit()

statename4 = StatesName(
    district="Kadapa",
    headquartes="Kadapa",
    revenue_division=3,
    mandals=50,
    population="2,884,524",
    area="15,359sq.km",
    density="188sq.km",
    statesid=4,
    user_id=1)
session.add(statename4)
session.commit()
statename5 = StatesName(
    district="Chittoor",
    headquartes="Chittoor",
    revenue_division=3,
    mandals=66,
    population="4,170,468",
    area="15,152sq.km ",
    density="275sq.km",
    statesid=5,
    user_id=1)
session.add(statename5)
session.commit()
print("Your states database has been inserted!")
