import os
from flask import Flask, session
from dotenv import load_dotenv
from pymongo import MongoClient

from todoApp.routes import pages

load_dotenv()


# def create_app():
app = Flask(__name__)
# app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
app.config["MONGODB_URI"] = "mongodb://localhost:27017/todo-app-flask"
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
)
app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()

app.register_blueprint(pages)
# session["theme"]="light"
# return app

if __name__ == '__main__':
    app.run(debug=True)