import json

from flask import Flask
from flask import jsonify
from flask import request
from urllib.parse import urlparse

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


posts = {
    0 : {"id":0,"upvotes":3,"title":"My first post!","link":"https://i.imgur.com/jseZqNK.jpg",
         "username":"Ciscognito16"}
}
post_counter = 1

comments = {
    0 : {
        0:{"id":0,"upvotes":3,"text":"Wow, my frist Reddit gold!","username":"alicia98"}
    }
}
comment_counter = 1



# your routes here
@app.route("/api/posts/",methods=["GET"])
def get_all_posts():
    """
    Get all posts
    """
    res = {"posts":list(posts.values())}
    return json.dumps(res),200


@app.route("/api/posts/",methods=["POST"])
def create_post():
    """
    Create a new post with fields "title", "link", "username" provided by the client
    """
    global post_counter
    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")
    if not title or not link or not username:
        return json.dumps({"error":"Fields missing"}),400
    
    post_counter += 1
    post = {"id": post_counter-1, "upvotes":1,"title":title,"link":link,"username":username}
    
    posts[post_counter-1] = post
    return json.dumps(post),201


@app.route("/api/posts/<int:post_id>/",methods=["GET"])
def get_post_by_id(post_id):
    """
    Get post by id. If post doesn't exist, then return error code 404.
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error":"Invalid id"}),404
    
    return json.dumps(post),200


@app.route("/api/posts/<int:post_id>/",methods=["DELETE"])
def delete_post(post_id):
    """
    Delete post by id.
    """
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error":"Invalid id"}),404
    
    del posts[post_id]
    return json.dumps(post),200



@app.route("/api/posts/<int:post_id>/comments/",methods=["GET"])
def get_comments_of_post(post_id):
    """
    Get comments of a post by post_id
    """
    post_comments = comments.get(post_id)
    if not post_comments:
        return json.dumps({"error":"Invalid id"}),404
    res = {"comments":list(post_comments.values())}

    return json.dumps(res),200


@app.route("/api/posts/<int:post_id>/comments/",methods=["POST"])
def post_comment(post_id):
    """
    Post comment on post_id. It must have text and username.
    """
    global comment_counter
    body = json.loads(request.data)
    post = posts.get(post_id)

    if not post:
        return json.dumps({"error":"Invalid post id."}),404

    text = body.get("text")
    username = body.get("username")
    if not text or not username:
        return json.dumps({"error":"Missing text or username on comment."}),400
    comment_counter += 1
    new_comment = {"id":comment_counter-1,"upvotes":0,"text":text,"username":username}


    comments.setdefault(post_id,{})
    comments[post_id][comment_counter-1] = new_comment

    return json.dumps(new_comment),201


@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/",methods=["POST"])
def edit_comment(post_id,comment_id):
    """
    Edit comment_id on post_id by the same user. It must have text.
    """
    body = json.loads(request.data)
    post_commented = comments.get(post_id)
    if not post_commented:
        return json.dumps({"error":"Post has no current comments."}),400
    
    comment = post_commented.get(comment_id)
    if not post_commented:
        return json.dumps({"error":"Invalid comment id."}),400

    text = body.get("text")
    if not text:
        return json.dumps({"error":"Missing text."}),400
    
    comments[post_id][comment_id]["text"] = text

    return json.dumps(comments[post_id][comment_id]),200

#Challenge section
@app.route("/api/extra/posts/",methods=["POST"])
def create_post_extra():
    """
    Create a new post with fields "title", "link", "username" provided by the client
    """
    global post_counter
    body = json.loads(request.data)
    title = body.get("title")
    if not isinstance(title,str):
        return json.dumps({"error":"title must be a string."}),400

    link = body.get("link")
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return result.scheme in ("http", "https") and bool(result.netloc)
        except:
            return False

    if not isinstance(link,str) or not is_valid_url(link):
        return json.dumps({"error":"title must be a string."}),400
    
    username = body.get("username")
    if not isinstance(username,str):
        return json.dumps({"error":"Username must be a string"}),400
    
    post_counter += 1
    post = {"id": post_counter-1, "upvotes":1,"title":title,"link":link,"username":username}
    
    posts[post_counter-1] = post
    return json.dumps(post),201
    
@app.route("/api/extra/posts/<int:post_id>/comments/",methods=["POST"])
def post_comment_extra(post_id):
    """
    Post comment on post_id. It must have text and username.
    """
    global comment_counter
    body = json.loads(request.data)
    post = posts.get(post_id)

    if not post:
        return json.dumps({"error":"Invalid post id."}),404

    text = body.get("text")
    username = body.get("username")
    if not isinstance(text,str) or not isinstance(username,str):
        return json.dumps({"error":"Text and username must be strings."}),400
    comment_counter += 1
    new_comment = {"id":comment_counter-1,"upvotes":0,"text":text,"username":username}


    comments.setdefault(post_id,{})
    comments[post_id][comment_counter-1] = new_comment

    return json.dumps(new_comment),201


@app.route("/api/extra/posts/<int:post_id>/comments/<int:comment_id>/",methods=["POST"])
def edit_comment_extra(post_id,comment_id):
    """
    Edit comment_id on post_id by the same user. It must have text.
    """
    body = json.loads(request.data)
    post_commented = comments.get(post_id)
    if not post_commented:
        return json.dumps({"error":"Post has no current comments."}),400
    
    comment = post_commented.get(comment_id)
    if not post_commented:
        return json.dumps({"error":"Invalid comment id."}),400

    text = body.get("text")
    if not isinstance(text,str):
        return json.dumps({"error":"Text must be a string."}),400
    
    comments[post_id][comment_id]["text"] = text

    return json.dumps(comments[post_id][comment_id]),200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
