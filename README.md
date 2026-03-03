# Professional Blog Engine API

Una implementación de alto rendimiento para la gestión de contenidos, construida sobre **Flask** y estructurada bajo patrones de diseño empresariales. Este sistema prioriza el desacoplamiento, la integridad de los datos y un control de acceso granular basado en identidades.

---

## 🏛️ Arquitectura de Software

El sistema implementa una **Arquitectura Multi-Capa** diseñada para maximizar la mantenibilidad y facilitar la evolución del software sin efectos secundarios:

### 🔹 Patrón Repository (Persistence Layer)
Abstracción total de la capa de datos mediante `PostRepository`. Este patrón garantiza que la lógica de negocio sea agnóstica al motor de persistencia, permitiendo migraciones de base de datos o cambios en el ORM con impacto cero en las capas superiores.

### 🔹 Service Layer (Domain Logic)
Centralización de las reglas de negocio en `PostService`. Esta capa actúa como el orquestador del dominio, gestionando la validación compleja, la integridad referencial y la verificación de permisos antes de cualquier mutación de estado.

### 🔹 Interface Layer (MethodView & Marshmallow)
Implementación de **Vistas Basadas en Clases (CBV)** para una gestión RESTful consistente. Se utilizan **Data Transfer Objects (DTOs)** vía Marshmallow para garantizar contratos de interfaz estrictos, saneamiento de entradas y serialización optimizada de salidas.

---

## 🔐 Seguridad y Control de Acceso (RBAC)

El sistema de seguridad está diseñado bajo el principio de **Privilegio Mínimo** y verificación criptográfica:

* **Identidad**: Autenticación asíncrona mediante **JWT (JSON Web Tokens)** con inyección de identidad en el contexto de ejecución.
* **Autorización Jerárquica**: Implementación de **Role-Based Access Control (RBAC)** que define capacidades granulares para roles de *Administrator*, *Moderator* y *Standard User*.
* **Resource Ownership Verification**: Validación dinámica de propiedad para prevenir vulnerabilidades de referencia directa insegura a objetos (IDOR).

---

## 🛠️ Stack Tecnológico
* **Backend**: Python 3.10+ | Flask
* **Persistencia**: MySQL | SQLAlchemy (ORM)
* **Seguridad**: Flask-JWT-Extended | Hashing BCrypt
* **Esquemas & Validación**: Marshmallow
* **Infraestructura de Datos**: Flask-Migrate (Alembic)

---

## 📋 Especificación de la Interfaz (API Reference)

Esta API sigue los estándares RESTful, utilizando códigos de estado HTTP semánticos y una matriz de permisos basada en identidades.

| Dominio | Endpoint | Operación | Control de Acceso | Definición Técnica |
| :--- | :--- | :--- | :--- | :--- |
| **Identity** | `/api/register`, `/api/login` | POST | Anonymous | Gestión de identidades y emisión de JWT |
| **Content** | `/api/posts` | GET, POST | Public / Auth | CRUD de recursos e inyección de autoría |
| **Content** | `/api/posts/<id>` | GET, PUT, DELETE | Public / Owner+ | Validación de propiedad y roles administrativos |
| **Engagement**| `/api/posts/<id>/comments` | GET, POST | Public / Auth | Capa de interacción social y persistencia |
| **Engagement**| `/api/comments/<id>` | DELETE | Owner, Mod+ | Moderación jerárquica de contenido |
| **Taxonomy** | `/api/categories` | GET, POST, PUT | Public / Mod+ | Clasificación y categorización de datos |
| **Governance**| `/api/users` | GET, PATCH, DELETE | Admin | Ciclo de vida de usuarios y gestión de RBAC |
| **Analytics** | `/api/stats` | GET | Privileged | Agregación de métricas y datos del sistema |

---

## 💎 High-End Standards

* **Type Hinting**: Uso extensivo de tipado estático para robustez del código y análisis estático.
* **DRY & Modularidad**: Refactorización de componentes comunes en servicios privados y decoradores reutilizables.
* **Global Error Handling**: Gestión centralizada de excepciones para garantizar respuestas JSON normalizadas bajo cualquier escenario de falla.
* **Relational Integrity**: Gestión avanzada de relaciones Many-to-Many para la categorización dinámica de contenido.

---

## ⚙️ Configuración del Entorno de Desarrollo

```bash
# Clonar repositorio e ingresar
git clone [https://github.com/mateoJk/flask-blog-api-architecture](https://github.com/mateoJk/flask-blog-api-architecture)
cd flask-blog-api-architecture

# Entorno Virtual
python -m venv env
source env/bin/activate  # Linux / Mac
.\env\Scripts\Activate.ps1  # Windows PowerShell

# Instalación de dependencias
pip install -r requirements.txt

# Inicialización de la aplicación
flask run
