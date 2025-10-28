import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

posts = {
    1 : {"id":0,"upvotes":3,"title":"My first post!","link":"https://i.imgur.com/jseZqNK.jpg",
         "username":"Ciscognito16"}
}
post_counter = 1

# your routes here
@app.route("/api/posts/",methods="GET")
def get_all_posts():
    """
    Get all posts
    """
    res = {"posts":list(posts.values())}
    return json.dumps(res),200

@app.route("/api/posts/",methods="POST")
def create_post():
    """
    Create a new post with fields "title", "link", "username" provided by the client
    """
    global post_counter
    body = json.loads(request.data)
    title = body["title"]
    link = body["link"]
    username = body["username"]
    if not title or not link or not username:
        return json.dumps({"error":"Fields missing"}),400
    
    post = {"id": post_counter, "title":title,"link":link,"username":username}
    posts[post_counter] = post
    post_counter += 1
    return json.dumps(post),201

@app.route("/api/posts/<int:post_id>",methods="GET")
def get_post_by_id(post_id):
    """
    Get post by id. If post doesn't exist, then return error code 404.
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error":"Invalid id"}),404
    
    return json.dumps(post),200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
