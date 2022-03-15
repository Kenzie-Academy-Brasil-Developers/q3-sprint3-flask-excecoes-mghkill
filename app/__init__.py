from flask import Flask, jsonify, request
from http import HTTPStatus
import json

app = Flask(__name__)

FILEPATH = "./app/database/database.json"


from json import JSONDecodeError


def read_json(filepath: str) -> list:
    try:
        with open(filepath, "r") as json_file:
            return json.load(json_file)

    except (FileNotFoundError, JSONDecodeError):

        return {"data": []}



@app.get("/user")
def retrieve():

    return jsonify(read_json(FILEPATH)), HTTPStatus.OK


@app.post("/user")
def create():

    data = request.get_json()
    teste = type(data["nome"]).__name__
    print(teste)
    if (type(data["nome"]) != str) or (type(data["email"]) != str):

        return {"wrong fields": [{"nome": type(data["nome"]).__name__},{"email": type(data["email"]).__name__}]}, HTTPStatus.BAD_REQUEST

    json_list = read_json(FILEPATH)
    
    data["id"] = len(json_list["data"]) + 1

    for item in json_list["data"]:
        if data["email"] == item["email"]:
            return {"error": "User already exists."}, HTTPStatus.CONFLICT
        
    json_list["data"].append(data)


    with open(FILEPATH, "w") as json_file:
        json.dump(json_list, json_file, indent=2)
        
        return {"data": data}, HTTPStatus.CREATED

    