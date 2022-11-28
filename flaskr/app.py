from flaskr import create_app
from .modelos import db
from flask_restful import Api
from flask_jwt_extended import JWTManager
from .vistas import SignInView, SignUpView, TasksView, TaskView

app = create_app('default')
app_context = app.app_context()
app_context.push() 

db.init_app(app)
db.create_all()

api = Api(app)

# --- API Endpoints --
api.add_resource(SignUpView, "/api/auth/signup")
api.add_resource(SignInView, "/api/auth/login")
api.add_resource(TasksView, '/api/tasks')
api.add_resource(TaskView, '/api/tasks/<int:id_task>')

jwt = JWTManager(app)