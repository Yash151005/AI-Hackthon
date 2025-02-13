from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from routes.auth import auth
from routes.chatbot import chatbot

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(chatbot, url_prefix='/bot')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
