from pymongo import MongoClient
from collections import defaultdict

client = MongoClient()
db = client.geospatial_demo
places = db.places
zones = db.zones

zone_place_map = defaultdict(list)

# Build a list of zones with names and geometry
zone_defs = list(zones.find())

for place in places.find():
    point = place["location"]
    matched = None
    for zone in zone_defs:
        if db.zones.find_one({
            "_id": zone["_id"],
            "area": {
                "$geoIntersects": {
                    "$geometry": point
                }
            }
        }):
            matched = zone["zone"]
            zone_place_map[matched].append(place["name"])
            break

print("Places grouped by zone:")
for zone in sorted(zone_place_map.keys()):
    print(f"\nZone: {zone}")
    for name in sorted(zone_place_map[zone]):
        print(f"  - {name}")
