from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity


def roles_required(*roles):
    """
    Decorador para restringir acceso según el rol del usuario.
    Uso:
        @jwt_required()
        @roles_required('admin')              # solo admin
        @roles_required('admin', 'moderator') # admin o moderator
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verifica token valido
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role", "user")  # fallback 'user' si no viene

            if user_role not in roles:
                return jsonify({
                    "error": "Acceso denegado",
                    "message": f"Tu rol actual es '{user_role}'. Se requiere uno de: {roles}"
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


def active_user_required(fn):
    """
    Decorador que verifica que el usuario (segun claims) este activo.
    Requiere que el token incluya 'is_active' en los claims o que la vista
    valide la condición consultando la BD.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        is_active = claims.get("is_active", True)
        if not is_active:
            return jsonify({
                "error": "Usuario inactivo",
                "message": "Tu cuenta ha sido desactivada. Contacta al administrador."
            }), 403

        return fn(*args, **kwargs)
    return wrapper


def check_ownership_or_role(resource_owner_id):
    """
    Verifica si el usuario autenticado ES PROPIETARIO del recurso
    o tiene rol 'admin'. Retorna True/False.

    Uso dentro de una vista (MethodView):
        if not check_ownership_or_role(post.usuario_id):
            return jsonify({"error": "No tienes permiso"}), 403
    """
    try:
        user_id = get_jwt_identity()
        if user_id is None:
            return False
            
        claims = get_jwt()
        # Si es admin, tiene pase libre siempre
        if claims.get("role") == "admin":
            return True
            
        # Comparamos asegurando que ambos sean del mismo tipo (int)
        return int(user_id) == int(resource_owner_id)
    except (ValueError, TypeError):
        return False