from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from PIL import Image
from io import BytesIO
import os
import base64
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
                               
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f05f31fd-b1e3-43d3-a594-0fbc3862ef1d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)
CORS(app)

with app.app_context():
    db.create_all()

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Todo(db.Model):
    user_id = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_authenticated = db.Column(db.Boolean, default=True)

    def get_id(self):
        return self.user_id

class TaskImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    image = db.Column(db.String, nullable=False)  # base64

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

def get_current_user():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]
        try:
            serializer = Serializer(app.config['SECRET_KEY'])
            data = serializer.loads(token)
            return User.query.get(data['user_id'])
        except:
            return None
    return None

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    if request.method == 'POST':
        task_content = request.json.get('content')
        uploaded_files = request.json.get('images', [])
        deadline = request.json.get('date')
        due_date = datetime.strptime(deadline, '%Y-%m-%d')

        if due_date < (datetime.now() - timedelta(days=1)):
            return jsonify({"error": "Deadline cannot be in the past"}), 400

        new_task = Todo(content=task_content, user_id=current_user.get_id(), deadline=due_date)
        db.session.add(new_task)
        db.session.commit()

        for image in uploaded_files:
            task_image = TaskImage(task_id=new_task.id, image=image)
            db.session.add(task_image)
        db.session.commit()

        return jsonify({"message": "Task created successfully"}), 201

    elif request.method == 'POST':
        tasks = Todo.query.filter_by(user_id=current_user.get_id()).all()
        result = [
            {
                "id": task.id,
                "content": task.content,
                "deadline": task.deadline.strftime('%Y-%m-%d'),
                "images": [
                    {"id": img.id, "base64": img.image}
                    for img in TaskImage.query.filter_by(task_id=task.id).all()
                ]
            }
            for task in tasks
        ]
        return jsonify(result)

@app.route('/tasks/<int:id>', methods=['DELETE', 'PUT'])
@login_required
def manage_task(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        TaskImage.query.filter_by(task_id=id).delete()
        db.session.commit()
        return jsonify({"message": "Task and associated images deleted"}), 200

    elif request.method == 'PUT':
        task.content = request.json.get('content', task.content)
        deadline = request.json.get('date', task.deadline.strftime('%Y-%m-%d'))
        task.deadline = datetime.strptime(deadline, '%Y-%m-%d')

        uploaded_files = request.json.get('images', [])
        for image in uploaded_files:
            task_image = TaskImage(task_id=task.id, image=image)
            db.session.add(task_image)

        db.session.commit()
        return jsonify({"message": "Task updated successfully"}), 200

from werkzeug.security import generate_password_hash

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 400

    hashed_password = generate_password_hash(password)
    
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        serializer = Serializer(app.config['SECRET_KEY'])
        token = serializer.dumps({'user_id': user.user_id})
        login_user(user)
        # access_token = create_access_token(identity=username)
        # response = {"access_token":access_token}
        # return response
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

if __name__ == "__main__":
    app.run(debug=True)