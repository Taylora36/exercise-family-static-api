"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    # this is how you can use the Family datastructure by calling its methods
    mem = jackson_family.get_member(id)
    print("this is from inside the app.py", mem)
    return jsonify(mem), 200
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    # this is how you can use the Family datastructure by calling its methods
    mem = jackson_family.delete_member(id)
    return jsonify({
        "done": True
    }), 200
@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.get_json()
    first_name = request_body["first_name"]
    age = request_body["age"]
    id = request_body["id"]
    lucky_numbers = request_body["lucky_numbers"]
    if id is not None:
        jackson_family.add_member({
        "id": id,
        "first_name": first_name,
        "age": age,
        "lucky_numbers": lucky_numbers
    })
    else:
        jackson_family.add_member({
        "first_name": first_name,
        "age": age,
        "lucky_numbers": lucky_numbers
    })
    return jsonify("success"), 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
