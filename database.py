from pymongo import MongoClient

client = MongoClient("mongo")
db = client['db']
video_db = db['videos']