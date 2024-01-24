from pymongo.mongo_client import MongoClient 
from flask import Flask, jsonify, request 
from flask_basicauth import BasicAuth 
 
uri = "mongodb+srv://sirikul:tt1100703512533@cluster0.sg4o3dw.mongodb.net/retryWrites=true&w=majority" 
 
client = MongoClient(uri) 
db = client["studentss"] 
collection = db["stdd_info"] 
 
app = Flask(__name__) 
 
app.config['BASIC_AUTH_USERNAME'] = "vieweruser" 
app.config['BASIC_AUTH_PASSWORD'] = "viewerpass" 
basic_auth = BasicAuth(app) 
 
@app.route("/") 
def Greet(): 
    return "<p>Welcome to Student Management API</p>" 
 
@app.route("/students", methods = ["GET"]) 
@basic_auth.required 
def get_all_students(): 
    all_students = collection.find() 
    return jsonify({"students":[i for i in all_students]}) 
 
@app.route("/students/<int:std_id>", methods = ["GET"]) 
@basic_auth.required 
def get_student(std_id): 
    all_students = collection.find() 
    student = next( (i for i in all_students if i["_id"] == std_id), None) 
    if student: 
        return jsonify(student) 
    else: 
        return jsonify({"error": "Student not found"}), 404 
     
@app.route("/students", methods = ["POST"]) 
@basic_auth.required 
def create_students(): 
    try: 
        data = request.get_json() 
        new_student = { 
            "_id": data["id"], 
            "fullname": data["fullname"], 
            "major": data["major"], 
            "gpa": data["gpa"] 
        } 
        collection.insert_one(new_student) 
        return jsonify(new_student), 200 
    except Exception as e: 
        return jsonify({"error":"Cannot create new student"}), 500 
     
@app.route("/students/<int:std_id>", methods = ["PUT"]) 
@basic_auth.required 
def update_student(std_id): 
    all_students = collection.find() 
    student = next( (i for i in all_students if i["_id"] == std_id), None) 
    if student: 
        data = request.get_json() 
        collection.update_one({"_id": std_id}, {"$set": data}) 
        return jsonify(student), 200 
    else: 
        return jsonify({"error": "Student not found"}), 404 
 
@app.route("/students/<int:std_id>", methods = ["DELETE"]) 
@basic_auth.required 
def delete_student(std_id): 
    all_students = collection.find() 
    student = next( (i for i in all_students if i["_id"] == std_id), None) 
    if student: 
        collection.delete_one({"_id": std_id}) 
        return jsonify({"message": "Student deleted successfully"}), 200 
    else: 
        return jsonify({"error": "Student not found"}), 404 
 
if __name__=="__main__": 
    app.run(host = "0.0.0.0", port = 5000, debug = True)