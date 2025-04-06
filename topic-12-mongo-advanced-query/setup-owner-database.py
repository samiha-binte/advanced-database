from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint

uri = "mongodb+srv://greg:alabama@class-demo-cluster.gvxjh.mongodb.net/?appName=Class-Demo-Cluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
db = client.pets_db

def create_owners():
    owners_collection = db.owners
    # Drop the collection to start fresh
    owners_collection.drop()

    # Define about 10 owners with embedded pet records (≈30 pets total)
    owners = [
        {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "pets": [
                {"name": "Buddy", "age": 5, "kind": "Dog", "breed": "Golden Retriever"},
                {"name": "Whiskers", "age": 3, "kind": "Cat", "breed": "Siamese"},
                {"name": "Spike", "age": 2, "kind": "Dog", "breed": "Bulldog"},
            ],
        },
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "pets": [
                {"name": "Rex", "age": 2, "kind": "Dog", "breed": "German Shepherd"},
                {"name": "Fido", "age": 4, "kind": "Dog", "breed": "Beagle"},
                {"name": "Paws", "age": 1, "kind": "Cat", "breed": "Tabby"},
            ],
        },
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "pets": [
                {"name": "Mittens", "age": 3, "kind": "Cat", "breed": "Calico"},
                {"name": "Shadow", "age": 4, "kind": "Cat", "breed": "Black Cat"},
                {"name": "Fluffy", "age": 2, "kind": "Rabbit", "breed": "Angora"},
                {"name": "Bubbles", "age": 1, "kind": "Fish", "breed": "Goldfish"},
            ],
        },
        {
            "name": "Bob Brown",
            "email": "bob.brown@example.com",
            "pets": [
                {"name": "Chirpy", "age": 2, "kind": "Bird", "breed": "Parakeet"},
                {"name": "Buddy Jr", "age": 1, "kind": "Dog", "breed": "Labrador"},
            ],
        },
        {
            "name": "Carol White",
            "email": "carol.white@example.com",
            "pets": [
                {"name": "Daisy", "age": 3, "kind": "Dog", "breed": "Cocker Spaniel"},
                {"name": "Luna", "age": 2, "kind": "Cat", "breed": "Sphynx"},
                {"name": "Max", "age": 4, "kind": "Dog", "breed": "Boxer"},
            ],
        },
        {
            "name": "Dave Black",
            "email": "dave.black@example.com",
            "pets": [
                {"name": "Coco", "age": 2, "kind": "Parrot", "breed": "African Grey"},
                {"name": "Rocky", "age": 3, "kind": "Dog", "breed": "Pitbull"},
            ],
        },
        {
            "name": "Eva Green",
            "email": "eva.green@example.com",
            "pets": [
                {"name": "Simba", "age": 4, "kind": "Cat", "breed": "Maine Coon"},
                {"name": "Nala", "age": 3, "kind": "Cat", "breed": "Bengal"},
                {"name": "Zazu", "age": 1, "kind": "Bird", "breed": "Canary"},
            ],
        },
        {
            "name": "Frank Blue",
            "email": "frank.blue@example.com",
            "pets": [
                {"name": "Goldie", "age": 1, "kind": "Fish", "breed": "Betta"},
                {"name": "Buster", "age": 2, "kind": "Dog", "breed": "Dalmatian"},
                {"name": "Milo", "age": 3, "kind": "Cat", "breed": "Persian"},
            ],
        },
        {
            "name": "Grace Yellow",
            "email": "grace.yellow@example.com",
            "pets": [
                {"name": "Shadow", "age": 4, "kind": "Dog", "breed": "Rottweiler"},
                {"name": "Bella", "age": 2, "kind": "Cat", "breed": "Siamese"},
                {"name": "Lucy", "age": 3, "kind": "Dog", "breed": "Poodle"},
                {"name": "Duke", "age": 5, "kind": "Dog", "breed": "Bulldog"},
            ],
        },
        {
            "name": "Henry Purple",
            "email": "henry.purple@example.com",
            "pets": [
                {"name": "Oreo", "age": 2, "kind": "Cat", "breed": "Bombay"},
                {"name": "Buddy", "age": 3, "kind": "Dog", "breed": "Beagle"},
                {"name": "Sunny", "age": 1, "kind": "Dog", "breed": "Shiba Inu"},
            ],
        },
    ]

    # Insert the sample owners into the collection
    owners_collection.insert_many(owners)

    # Output the inserted documents for verification
    print("Inserted owners:")
    for owner in owners_collection.find():
        pprint(owner)


if __name__ == "__main__":
    create_owners()
    print("done.")
