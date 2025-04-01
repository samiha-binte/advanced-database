from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint

uri = "mongodb+srv://greg:alabama@class-demo-cluster.gvxjh.mongodb.net/?appName=Class-Demo-Cluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
db = client.pets_db

def count_dogs_1():
    owners_collection = db.owners
    owners = list(owners_collection.find({}))
    dog_count = 0

    for owner in owners:
        pets = owner.get("pets", [])
        for pet in pets:
            if pet.get("kind") == "Dog":
                dog_count += 1

    print("Total number of dogs:", dog_count)

def list_dogs_1():
    owners_collection = db.owners
    owners = list(owners_collection.find({}))

    all_dogs = []
    for owner in owners:
        pets = owner.get("pets", [])
        for pet in pets:
            if pet.get("kind") == "Dog":
                all_dogs.append(pet)

    print("All dogs:", all_dogs)


def count_dogs_2():
    owners_collection = db.owners
    owners = list(owners_collection.find({}))
    dog_count = sum(
        1 for owner in owners 
            for pet in owner.get("pets", []) 
            if pet.get("kind") == "Dog"
    )
    print("Total number of dogs:", dog_count)

def list_dogs_2():
    owners_collection = db.owners
    owners = list(owners_collection.find({}))
    all_dogs = [
        pet for owner in owners 
            for pet in owner.get("pets", []) 
            if pet.get("kind") == "Dog"
    ]
    print("All Dogs:", all_dogs)

"""
db.owners.aggregate([
  { $unwind: "$pets" },
  { $replaceRoot: { newRoot: "$pets" } }
])

db.owners.aggregate([
  { $unwind: "$pets" },
  { $match: { "pets.kind": "Dog" } },
  { $replaceRoot: { newRoot: "$pets" } }
])

db.owners.aggregate([
  { $unwind: "$pets" },
  { $match: { "pets.kind": "Dog" } },
  { $count: "dogCount" }])

"""

def list_dogs_3():
    owners_collection = db.owners
    pipeline = [
        {"$unwind": "$pets"},
        {"$match": {"pets.kind": "Dog"}},
        {"$replaceRoot": {"newRoot": "$pets"}},
    ]
    dogs = list(owners_collection.aggregate(pipeline))
    print("\nAll dogs:")
    for dog in dogs:
        pprint(dog)


def count_dogs_3():
    owners_collection = db.owners
    pipeline = [
        {"$unwind": "$pets"},
        {"$match": {"pets.kind": "Dog"}},
        {"$count": "dogCount" },
    ]
    result = list(owners_collection.aggregate(pipeline))
    dog_count = result[0]["dogCount"] if result else 0
    print(f"\nTotal number of dogs: {dog_count}")

if __name__ == "__main__":
    count_dogs_3()
    list_dogs_3()
