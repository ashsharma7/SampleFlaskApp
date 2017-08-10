from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine) 
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/')
def listRestaurants():
    restaurants = session.query(Restaurant)
    return render_template("restaurants.html", restaurants=restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    r = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = r.id)
    return render_template("menu.html", restaurant=r, items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], 
            description=request.form['description'],
            price = request.form['price'],
            course = request.form['course'],
            restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New Menu Item Created!')
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
        flash('Menu Item Edited!')
        return redirect(url_for("restaurantMenu",restaurant_id=restaurant_id))
    else:
        r = session.query(Restaurant).filter_by(id=restaurant_id).one()
        itemToEdit = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
        return render_template("editmenuitem.html",restaurant=r, menuitem=itemToEdit)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        itemToDelete = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Deleted!')
        return redirect(url_for("restaurantMenu",restaurant_id=restaurant_id))
    else:
        itemToDelete = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id = menu_id).one()
        return render_template("deletemenuitem.html",item=itemToDelete)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

if __name__ == '__main__':
    app.secret_key = 'SuperSecretKey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
