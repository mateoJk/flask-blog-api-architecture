import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
# Instanciamos extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Instancia de Flask
app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'mysql+pymysql://root:@172.26.112.1/miniblog'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'cualquiercosa')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
CORS(app)
# Inicializar extensiones
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

# Importar modelos y vistas
from models import Usuario, UserCredentials, Post, Comentario, Categoria, post_categoria
from views import (
    AuthRegisterView, AuthLoginView,
    PostsAPI, PostDetailAPI,
    PostCommentsAPI, CommentDeleteAPI,
    CategoriesAPI, CategoryDetailAPI,
    UsersAPI, UserDetailAPI, UserRolePatchAPI,
    StatsAPI
)

# Registrar rutas
app.add_url_rule('/api/register', view_func=AuthRegisterView.as_view('register'), methods=['POST'])
app.add_url_rule('/api/login', view_func=AuthLoginView.as_view('login'), methods=['POST'])

app.add_url_rule('/api/posts', view_func=PostsAPI.as_view('posts'), methods=['GET', 'POST'])
app.add_url_rule('/api/posts/<int:post_id>', view_func=PostDetailAPI.as_view('post_detail'),
                 methods=['GET', 'PUT', 'DELETE'])

app.add_url_rule('/api/posts/<int:post_id>/comments', view_func=PostCommentsAPI.as_view('post_comments'),
                 methods=['GET', 'POST'])
app.add_url_rule('/api/comments/<int:comment_id>', view_func=CommentDeleteAPI.as_view('comment_delete'),
                 methods=['DELETE'])

app.add_url_rule('/api/categories', view_func=CategoriesAPI.as_view('categories'), methods=['GET', 'POST'])
app.add_url_rule('/api/categories/<int:cat_id>', view_func=CategoryDetailAPI.as_view('category_detail'),
                 methods=['PUT', 'DELETE'])

app.add_url_rule('/api/users', view_func=UsersAPI.as_view('users'), methods=['GET'])
app.add_url_rule('/api/users/<int:user_id>', view_func=UserDetailAPI.as_view('user_detail'),
                 methods=['GET', 'DELETE'])
app.add_url_rule('/api/users/<int:user_id>/role', view_func=UserRolePatchAPI.as_view('user_role'),
                 methods=['PATCH'])

app.add_url_rule('/api/stats', view_func=StatsAPI.as_view('stats'), methods=['GET'])


# Manejo de errores JSON

@app.errorhandler(400)
def bad_request(err):
    return jsonify({"error": "Bad Request"}), 400

@app.errorhandler(401)
def unauthorized(err):
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(err):
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(404)
def not_found(err):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(500)
def internal_error(err):
    return jsonify({"error": "Internal Server Error"}), 500


# Arranque de la app

if __name__ == '__main__':
    app.run(debug=True)