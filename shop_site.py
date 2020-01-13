import json
import uuid

from flask import Flask
from flask import request
from flask import render_template

from model.post import Post
from model.user import User
from errors import register_error_handlers

from security.basic_authentication import generate_password_hash
from security.basic_authentication import init_basic_auth


app = Flask(__name__)
auth = init_basic_auth()
register_error_handlers(app)

@app.route("/api/users", methods = ["POST"])
def create_user():
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 400
    hashed_password = generate_password_hash(user_data["Password"])
    user = User(user_data["Username"], hashed_password, user_email["E-mail"], 			user_adress["Adress"], user_phone["Phone"])
    user.save()
    return json.dumps(user.to_dict()), 201

