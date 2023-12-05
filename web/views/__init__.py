from flask import Flask, render_template
from views.auth import auth_blueprint
from views.novels import novels_blueprint
from views.browser import browser_blueprint
from views.forum import forum_blueprint

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'root'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/wriding'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads/novel_covers')

# Registrar los blueprints en la aplicación
app.register_blueprint(auth_blueprint)
app.register_blueprint(novels_blueprint)
app.register_blueprint(browser_blueprint)
app.register_blueprint(forum_blueprint)

# Resto de la configuración y rutas de la aplicación...
# ...

if __name__ == '__main__':
    app.run(debug=True)
