from pymongo import MongoClient

uri = "mongodb+srv://greg:alabama@class-demo-cluster.gvxjh.mongodb.net/?appName=Class-Demo-Cluster"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.geospatial_demo
places = db.places

# Find places within ~1km of a point
results = places.find(
    {
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [-73.9855, 40.7580]},
                "$maxDistance": 1000,
            }
        }
    }
)

print("near point")
for place in results:
    print(place["name"])

results = places.find(
    {
        "location": {
            "$geoWithin": {
                "$box": [[-73.9855, 40.7580],[-74.9855, 41.7580]]
            },
        }
    }
)
print("in box")
for place in results:
    print(place["name"])
