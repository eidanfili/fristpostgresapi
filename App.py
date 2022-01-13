from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy 
from marshmallow import Schema, fields


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:admin2003@localhost/firstpgdb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class Friends(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255), primary_key = False)
    description = db.Column(db.Text(), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self): 
        db.session.delete(self)
        db.session.commit()
        
class FriendsSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()



@app.route("/friends", methods=["GET"])
def get_all_friends():
    all_friends = Friends.get_all()

    serializer = FriendsSchema(many=True)

    data = serializer.dump(all_friends)
    return jsonify(data)

@app.route("/friends/add", methods=["POST"])
def add_friend():
    name = request.json.get("name")
    description = request.json.get("description")

    new_friend = Friends(name, description)
    new_friend.save()
    serializer = FriendsSchema()

    data = serializer.dump(new_friend)

    return jsonify(data)

@app.route("/friends/<id>", methods=["GET"])
def get_friend_by_id(id):
    friend = Friends.get_by_id(id)

    serializer = FriendsSchema()

    data = serializer.dump(friend)

    return jsonify(data)

@app.route("/friends/update/<id>", methods=["PUT"])
def update_friend(id):
    friend = Friends.get_by_id(id)

    data = request.get_json()
    
    friend.name = data.get('name')
    friend.description = data.get('description')

    db.session.commit()
    
    serializer = FriendsSchema()

    friend_data = serializer.dump(friend)

    return jsonify(friend_data)


    

@app.route("/friends/delete/<id>", methods=["DELETE"])
def remove_friend(id):
    friend = Friends.get_by_id(id)

    friend.delete()

    return jsonify({"Message": "Deleted"})


@app.errorhandler(404)
def internal_server(error):
    return jsonify({"Message": "RESOURCE NOT FOUND!"}),404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"Message": "ERROR FOUND!"}),500

if __name__ == "__main__":
    app.run(debug=True)


# postgress_app_env\Scripts\activate.bat <------ scripts for venv