from marshmallow import Schema, fields, validate

class CommentCreateSchema(Schema):
    contenido = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "El contenido es obligatorio"}
    )

class CommentSchema(Schema):
    id = fields.Int()
    contenido = fields.Str()
    usuario_id = fields.Int()
    post_id = fields.Int()
    fecha_creacion = fields.DateTime()