# Preparacion e instalación
git clone <https://github.com/mateoJk/efi_segundo_semestre>
cd <efi_segundo_semestre>
python -m venv env
source env/bin/activate  # Linux/Mac
.\env\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt

# Cómo ejecutar la app
flask run


# Documentacion de endpoints
# NOTA: Todos los endpoints que requieren autenticación deben recibir el token JWT en el header: Authorization: Bearer <token>

#### **Posts**
```
GET    /api/posts              # Público - listar todos los posts
GET    /api/posts/<id>         # Público - ver un post específico
POST   /api/posts              # Requiere autenticación (user+)
PUT    /api/posts/<id>         # Solo el autor o admin
DELETE /api/posts/<id>         # Solo el autor o admin
```

#### **Comentarios**
```
GET    /api/posts/<id>/comments      # Público
POST   /api/posts/<id>/comments      # Requiere autenticación (user+)
DELETE /api/comments/<id>            # Autor, moderator o admin
```

#### **Categorías**
```
GET    /api/categories         # Público
POST   /api/categories         # Solo moderator y admin
PUT    /api/categories/<id>    # Solo moderator y admin
DELETE /api/categories/<id>    # Solo admin
```

#### **Usuarios (Admin)**
```
GET    /api/users              # Solo admin
GET    /api/users/<id>         # Usuario mismo o admin
PATCH  /api/users/<id>/role    # Solo admin (cambiar rol)
DELETE /api/users/<id>         # Solo admin (desactivar)
```

#### **Estadísticas**
```
GET /api/stats                 # Moderator y admin
  Response: {
    "total_posts": 45,
    "total_comments": 120,
    "total_users": 30,
    "posts_last_week": 8  // solo admin
  }
```


# Credenciales de Prueba
admin: "email": "admin1@test.com" / "password": "123456"
#
moderator: "email": "user1@test.com" / "password": "123456"
#
user: "email": "user2@test.com" / "password": "123455"

