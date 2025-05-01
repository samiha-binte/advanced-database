from pymongo import MongoClient

client = MongoClient()
db = client.geospatial_demo
zones = db.zones
zones.drop()

zone_data = [
    {
        "zone": "Manhattan",
        "area": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -74.025,
                        40.7
                    ],
                    [
                        -73.925,
                        40.7
                    ],
                    [
                        -73.925,
                        40.88
                    ],
                    [
                        -74.025,
                        40.88
                    ],
                    [
                        -74.025,
                        40.7
                    ]
                ]
            ]
        }
    },
    {
        "zone": "Uptown",
        "area": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -74.0,
                        40.82
                    ],
                    [
                        -73.94,
                        40.82
                    ],
                    [
                        -73.94,
                        40.88
                    ],
                    [
                        -74.0,
                        40.88
                    ],
                    [
                        -74.0,
                        40.82
                    ]
                ]
            ]
        }
    },
    {
        "zone": "Downtown",
        "area": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -74.02,
                        40.7
                    ],
                    [
                        -73.97,
                        40.7
                    ],
                    [
                        -73.97,
                        40.74
                    ],
                    [
                        -74.02,
                        40.74
                    ],
                    [
                        -74.02,
                        40.7
                    ]
                ]
            ]
        }
    },
    {
        "zone": "Brooklyn",
        "area": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -74.04,
                        40.57
                    ],
                    [
                        -73.85,
                        40.57
                    ],
                    [
                        -73.85,
                        40.7
                    ],
                    [
                        -74.04,
                        40.7
                    ],
                    [
                        -74.04,
                        40.57
                    ]
                ]
            ]
        }
    },
    {
        "zone": "Bronx",
        "area": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -73.935,
                        40.8
                    ],
                    [
                        -73.82,
                        40.8
                    ],
                    [
                        -73.82,
                        40.92
                    ],
                    [
                        -73.935,
                        40.92
                    ],
                    [
                        -73.935,
                        40.8
                    ]
                ]
            ]
        }
    }
]

zones.insert_many(zone_data)
zones.create_index([("area", "2dsphere")])
print("Zones loaded and indexed.")
