from datetime import datetime, timedelta
from typing import List, Optional

from app import db
from models import Post, Categoria


class PostRepository:
    """Repository para operaciones CRUD sobre Post con nivel de abstracción Senior."""

    @staticmethod
    def _get_or_create_categories(data: dict) -> List[Categoria]:
        """
        Método privado para centralizar la lógica de categorías.
        Evita la repetición de código (DRY).
        """
        categorias = []

        # Categorías existentes por ID
        cat_ids = data.get("categoria_ids") or []
        if cat_ids:
            categorias_existentes = Categoria.query.filter(Categoria.id.in_(cat_ids)).all()
            categorias.extend(categorias_existentes)

        # Lógica para nueva categoría por texto
        nueva_cat_nombre = data.get("nueva_categoria")
        if nueva_cat_nombre and nueva_cat_nombre.strip():
            nombre_limpio = nueva_cat_nombre.strip()
            
            # Búsqueda optimizada (Case-insensitive)
            categoria_existente = Categoria.query.filter(
                db.func.lower(Categoria.nombre) == nombre_limpio.lower()
            ).first()

            if categoria_existente:
                if categoria_existente not in categorias:
                    categorias.append(categoria_existente)
            else:
                nueva_categoria = Categoria(nombre=nombre_limpio)
                db.session.add(nueva_categoria)
                db.session.flush()  # Obtenemos el ID antes del commit
                categorias.append(nueva_categoria)
        
        return categorias

    @staticmethod
    def get_all(published_only: bool = True, order_desc: bool = True) -> List[Post]:
        query = Post.query
        if published_only:
            query = query.filter_by(is_published=True)
        
        order_fn = Post.fecha_creacion.desc() if order_desc else Post.fecha_creacion.asc()
        return query.order_by(order_fn).all()

    @staticmethod
    def get_by_id(post_id: int) -> Optional[Post]:
        return Post.query.get(post_id)

    @staticmethod
    def get_by_user(user_id: int, published_only: bool = False) -> List[Post]:
        query = Post.query.filter_by(usuario_id=user_id)
        if published_only:
            query = query.filter_by(is_published=True)
        return query.order_by(Post.fecha_creacion.desc()).all()

    @staticmethod
    def create(data: dict) -> Post:
        """Crea un post utilizando la lógica centralizada de categorías."""
        nuevo_post = Post(
            titulo=data["titulo"],
            contenido=data["contenido"],
            usuario_id=data["usuario_id"],
            is_published=data.get("is_published", True)
        )
        
        # Usamos el método privado optimizado
        nuevo_post.categorias = PostRepository._get_or_create_categories(data)

        db.session.add(nuevo_post)
        db.session.commit()
        db.session.refresh(nuevo_post)
        return nuevo_post

    @staticmethod
    def update(post: Post, data: dict) -> Post:
        """Actualiza un post existente de forma segura."""
        if "titulo" in data:
            post.titulo = data["titulo"]
        if "contenido" in data:
            post.contenido = data["contenido"]
        if "is_published" in data:
            post.is_published = data["is_published"]

        # Actualizamos categorías solo si vienen en el data
        if "categoria_ids" in data or "nueva_categoria" in data:
            post.categorias = PostRepository._get_or_create_categories(data)

        db.session.commit()
        db.session.refresh(post)
        return post

    @staticmethod
    def delete(post: Post) -> None:
        db.session.delete(post)
        db.session.commit()

    @staticmethod
    def count_all(published_only: bool = True) -> int:
        query = Post.query
        if published_only:
            query = query.filter_by(is_published=True)
        return query.count()

    @staticmethod
    def get_posts_last_week() -> List[Post]:
        since = datetime.utcnow() - timedelta(days=7)
        return Post.query.filter(Post.fecha_creacion >= since).order_by(Post.fecha_creacion.desc()).all()