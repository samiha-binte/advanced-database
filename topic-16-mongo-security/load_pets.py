from pymongo import MongoClient

def main():
    # 1. Connect
    client = MongoClient("mongodb://localhost:27017/")
    db = client.my_database
    types = db.types
    pets = db.pets

    # 2. Define your types metadata
    sample_types = [
        {"_id": "dog",    "food": "kibble",  "noise": "bark", "size": "medium"},
        {"_id": "cat",    "food": "tuna",    "noise": "meow", "size": "small"},
        {"_id": "fish",   "food": "flakes",  "noise": "—",    "size": "tiny"},
        {"_id": "parrot", "food": "seeds",   "noise": "squawk","size": "small"},
    ]

    # 3. Drop & re‐create collections
    types.drop()
    pets.drop()

    # 4. Insert types and pets
    types.insert_many(sample_types)
    sample_pets = [
        {"name": "Fido",     "type": "dog",    "age": 3, "owner": "Alice"},
        {"name": "Whiskers", "type": "cat",    "age": 2, "owner": "Bob"},
        {"name": "Goldie",   "type": "fish",   "age": 1, "owner": "Carol"},
        {"name": "Polly",    "type": "parrot", "age": 5, "owner": "Dan"},
    ]
    pets.insert_many(sample_pets)

    # 5. Aggregate pets with their type info
    for doc in pets.aggregate([
        {
            "$lookup": {
                "from": "types",           # the metadata collection
                "localField": "type",      # pets.type
                "foreignField": "_id",     # types._id
                "as": "type_info"
            }
        },
        {"$unwind": "$type_info"}        # turn type_info array into a sub‐document
    ]):
        ti = doc["type_info"]
        print(
            f"{doc['name']} (a {doc['type']}, age {doc['age']}, owner {doc['owner']}):\n"
            f"  • Eats: {ti['food']}\n"
            f"  • Noise: {ti['noise']}\n"
            f"  • Size: {ti['size']}\n"
        )

if __name__ == "__main__":
    main()
    