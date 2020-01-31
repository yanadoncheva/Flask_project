import json
import uuid

from flask import Flask
from flask import request
from flask import render_template, redirect, url_for, jsonify

from model.post import Post
from model.user import User
from errors import register_error_handlers

# from security.basic_authentication import generate_password_hash
# from security.basic_authentication import init_basic_auth


app = Flask(__name__)

# auth = init_basic_auth()
register_error_handlers(app)

@app.route("/api/posts/new", methods = ["POST", "GET"])
def create_post():
	if request.method == 'GET':
		return render_template("new_post.html")
	elif request.method == 'POST':
		post_data = request.get_json(force=True, silent=True)
		if post_data == None:
		    return "Bad request", 400
		post = Post(post_data["title"], post_data["content"], post_data["price"], post_data["post_date"], post_data["available"], post_data["buyer"])
		post.save()
		return redirect('/api/posts')


@app.route("/api/posts", methods = ["GET"])
def list_posts():
	#result = {"result": []}
	# post in Post.all():
    #    result["result"].append(post.to_dict())
    #return json.dumps(result)
	return render_template("posts.html", posts=Post.all())


@app.route("/api/posts/<post_id>", methods = ["GET"])
def get_post(post_id):
    return json.dumps(Post.find(post_id).to_dict())


#@app.route("/api/posts/<post_id>", methods = ["DELETE"])
#def delete_post(post_id):
    #Post.delete(post_id)
@app.route('/api/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
	post = Post.find(id)
	post.delete()

	return redirect('/')


@app.route("/api/posts/<post_id>", methods = ["PATCH"])
def update_post(post_id):
	post_data = request.get_json(force=True, silent=True)
	if post_data == None:
		return "Bad request", 400

	post = Post.find(post_id)
	if "title" in post_data:
		post.title = post_data["title"]
	if "content" in post_data:
		post.content = post_data["content"]
	if "price" in post_data:
		post.price = post_data["price"]
	if "post_date" in post_data:
		post.post_date = post_data["post_date"]
	if "available" in post_data:
		post.available = post_data["available"]
	if "buyer" in post_data:
		post.buyer = post_data["buyer"]

	return json.dumps(post.save().to_dict())


@app.route("/api/users", methods = ["POST"])
def create_user():
    user_data = request.get_json(force=True, silent=True)
    if user_data == None:
        return "Bad request", 400
    # hashed_password = generate_password_hash(user_data["password"])
    # user = User(user_data["username"], hashed_password, user_email["email"], user_adress["adress"], user_phone["phone"])
    # user.save()
    return json.dumps(user.to_dict()), 201

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password']),
			request.form['email'],
			request.form['adress'],
			request.form['phone']
        )
        User(*values).create()

        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = json.loads(request.data.decode('ascii'))
        username = data['username']
        password = data['password']
        user = User.find_by_username(username)
        #if not user or not user.verify_password(password):
        #    return jsonify({'token': None})
        #token = user.generate_token()
        #return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    app.run()
