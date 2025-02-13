from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this for security
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Chat Model
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route (Serve index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"})

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Login successful!"})
    return jsonify({"error": "Invalid credentials"}), 401

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Chatbot Route
@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    prompt = data['prompt']
    
    # Mock AI Response (Replace this with real chatbot logic)
    response = f"AI Response to: {prompt}"

    # Save to database
    new_chat = Chat(user_id=current_user.id, prompt=prompt, response=response)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"response": response})

# Fetch Chat History
@app.route('/history')
@login_required
def history():
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"prompt": c.prompt, "response": c.response} for c in chats])

if __name__ == '__main__':
    db.create_all()  # Ensures database tables are created
    app.run(debug=True)
