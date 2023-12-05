from flask import Flask, render_template, request
from models import db
from models.novels import Followers, LikeNovel, Novels, ReadLater, Libraries
from models.users import Users
from views.auth import auth_blueprint
from views.novels import novels_blueprint
from views.users import users_blueprint
from views.browser import browser_blueprint
from views.forum import forum_blueprint

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'root'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/wriding'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')

# Inicializa la base de datos
db.init_app(app)
app.register_blueprint(auth_blueprint)
app.register_blueprint(novels_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(browser_blueprint)
app.register_blueprint(forum_blueprint)


# Registra el blueprint de autenticación
@app.route('/')
def home():
    novels = Novels.query.order_by(Novels.id.desc()).limit(10)  
    novels2 = Novels.query.order_by(Novels.views.desc()).limit(10) 
    return render_template('index.html', novels=novels,novels2 = novels2)
if __name__ == '__main__':
    app.run(debug=True)
