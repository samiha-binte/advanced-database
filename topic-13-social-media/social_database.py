import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# Change this URI to your MongoDB Atlas cluster connection string.
uri = "mongodb+srv://greg:alabama@class-demo-cluster.gvxjh.mongodb.net/?appName=Class-Demo-Cluster"

# Create a new MongoClient and select our database.
client = MongoClient(uri, server_api=ServerApi("1"))
social_db = client.social_media


def ensure_indexes():
    posts_collection = social_db.posts
    comments_collection = social_db.comments

    # Posts indexes (adjust fields as needed)
    posts_collection.create_index("author.username")
    posts_collection.create_index("createdAt")

    # Comments indexes to improve lookup performance
    comments_collection.create_index("postId")
    comments_collection.create_index("parentCommentId")
    comments_collection.create_index("createdAt")


# Ensure the indexes are created on module load.
ensure_indexes()

# POSTS


def retrieve_posts():
    """Retrieve all posts."""
    posts_collection = social_db.posts
    posts = list(posts_collection.find().sort("createdAt", -1))
    for post in posts:
        post["id"] = str(post["_id"])
        del post["_id"]
    return posts


def retrieve_post(post_id):
    """Retrieve a single post by its id."""
    posts_collection = social_db.posts
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post:
        post["id"] = str(post["_id"])
        del post["_id"]
    return post


def create_post(data):
    """Create a new post."""
    posts_collection = social_db.posts
    data["createdAt"] = datetime.datetime.utcnow()
    # Ensure likes and tags are in place
    data.setdefault("likes", [])
    data.setdefault("tags", [])
    posts_collection.insert_one(data)


def update_post(post_id, data):
    """Update an existing post."""
    posts_collection = social_db.posts
    posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": data})


def delete_post(post_id):
    """Delete a post."""
    posts_collection = social_db.posts
    posts_collection.delete_one({"_id": ObjectId(post_id)})


# COMMENTS


def retrieve_comments_for_post(post_id, parent_comment_id=None):
    """Retrieve comments for a given post.

    If parent_comment_id is None, returns top-level comments.
    Otherwise, returns replies to the given comment.
    """
    comments_collection = social_db.comments
    query = {"postId": ObjectId(post_id)}
    if parent_comment_id is None:
        query["parentCommentId"] = None
    else:
        query["parentCommentId"] = ObjectId(parent_comment_id)
    comments = list(comments_collection.find(query).sort("createdAt", 1))
    for comment in comments:
        comment["id"] = str(comment["_id"])
        del comment["_id"]
    return comments


def create_comment(data):
    """Create a new comment on a post or as a reply to another comment."""
    comments_collection = social_db.comments
    # Ensure postId and (optionally) parentCommentId are ObjectIds.
    data["postId"] = ObjectId(data["postId"])
    if data.get("parentCommentId"):
        data["parentCommentId"] = ObjectId(data["parentCommentId"])
    else:
        data["parentCommentId"] = None
    data["createdAt"] = datetime.datetime.utcnow()
    comments_collection.insert_one(data)


def update_comment(comment_id, data):
    """Update an existing comment."""
    comments_collection = social_db.comments
    if "postId" in data:
        data["postId"] = ObjectId(data["postId"])
    if "parentCommentId" in data:
        if data["parentCommentId"]:
            data["parentCommentId"] = ObjectId(data["parentCommentId"])
        else:
            data["parentCommentId"] = None
    comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": data})


def delete_comment(comment_id):
    """Delete a comment."""
    comments_collection = social_db.comments
    comments_collection.delete_one({"_id": ObjectId(comment_id)})
