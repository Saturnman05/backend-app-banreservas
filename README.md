# 🏦 MVP Banking API – FastAPI + Screaming Architecture

Este proyecto es un MVP de una aplicación bancaria que provee servicios básicos relacionados con:

- Cuentas bancarias

- Reclamaciones sobre cuentas y tarjetas

La arquitectura implementada sigue los principios de Screaming Architecture, donde el dominio es lo primero y la estructura del proyecto “grita” cuál es su propósito.

## Estructura del proyecto

```text
project/
│
├── app/
│   ├── accounts/                   # Módulo de Cuentas (Dominio principal)
│   │   ├── domain/
│   │   │   ├── models.py          # Entidades del dominio (Account)
│   │   │   ├── exceptions.py      # Excepciones del dominio
│   │   │   └── events.py          # Eventos del dominio (opcional)
│   │   ├── application/
│   │   │   ├── services.py        # Casos de uso (crear cuenta, listar, bloquear...)
│   │   │   └── dto.py             # DTOs o schemas de entrada/salida
│   │   ├── infrastructure/
│   │   │   ├── repository.py      # Implementación de acceso a base de datos
│   │   │   └── models_db.py       # Modelos de ORM
│   │   └── routes.py          # Rutas HTTP relacionadas a cuentas
│   │
│   ├── claims/                     # Módulo de Reclamaciones
│   │   ├── domain/
│   │   │   ├── models.py          # Entidad Claim
│   │   │   └── exceptions.py
│   │   ├── application/
│   │   │   ├── services.py        # Casos de uso: crear, revisar, resolver reclamaciones
│   │   │   └── dto.py
│   │   ├── infrastructure/
│   │   │   ├── repository.py
│   │   │   └── models_db.py
│   │   └── routes.py
│   │
│   ├── core/
│   │   ├── config.py               # Configuración general (env, BD, etc.)
│   │   ├── database.py             # Conexión y sesión de base de datos
│   │   ├── exceptions.py           # Manejo global de excepciones
│   │   └── security.py             # Autenticación y autorización (si aplica)
│   │
│   ├── main.py                     # Punto de entrada FastAPI
│   └── dependencies.py             # Inyección de dependencias
│
├── tests/
│   ├── accounts/
│   └── claims/
│
├── requirements.txt
└── README.md
```

## 🧠 Filosofía de la Arquitectura

Este proyecto sigue los principios de Screaming Architecture:

- El dominio es el punto central.

- Las carpetas se nombran por conceptos del negocio, no por capas técnicas.

- Aísla el dominio de infraestructura y frameworks.

- Facilita crecimiento modular.

## Instalacion

1️⃣ Clonar el repositorio

```bash
git clone https://github.com/usuario/mvp-banking-api.git
cd mvp-banking-api
```

2️⃣ Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
```

3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

4️⃣ Configurar variables de entorno

Crea un archivo .env:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/bankdb
ENV=development
```

▶️ Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```
