from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

# Café Table Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/random')
def random_cafe():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars()
    cafe_list = []
    for cafe in all_cafes:
        cafe_list.append(cafe)

    # Café that was randomly picked
    cafe_random = random.choice(cafe_list)
    return jsonify(
        cafe={
            'name': cafe_random.name,
            'map_url': cafe_random.map_url,
            'img_url': cafe_random.img_url,
            'location': cafe_random.location,
        },
        amenities={
            'seats': cafe_random.seats,
            'has_toilet': cafe_random.has_toilet,
            'has_wifi': cafe_random.has_wifi,
            'has_sockets': cafe_random.has_sockets,
            'can_take_calls': cafe_random.can_take_calls,
            'coffee_price': cafe_random.coffee_price
        }
    )

# Read Record
@app.route('/all')
def all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars()

    cafe_list = []

    for cafe in all_cafes:
        cafe_list.append({
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
            "has_sockets": cafe.has_sockets,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "id":cafe.id,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "map_url": cafe.map_url,
            "name": cafe.name,
            "seats": cafe.seats

        })
    return jsonify(
        cafes = cafe_list
    )

@app.route('/search')
def search():
    location = request.args.get('loc')
    print(f"This is the grabbed 'loc' variable from the URL: {location}")

    result = db.session.execute(db.select(Cafe).where(Cafe.location == location))
    queried_cafes = result.scalars()

    cafe_list = []

    for cafe in queried_cafes:
        cafe_list.append({
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
            "has_sockets": cafe.has_sockets,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "id": cafe.id,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "map_url": cafe.map_url,
            "name": cafe.name,
            "seats": cafe.seats
        })

    if len(cafe_list) == 0:
        return jsonify(
            error={
                "Not found": "Sorry, we don't have a cafe at that location"
            }
        )
    else:
        return jsonify(
            cafes=cafe_list
        )

# Create Record
@app.route('/add', methods=['POST'])
def add_cafe():
    has_sockets = False
    has_toilet = False
    has_wifi = False
    can_take_calls = False

    if request.form['has_sockets'].lower() == 'true':
        has_sockets = True
    elif request.form['has_toilet'].lower() == 'true':
        has_toilet = True
    elif request.form['has_wifi'].lower() == 'true':
        has_wifi = True
    elif request.form['can_take_calls'].lower() == 'true':
        can_take_calls = True

    new_cafe = Cafe(
        name = request.form['name'],
        map_url = request.form['map_url'],
        img_url = request.form['img_url'],
        location = request.form['location'],
        seats = request.form['seats'],
        has_toilet = has_toilet,
        has_wifi = has_wifi,
        has_sockets = has_sockets,
        can_take_calls = can_take_calls,
        coffee_price = request.form['coffee_price'],
    )

    print(f"New cafe's ID: {new_cafe.id}")
    db.session.add(new_cafe)
    db.session.commit()
    print(f"New cafe's ID: {new_cafe.id}")

    return jsonify(
        repsonse={
            "success": "Successfully added the new cafe."
        }
    )

# Update Record
@app.route('/update-price/<cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    cafe_to_update = db.session.get(Cafe, cafe_id)

    if cafe_to_update is not None:
        cafe_to_update.coffee_price = request.args['new_price']
        db.session.commit()

        return jsonify(
            success = "Successfully updated the price."
        )
    else:
        return jsonify(
            error = {
                "Not Found": "Sorry, a cafe with that id was not found in the database"
            }
        )

# Delete Record
@app.route('/report-closed/<cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    cafe_to_delete = db.session.get(Cafe, cafe_id)
    if request.args['api_key'] == 'TopSecretAPIKey':
        if cafe_to_delete is not None:
            db.session.delete(cafe_to_delete)
            db.session.commit()

            return jsonify(
                success="Successfully deleted the cafe."
            )
        else:
            return jsonify(
                error={
                    "Not Found": "Sorry, a cafe with that id was not found in the database"
                }
            )
    else:
        return jsonify(
            error="Sorry that's not allowed. Make sure you have the correct api_key."
        )

if __name__ == '__main__':
    app.run(debug=True)
