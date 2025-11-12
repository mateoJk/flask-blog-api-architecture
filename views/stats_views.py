from flask.views import MethodView
from flask import jsonify
from decorators.auth_decorators import roles_required, active_user_required
from services.stats_service import StatsService
from flask_jwt_extended import get_jwt

stats_service = StatsService()

class StatsAPI(MethodView):
    """Endpoints para /api/stats"""

    @roles_required("admin", "moderator")
    @active_user_required
    def get(self):
        """Obtiene estadísticas generales de la aplicación"""
        stats = stats_service.get_stats()

        claims = get_jwt()  # obtenemos claims del token
        role = claims.get("role")

        # Si no es admin, eliminamos posts_last_week
        if role != "admin":
            stats.pop("posts_last_week", None)

        return jsonify(stats), 200