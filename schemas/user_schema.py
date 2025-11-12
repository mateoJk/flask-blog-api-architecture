from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    is_active = fields.Bool()
    created_at = fields.DateTime()
    role = fields.Method("get_role")

    def get_role(self, obj):
        # obj.credenciales es la relación uno a uno con UserCredentials
        return obj.credenciales.role if obj.credenciales else None