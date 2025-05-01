from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import datetime
import random

# Replace with your actual connection string
uri = "mongodb+srv://greg:alabama@class-demo-cluster.gvxjh.mongodb.net/?appName=Class-Demo-Cluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))


def create_database():
    social_db = client.social_media

    # Drop existing collections for a clean setup.
    social_db.drop_collection("posts")
    social_db.drop_collection("comments")

    posts_collection = social_db.posts
    comments_collection = social_db.comments

    # List of dozens of authors
    authors = [
        {"userId": "u1", "username": "alice"},
        {"userId": "u2", "username": "bob"},
        {"userId": "u3", "username": "carol"},
        {"userId": "u4", "username": "dave"},
        {"userId": "u5", "username": "eve"},
        {"userId": "u6", "username": "frank"},
        {"userId": "u7", "username": "grace"},
        {"userId": "u8", "username": "heidi"},
        {"userId": "u9", "username": "ivan"},
        {"userId": "u10", "username": "judy"},
        {"userId": "u11", "username": "mallory"},
        {"userId": "u12", "username": "oscar"},
        {"userId": "u13", "username": "peggy"},
        {"userId": "u14", "username": "trent"},
        {"userId": "u15", "username": "victor"},
        {"userId": "u16", "username": "walter"},
        {"userId": "u17", "username": "sybil"},
        {"userId": "u18", "username": "zara"},
        {"userId": "u19", "username": "yasmin"},
        {"userId": "u20", "username": "xander"},
    ]

    # Sample post contents
    post_texts = [
        "Today was a great day! Feeling happy and blessed.",
        "Just finished a fantastic project at work.",
        "Looking forward to the weekend. Any plans?",
        "I just read an amazing book on history.",
        "Anyone up for a game of chess?",
        "Learning Python is fun and challenging.",
        "Enjoying a delicious cup of coffee.",
        "The weather is perfect for a hike.",
        "Just got a new pet. So excited!",
        "Cooking a new recipe today. Wish me luck!",
        "Watching the sunset is the best part of my day.",
        "Feeling a bit under the weather today.",
        "Had a long day at work, time to relax.",
        "Traveling is my passion. Can’t wait for my next trip!",
        "Just saw a great movie at the theater.",
    ]

    # Sample tags
    sample_tags = [
        "life",
        "daily",
        "fun",
        "travel",
        "food",
        "tech",
        "mood",
        "books",
        "music",
    ]

    number_of_posts = 50
    for _ in range(number_of_posts):
        # Choose a random author and content for each post
        author = random.choice(authors)
        post_content = random.choice(post_texts)
        # Create a random time within the last 30 days.
        created_at = datetime.datetime.utcnow() - datetime.timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        # Random tags: select between 1 and 3 tags
        tags = random.sample(sample_tags, random.randint(1, 3))

        post_data = {
            "author": author,
            "content": post_content,
            "createdAt": created_at,
            "tags": tags,
            "likes": [],
        }
        post_result = posts_collection.insert_one(post_data)
        post_id = post_result.inserted_id

        # Insert a random number of top-level comments (between 2 and 10) for this post.
        number_of_comments = random.randint(2, 10)
        for _ in range(number_of_comments):
            comment_author = random.choice(authors)
            comment_texts = [
                "Great post!",
                "I totally agree.",
                "Thanks for sharing!",
                "Interesting perspective.",
                "Could you elaborate?",
                "This made my day.",
                "Nice thoughts!",
                "Well said!",
            ]
            comment_text = random.choice(comment_texts)
            # Generate a comment timestamp after the post's creation
            comment_created = created_at + datetime.timedelta(
                hours=random.randint(0, 72)
            )
            comment_data = {
                "postId": post_id,
                "parentCommentId": None,
                "author": comment_author,
                "content": comment_text,
                "createdAt": comment_created,
            }
            comment_result = comments_collection.insert_one(comment_data)
            comment_id = comment_result.inserted_id

            # Insert a random number (0-3) of replies to this comment.
            number_of_replies = random.randint(0, 3)
            for _ in range(number_of_replies):
                reply_author = random.choice(authors)
                reply_texts = [
                    "I agree with you.",
                    "That's interesting.",
                    "Good point!",
                    "Could you clarify?",
                    "Absolutely!",
                    "I had a similar experience.",
                ]
                reply_text = random.choice(reply_texts)
                reply_created = comment_created + datetime.timedelta(
                    hours=random.randint(0, 48)
                )
                reply_data = {
                    "postId": post_id,
                    "parentCommentId": comment_id,
                    "author": reply_author,
                    "content": reply_text,
                    "createdAt": reply_created,
                }
                comments_collection.insert_one(reply_data)

    print(
        "Inserted {} posts along with their comments and replies.".format(
            number_of_posts
        )
    )


if __name__ == "__main__":
    create_database()
    print("Database created and populated successfully.")
