from pymongo import MongoClient, GEOSPHERE
import json


# uri = "mongodb+srv://greg:alabama@class-demo-cluster.gvxjh.mongodb.net/?appName=Class-Demo-Cluster"

# Create a new client and connect to the server
client = MongoClient()

db = client.geospatial_demo
places = db.places
places.drop()

with open("geo_locations.json") as f:
    data = json.load(f)
    places.insert_many(data)

places.create_index([("location", GEOSPHERE)])
print("Inserted and indexed locations.")
