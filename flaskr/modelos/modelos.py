from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from enum import Enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    conversion_tasks = db.relationship(
        "ConversionTask", cascade="all, delete, delete-orphan"
    )


class TaskStatus(Enum):
    UPLOADED = 1
    PROCESSED = 2


class TaskFormats(Enum):
    MP3 = "mp3"
    OGG = "ogg"
    WMA = "wma"


class ConversionTask(db.Model):
    __tablename__ = "conversion_task"
    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.UPLOADED)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    original_file_name = db.Column(db.String(150), nullable=False)
    new_file_name = db.Column(db.String(150), nullable=True)
    new_file_format = db.Column(db.String(150), nullable=False)

class Enum2Dict(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.name

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        includde_relationships = True
        load_instance = True


class ConversionTaskSchema(SQLAlchemyAutoSchema):
    status = Enum2Dict(attribute=("status"))
    #new_file_format = Enum2Dict(attribute=("new_file_format"))
    class Meta:
        model = ConversionTask
        includde_relationships = True
        load_instance = True
