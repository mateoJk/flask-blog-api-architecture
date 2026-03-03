from marshmallow import Schema, fields, validate, validates_schema, ValidationError

# schemas de validacion con Marshmallow

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=64), error_messages={"required": "El nombre de usuario es obligatorio"})
    email = fields.Email(required=True, error_messages={"required": "El email es obligatorio"})
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128), error_messages={"required": "La contraseña es obligatoria"})
    role = fields.Str(
        required=True,
        validate=validate.OneOf(["user", "moderator", "admin"]),
        error_messages={
            "required": "El rol es obligatorio",
            "validator_failed": "El rol debe ser 'user', 'moderator' o 'admin'"
        }
    )

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RoleUpdateSchema(Schema):
    role = fields.Str(
        required=True,
        validate=validate.OneOf(["user", "moderator", "admin"]),
        error_messages={
            "required": "El rol es obligatorio.",
            "validator_failed": "El rol debe ser 'user', 'moderator' o 'admin'."
        }
    )