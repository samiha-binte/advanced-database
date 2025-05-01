from flask import Flask, render_template, request, redirect, url_for
import social_database as db  # Our database layer module

app = Flask(__name__)


# Route to display the social media feed with posts.
@app.route("/")
@app.route("/feed")
def feed():
    posts = db.retrieve_posts()
    return render_template("feed.html", posts=posts)


# Route to create a new post.
@app.route("/post/create", methods=["GET", "POST"])
def post_create():
    if request.method == "GET":
        return render_template("post_create.html")
    elif request.method == "POST":
        data = {
            "author": {
                "userId": "user1",  # This could be replaced by the authenticated user id.
                "username": request.form.get("username", "anonymous"),
            },
            "content": request.form.get("content"),
            "tags": [
                tag.strip()
                for tag in request.form.get("tags", "").split(",")
                if tag.strip()
            ],
        }
        db.create_post(data)
        return redirect(url_for("feed"))


# Route to show details of a single post along with its comments.
@app.route("/post/<post_id>")
def post_detail(post_id):
    post = db.retrieve_post(post_id)
    if post is None:
        return "Post not found", 404
    # Retrieve top-level comments.
    comments = db.retrieve_comments_for_post(post_id)
    return render_template("post_detail.html", post=post, comments=comments)


# Route to update an existing post.
@app.route("/post/update/<post_id>", methods=["GET", "POST"])
def post_update(post_id):
    if request.method == "GET":
        post = db.retrieve_post(post_id)
        return render_template("post_update.html", post=post)
    elif request.method == "POST":
        data = {
            "content": request.form.get("content"),
            "tags": [
                tag.strip()
                for tag in request.form.get("tags", "").split(",")
                if tag.strip()
            ],
        }
        db.update_post(post_id, data)
        return redirect(url_for("post_detail", post_id=post_id))


# Route to delete a post.
@app.route("/post/delete/<post_id>")
def post_delete(post_id):
    db.delete_post(post_id)
    return redirect(url_for("feed"))


# Route to add a comment to a post.
@app.route("/comment/create", methods=["POST"])
def comment_create():
    post_id = request.form.get("post_id")
    data = {
        "postId": post_id,
        "parentCommentId": request.form.get("parent_comment_id", None),
        "author": {
            "userId": "user1",  # Replace with actual authenticated user info.
            "username": request.form.get("username", "anonymous"),
        },
        "content": request.form.get("content"),
    }
    db.create_comment(data)
    return redirect(url_for("post_detail", post_id=post_id))


# Route to delete a comment.
@app.route("/comment/delete/<comment_id>")
def comment_delete(comment_id):
    # Assume a query parameter "post_id" is passed to redirect back to the right post.
    post_id = request.args.get("post_id")
    db.delete_comment(comment_id)
    return redirect(url_for("post_detail", post_id=post_id))


if __name__ == "__main__":
    app.run(debug=True)
