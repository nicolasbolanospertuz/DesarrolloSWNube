from flask_restful import Resource
from flask import request, current_app, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from ..modelos import db, User, UserSchema, ConversionTask, ConversionTaskSchema, TaskStatus
from werkzeug.utils import secure_filename
from celery import Celery
import os

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

user_schema = UserSchema()
conversion_task_schema = ConversionTaskSchema()

@celery_app.task(name='convert_file')
def convert_file(*args):
    pass

class SignUpView(Resource):
    def post(self):
        new_user = User(
            username=request.json["username"],
            email=request.json["email"],
            password=request.json["password"],
        )
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user.id)
        return {
            "mensaje": "User created successfully",
            "token": access_token,
            "id": new_user.id,
        }

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user.password = request.json.get("password", user.password)
        db.session.commit()
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return "", 204


class SignInView(Resource):
    def post(self):
        usuario = User.query.filter(
            User.username == request.json["username"],
            User.password == request.json["password"],
        ).first()
        db.session.commit()
        if usuario is None:
            return "User does not exist", 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Successfully signed in", "token": token_de_acceso}

class TasksView(Resource):

    @jwt_required()
    def get(self):
        return [conversion_task_schema.dump(conversion_task) for conversion_task in ConversionTask.query.all()]

    @jwt_required()
    def post(self):
        audio_file = request.files['file']
        filename = secure_filename(request.form['filename'])
        new_file_format = request.form['new_format']
        new_file_name = f'{filename.split(".")[0]}.{new_file_format}'
        new_task = ConversionTask(
                                user = get_jwt_identity(),
                                original_file_name = filename,
                                new_file_name = new_file_name,
                                new_file_format = new_file_format
        )
        db.session.add(new_task)
        db.session.commit()
        audio_file.save(os.path.join(current_app.config['FILES_FOLDER'], filename))
        args = (
            new_task.id, 
            new_task.original_file_name, 
            new_task.new_file_format
        )
        convert_file.apply_async(args=args, queue="batch")
        return conversion_task_schema.dump(new_task)

class TaskView(Resource):

    @jwt_required()
    def get(self, id_task):
        return conversion_task_schema.dump(ConversionTask.query.get_or_404(id_task))

    @jwt_required()
    def put(self, id_task):
        task = ConversionTask.query.get_or_404(id_task)
        task.status = request.json.get('status', task.status)
        task.user = request.json.get('user', task.user)
        task.original_file_name = request.json.get('original_file_name', task.original_file_name)
        task.new_file_name = request.json.get('new_file_name', task.mew_file_name)
        task.new_file_format = request.json.get('new_file_format', task.new_file_format)
        db.session.commit()
        return conversion_task_schema.dump(task)

    @jwt_required()
    def delete(self, id_task):
        task = ConversionTask.query.get_or_404(id_task)
        db.session.delete(task)
        db.session.commit()
        return 'Se ha eliminado la tarea', 204

class WorkerView(Resource):

    def post(self, id_task):
        task = ConversionTask.query.get_or_404(id_task)
        task.status = "PROCESSED"
        db.session.commit()
        return conversion_task_schema.dump(task)