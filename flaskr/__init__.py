from flask import Flask
import os

def create_app(config_name):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["FILES_FOLDER"] = '../tareas/files'
    app.config["REDIS_INSTANCE_IP"] = '34.138.239.130'
    return app