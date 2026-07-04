# API de Facturación - FastAPI + SQLModel

Proyecto desarrollado como evidencia de aprendizaje SENA. Es una API REST construida con **FastAPI** y **SQLModel** que gestiona **Clientes**, **Facturas** y **Transacciones**, con relación entre ellas y CRUD completo, persistiendo los datos en una base de datos **SQLite**.

## Descripción del proyecto

- **Clientes**: información básica de cada cliente (nombre, email, descripción).
- **Facturas**: pertenecen a un cliente y contienen una lista de transacciones. El valor total se calcula sumando `cantidad * valor_unitario` de cada transacción asociada.
- **Transacciones**: pertenecen a una factura, con cantidad y valor unitario.

## Estructura del proyecto

```
app/
├── main.py                  # Punto de entrada, arma la app y crea las tablas al iniciar
├── conexion_bd.py             # Configuración de conexión a SQLite (SQLModel)
├── modelos/                    # Modelos SQLModel: tabla + validación en un solo lugar
│   ├── clientes.py
│   ├── facturas.py
│   └── transacciones.py
└── enrutadores/                 # Endpoints CRUD por entidad
    ├── clientes.py
    ├── facturas.py
    └── transacciones.py
requirements.txt
```

## ¿Por qué SQLModel?

SQLModel es una librería creada por el mismo autor de FastAPI. Combina en una sola clase lo que en SQLAlchemy + Pydantic serían dos clases separadas: una misma clase puede representar la tabla en la base de datos y, al mismo tiempo, validar los datos que entran y salen de la API.

Por eso en `modelos/` verás varias clases por archivo:
- Una clase base con los campos comunes (ej. `ClienteBase`).
- Una clase con `table=True` que es la tabla real en la base de datos (ej. `Cliente`).
- Clases para crear/editar (`ClienteCrear`, `ClienteEditar`) que definen qué datos recibe la API.
- Una clase de respuesta (ej. `ClienteRespuesta`) que define qué devuelve la API.

## Base de datos

El proyecto usa **SQLite** a través de **SQLModel**. Al iniciar la aplicación, se crea automáticamente el archivo `bd_facturacion.sqlite3` en la raíz del proyecto con las 3 tablas y sus relaciones (llaves foráneas).

### Relación entre entidades

- Un **Cliente** puede tener muchas **Facturas** (relación 1 a N, llave foránea `cliente_id` en `factura`).
- Una **Factura** puede tener muchas **Transacciones** (relación 1 a N, llave foránea `factura_id` en `transaccion`).
- El **valor_total** de una factura se calcula al construir la respuesta, sumando `cantidad * valor_unitario` de cada transacción asociada.

Puedes revisar la base de datos generada con la extensión **SQLite Viewer** en VS Code, abriendo el archivo `bd_facturacion.sqlite3`.

## Endpoints disponibles

### Clientes
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/clientes` | Listar todos los clientes |
| GET | `/clientes/{cliente_id}` | Listar un cliente por id |
| POST | `/clientes` | Crear un cliente |
| PATCH | `/clientes/{cliente_id}` | Editar un cliente |
| DELETE | `/clientes/{cliente_id}` | Eliminar un cliente |

### Facturas
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/facturas` | Listar todas las facturas |
| GET | `/facturas/{factura_id}` | Listar una factura por id |
| POST | `/facturas/{cliente_id}` | Crear una factura asociada a un cliente |
| PATCH | `/facturas/{factura_id}` | Editar una factura |
| DELETE | `/facturas/{factura_id}` | Eliminar una factura |

### Transacciones
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/transacciones` | Listar todas las transacciones |
| GET | `/transacciones/{transaccion_id}` | Listar una transacción por id |
| POST | `/transacciones/{factura_id}` | Crear una transacción asociada a una factura |
| PATCH | `/transacciones/{transaccion_id}` | Editar una transacción |
| DELETE | `/transacciones/{transaccion_id}` | Eliminar una transacción |

## Instalación y ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/ErikRm1962/Fast-Api.git
   cd Fast-Api
   ```

2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecutar el servidor:
   ```bash
   fastapi dev app/main.py
   ```
   Al iniciar, se crea automáticamente el archivo `bd_facturacion.sqlite3` con las tablas.

5. Abrir la documentación interactiva (Swagger UI):
   ```
   http://127.0.0.1:8000/docs
   ```

## Proceso de desarrollo (historial de commits)

El proyecto se desarrolló de forma incremental:
1. Versión inicial sin estructura (todo en un `main.py`, listas en memoria).
2. Reestructuración con carpetas (`modelos`, `enrutadores`), aún con listas en memoria.
3. Migración a base de datos real con SQLModel y SQLite, con relaciones entre tablas.
4. Documentación final.

El historial de commits refleja este proceso completo.

## Autor

Erik - Aprendiz SENA, ficha 3407187.
