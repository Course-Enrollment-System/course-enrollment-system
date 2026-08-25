from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

database = client["course_enrollment"]

students_collection = database["students"]