from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from databaseSetup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def show_menu(id):
    menu = session.query(MenuItem).filter(MenuItem.restaurant_id == id).all()
    return menu 

def add_item(id,name,desc,Course,price):
    restaurant = session.query(Restaurant).get(id)
    menuItem = MenuItem(name = name, description = desc, price = "$"+price, course = Course, restaurant = restaurant)
    session.add(menuItem)
    session.commit()
    

