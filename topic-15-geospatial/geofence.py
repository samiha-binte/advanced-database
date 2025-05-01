from pymongo import MongoClient

client = MongoClient()
db = client.geospatial_demo
zones = db.zones  # stores polygon boundaries

def in_zone(lat, lon):
    match = zones.find_one({
        "area": {
            "$geoIntersects": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            }
        }
    })
    return match["zone"] if match else None

if __name__ == "__main__":
    zone_name = in_zone(40.76, -73.98)
    if zone_name:
        print(f"✔ Inside zone: {zone_name}")
    else:
        print("✘ Outside all zones")
