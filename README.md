# API de Facturación - FastAPI

Proyecto desarrollado como evidencia de aprendizaje SENA. Es una API REST construida con **FastAPI** que gestiona **Clientes**, **Facturas** y **Transacciones**, con relación entre ellos y CRUD completo.

## Descripción del proyecto

- **Clientes**: información básica de cada cliente (nombre, email, descripción).
- **Facturas**: pertenecen a un cliente y contienen una lista de transacciones. El valor total se calcula automáticamente sumando `cantidad * valor_unitario` de cada transacción asociada.
- **Transacciones**: pertenecen a una factura, con cantidad y valor unitario.

## Estructura del proyecto

```
app/
├── main.py                  # Punto de entrada, arma la app FastAPI
├── listas.py                 # Listas en memoria que simulan la "base de datos"
├── modelos/
│   ├── clientes.py            # Modelos Pydantic de Cliente
│   ├── facturas.py            # Modelos Pydantic de Factura (con valor_total calculado)
│   └── transacciones.py       # Modelos Pydantic de Transaccion
└── enrutadores/
    ├── clientes.py             # Endpoints CRUD de clientes
    ├── facturas.py             # Endpoints CRUD de facturas
    └── transacciones.py        # Endpoints CRUD de transacciones
requirements.txt
```

## Relación entre entidades

- Un **Cliente** puede tener muchas **Facturas** (relación 1 a N).
- Una **Factura** puede tener muchas **Transacciones** (relación 1 a N).
- El **valor_total** de una factura se calcula dinámicamente a partir de sus transacciones (campo `computed_field`).

Como no se usa base de datos externa, la persistencia se simula con listas en memoria (`listas.py`), que se reinician cada vez que se reinicia el servidor.

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

5. Abrir la documentación interactiva (Swagger UI):
   ```
   http://127.0.0.1:8000/docs
   ```

## Proceso de desarrollo (historial de commits)

El proyecto se desarrolló de forma incremental, empezando sin estructura (todo en un solo `main.py`) y evolucionando hacia una estructura organizada por carpetas (`modelos` y `enrutadores`). El historial de commits refleja este proceso, ver sección de commits abajo.

## Autor

Erik - Aprendiz SENA, ficha 3407187.
