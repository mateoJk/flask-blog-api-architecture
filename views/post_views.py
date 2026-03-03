from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity

from services.post_service import PostService
from schemas.post_schemas import PostCreateSchema, PostUpdateSchema, PostSchema
from decorators.auth_decorators import roles_required, active_user_required

# Instanciamos el servicio
post_service = PostService()

class PostsAPI(MethodView):
    """Endpoints para /api/posts"""

    def get(self):
        """Listar todos los posts públicos"""
        posts = post_service.get_public_posts()
        return jsonify(PostSchema(many=True).dump(posts)), 200

    @roles_required("user", "moderator", "admin")
    @active_user_required
    def post(self):
        """Crear un nuevo post"""
        try:
            # Validación con Marshmallow
            data = request.get_json()
            valid_data = PostCreateSchema().load(data)
            
            # El usuario_id se inyecta desde el JWT por seguridad
            valid_data["usuario_id"] = get_jwt_identity()

            nuevo_post = post_service.create_post(valid_data)
            return jsonify(PostSchema().dump(nuevo_post)), 201
            
        except ValidationError as err:
            return jsonify({"error": "Datos inválidos", "messages": err.messages}), 400
        except Exception as e:
            return jsonify({"error": "Error interno del servidor", "message": str(e)}), 500


class PostDetailAPI(MethodView):
    """Endpoints para /api/posts/<id>"""

    def get(self, post_id):
        """Obtener un post específico"""
        post = post_service.get_post_by_id(post_id)
        if not post:
            return jsonify({"error": "Post no encontrado"}), 404
        return jsonify(PostSchema().dump(post)), 200

    @roles_required("user", "moderator", "admin")
    @active_user_required
    def put(self, post_id):
        """Actualizar un post (la seguridad la maneja el Service)"""
        post = post_service.get_post_by_id(post_id)
        if not post:
            return jsonify({"error": "Post no encontrado"}), 404

        try:
            data = request.get_json()
            valid_data = PostUpdateSchema().load(data)

            # Delevamos la responsabilidad de verificar propiedad al Service
            actualizado = post_service.update_post(post, valid_data)
            return jsonify(PostSchema().dump(actualizado)), 200
            
        except ValidationError as err:
            return jsonify({"error": "Datos inválidos", "messages": err.messages}), 400
        except PermissionError as err:
            return jsonify({"error": "Acceso denegado", "message": str(err)}), 403

    @roles_required("user", "moderator", "admin")
    @active_user_required
    def delete(self, post_id):
        """Eliminar un post (la seguridad la maneja el Service)"""
        post = post_service.get_post_by_id(post_id)
        if not post:
            return jsonify({"error": "Post no encontrado"}), 404

        try:
            # El Service lanzará PermissionError si no es el dueño o admin
            post_service.delete_post(post)
            return jsonify({"message": "Post eliminado correctamente"}), 200
            
        except PermissionError as err:
            return jsonify({"error": "Acceso denegado", "message": str(err)}), 403