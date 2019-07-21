from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from databaseSetup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def list_all():
    result = []
    items = session.query(Restaurant).all()
    for item in items:
        result.append(item)
    return result

def add_restaurant(rest_name):
    restaurant1 = Restaurant(name = rest_name)
    session.add(restaurant1)
    session.commit()

def edit_restaurant(id,new_name):
    item = session.query(Restaurant).get(id)
    item.name = new_name
    session.add(item)
    session.commit() 

def find_restaurant(id):
    item = session.query(Restaurant).get(id)
    return item

def delete_restaurant(id):
    item = session.query(Restaurant).get(id)
    session.delete(item)
    session.commit()

