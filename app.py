from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f05f31fd-b1e3-43d3-a594-0fbc3862ef1d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Todo(db.Model):
    user_id = db.Column(db.Integer, nullable = False)
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    image = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250),nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    is_active = db.Column(db.Boolean , default = True)
    is_authenticated = db.Column(db.Boolean , default = True)

    def __repr__(self):
        return '<User %r>' % self.user_id
    
    def get_id(self):
        return self.user_id

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
	return render_template('home.html')

@app.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        uploaded_files = request.files.getlist('image')
        print("uploaded files", uploaded_files)
        num_files = len(uploaded_files)
        print("number of files", num_files)
        for task_image in uploaded_files:
            if not task_image or not task_image.filename:  
                filename = ""
            else:
                filename = secure_filename(task_image.filename)
            if not filename == "":  
                new_task=Todo(content=task_content, user_id = current_user.get_id(), image = task_image.read())
            else:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], "empty.png")
                new_task=Todo(content=task_content, user_id = current_user.get_id(), image = file_path)
            try:
                db.session.add(new_task)
                db.session.commit()
            except:
                return 'there was an issue adding your task'
            
        return redirect('/index')
    else:
        tasks = Todo.query.filter_by(user_id = current_user.get_id()).all()
        return render_template('index.html' , tasks=tasks)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/index')
    except:
        return "your task could not be deleted"
    
@app.route('/deleteimage/<int:id>')
@login_required
def delete_image(id):
    task = Todo.query.get_or_404(id)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], "empty.png")
    task.image = filepath
    try:
        db.session.commit()
        return redirect('/index')
    except:
        return "your image could not be deleted"
    
@app.route('/display/<int:id>')
@login_required
def display(id):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.get_id()) + "_" + str(id) + ".jpg")
        return render_template('display.html', image_url=file_path)
    except: 
        return "there is a problem with the image"
    
@app.route('/update/<int:id>', methods=['POST','GET'])
@login_required
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        image = request.files['image']
        if not image or not image.filename:  
            filename = ""
        else:
            filename = secure_filename(image.filename)
        if not filename == "":  
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(file_path)
        else:
            file_path = task.image
        task.image = file_path
        try:
            db.session.commit()
            return redirect('/index')
        except:
            return "task could not be updated"

    else: 
        return render_template('update.html' , task=task)
        
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        new_user=User(username=username,password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            return render_template('alreadyRegistered.html') #user already registered

    else: 
	    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = User.query.filter_by(username=request.form['username']).one()
            if user.password == request.form['password']:
                login_user(user)
                return redirect('/index')
            else:
                return render_template('wrongPassword.html')
        except:
            return render_template('unregistered.html')
            
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)