from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine) 
session = DBSession()

app = Flask(__name__)


@app.route('/')
@app.route('/hello')
def helloWorld():
    restaurants = session.query(Restaurant)
    output = ""
    for r in restaurants:
        output += "<strong>"
        output += r.name
        output += "</strong>"
        output += "<br>"
        items = session.query(MenuItem).filter_by(restaurant_id = r.id)
        for i in items:
            output += i.name + " " + i.price + "<br>&#160;&#160;&#160;&#160;" + i.description
            output += "<br>"
        output += "<br><br>"
    return output

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    r = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = r.id)
    return render_template("menu.html", restaurant=r, items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for("restaurantMenu",restaurant_id=restaurant_id))
    else:
        return render_template("newmenuitem.html",restaurant_id = restaurant_id)
# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        itemToEdit = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
        newName = request.form['name']
        itemToEdit.name = newName
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for("restaurantMenu",restaurant_id=restaurant_id))
    else:
        r = session.query(Restaurant).filter_by(id=restaurant_id).one()
        itemToEdit = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
        return render_template("editmenuitem.html",restaurant=r, menuitem=itemToEdit)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
