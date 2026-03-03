from marshmallow import Schema, fields, validate


class PostCreateSchema(Schema):
    """Validación para crear un nuevo post"""
    titulo = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=140),
        error_messages={"required": "El título es obligatorio"}
    )
    contenido = fields.Str(
        required=True,
        validate=validate.Length(min=10),
        error_messages={"required": "El contenido es obligatorio"}
    )
    categoria_ids = fields.List(fields.Int(), required=False)    # IDs de categorías existentes
    nueva_categoria = fields.Str(required=False)   
    is_published = fields.Bool(load_default=True)


class PostUpdateSchema(Schema):
    """Validación para actualizar un post existente"""
    titulo = fields.Str(validate=validate.Length(min=3, max=140))
    contenido = fields.Str(validate=validate.Length(min=10))
    categoria_ids = fields.List(fields.Int(), required=False)
    nueva_categoria = fields.Str(required=False)
    is_published = fields.Bool()

class CategoriaSimpleSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()

class PostSchema(Schema):
    """Formato de salida para mostrar posts"""
    id = fields.Int(dump_only=True)
    titulo = fields.Str()
    contenido = fields.Str()
    is_published = fields.Bool()
    fecha_creacion = fields.DateTime()
    fecha_actualizacion = fields.DateTime()
    usuario_id = fields.Int()
    autor_username = fields.Method("get_autor_username")
    categorias = fields.List(fields.Nested(CategoriaSimpleSchema))

    def get_autor_username(self, obj):
        """Devuelve el nombre del autor asociado al post"""
        return obj.autor.username if obj.autor else None