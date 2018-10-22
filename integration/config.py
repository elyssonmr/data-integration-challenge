from decouple import config


MONGO_URI = config("MONGO_URI", default="mongodb://mongo:27017")
