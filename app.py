from flask import Flask, jsonify, request

app = Flask(__name__)
user_data = [
    {
        "user_id": 123,
        "user_name": "testing",
        "email": "user1@example.com",
        "nested_data": [
            {"hobby": "reading"},
            {"fave_food": "pizza"},
            {"sport": "basketball"}
        ]
    },
    {
        "user_id": 23,
        "user_name": "magic",
        "email": "user2@example.com",
        "nested_data": [
            {"hobby": "magic tricks"},
            {"fave_food": "sushi"},
            {"sport": "soccer"}
        ]
    },
    {
        "user_id": 3,
        "user_name": "wow",
        "email": "user1@example.com",
        "nested_data": [
            {"hobby": "painting"},
            {"hobby": "painting"},
            {"hobby": "painting"},
            {"fave_food": "pasta"},
            {"sport": "tennis"},
            {"sport": "tennis"},
            {"sport": "tennis"}
        ]
    },
    {
        "user_id": 31,
        "user_name": "ah wla ni",
        "email": "user1@example.com",
        "nested_data": [
            {"hobby": "cooking"},
            {"fave_food": "burgers"},
            {"sport": "volleyball"}
        ]
    },
    {
        "user_id": 13,
        "user_name": "wow",
        "email": "user1@example.com",
        "nested_data": [
            {"hobby": "dancing"},
            {"fave_food": "steak"},
            {"sport": "swimming"}
        ]
    },
    {
        "user_id": 2,
        "user_name": "user1",
        "email": "user1@example.com",
        "nested_data": [
            {"hobby": "writing"},
            {"fave_food": "salad"},
            {"sport": "chess"}
        ]
    }
]

@app.route("/", methods=["GET"])
def getAll():
    return jsonify(user_data)


@app.route("/users/<string:name>", methods=["GET"])
def getFromName(name):
    user = next((user for user in user_data if user["user_name"]==name),None)
    if not user:
        return jsonify("user not found"),404
    return jsonify(user),200


@app.route("/users/<string:name>/nested_data", methods=["GET"])
def getFromNested(name):
    user = next((user for user in user_data if user["user_name"]==name),None)
    if not user:
        return jsonify("user not found"),404
    data = user.get("nested_data",[])
    return jsonify(data),200


@app.route("/users/<string:name>/nested_data/hobbies", methods=["GET"])
def getFromNestedHobbies(name):
    user = next((user for user in user_data if user["user_name"]==name),None)
    if not user:
        return jsonify("user not found"),404
    data = user.get("nested_data",[])
    hobby=[]
    for item in data:
        if "hobby" in item:
            new_data={
                'hobby': item["hobby"]
            }
            hobby.append(new_data)
    return jsonify(hobby),200

@app.route("/users/<string:name>/nested_data/sport", methods=["GET"])
def getFromNestedSport(name):
    user = next((user for user in user_data if user["user_name"]==name),None)
    if not user:
        return jsonify("user not found"),404
    data = user.get("nested_data",[])
    hobby=[]
    for item in data:
        if "sport" in item:
            new_data={
                'sport': item["sport"]
            }
            hobby.append(new_data)
    return jsonify(hobby),200


@app.route("/users/<int:id>", methods=["DELETE","PATCH","GET"])
def usersRoute(id):
    user = next((user for user in user_data if user["user_id"]==id),None)
    if not user:
        return jsonify("user not found"),404
    if request.method == "DELETE":
            user_data.remove(user)
            return jsonify("user successfully delete"),200
    if request.method == "GET":
            return jsonify(user),200
    if request.method == "PATCH":
         if not request.is_json:
              return jsonify("json data required"),400
         update = request.get_json()
         if "user_name" in update:
              user["user_name"]=update["user_name"]
              return jsonify("user_name update success"),200
         if "email" in update:
              user["email"]=update["email"]
              return jsonify("email update success"),200
         if "nested_data" in update:
              nest = user.get("nested_data")
              nest["nested_data"]=update["nested_data"]
              return jsonify("nested update success"),200
         return jsonify("error fields are not seen"),400

@app.route("/users/addNew", methods=["POST"])
def addNew():
    if not request.is_json:
        return jsonify("json data required"),400
    data = request.get_json()
    if "user_name" not in data or "email" not in data or "nested_data" not in data:
         return jsonify("required fields [username, email, nested data]"),400  
    userID = max(user["user_id"] for user in user_data)+1
    data["user_id"] = userID
    user_data.append(data)
    return jsonify("user added successfully"),201
         
if __name__ == "__main__":
    app.run(debug=True,port=5001)