# FastAPI

Deps: 
```sh
pip install fastapi "uvicorn[standard]" sqlalchemy "databases[postgresql]" pydantic-settings python-dotenv psycopg2-binary alembic gunicorn


# sync engine db
pip install fastapi "uvicorn[standard]" sqlmodel pydantic-settings python-dotenv alembic psycopg2-binary gunicorn


# asycn engine db
pip install fastapi "uvicorn[standard]" sqlmodel pydantic-settings python-dotenv alembic asyncpg psycopg2-binary gunicorn fastapi-filter "fastapi-pagination[sqlalchemy]"

```

Paso:
```sh
alembic init alembic

```

Migraciones:
Como es async mi cnofig, debo colocar manualament en cada file `import sqlmodel` para q no se rompa. Luego ya se van agregando migraciones y se las corre con estos dos comandos.

```sh
alembic revision --autogenerate -m "Fix code field annotation in ProductCategory"
alembic upgrade head
```




DirTree:
```sh
project/
┣ alembic/
┃ ┣ versions/
┃ ┃ ┗ .gitkeep
┃ ┣ README
┃ ┣ env.py
┃ ┗ script.py.mako
┣ src/
┃ ┣ core/
┃ ┃ ┣ shared/
┃ ┃ ┃ ┣ exceptions/
┃ ┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┃ ┣ custom_exception.py
┃ ┃ ┃ ┃ ┗ not_found_exception.py
┃ ┃ ┃ ┣ models/
┃ ┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┃ ┗ audit_mixin_model.py
┃ ┃ ┃ ┣ repositories/
┃ ┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┃ ┗ generic_repository.py
┃ ┃ ┃ ┣ services/
┃ ┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┃ ┗ generic_service.py
┃ ┃ ┃ ┗ __init__.py
┃ ┃ ┣ __init__.py
┃ ┃ ┣ database.py
┃ ┃ ┣ error.py
┃ ┃ ┣ logging_cfg.py
┃ ┃ ┣ middleware.py
┃ ┃ ┣ routes.py
┃ ┃ ┗ settings.py
┃ ┣ inventory_settings/
┃ ┃ ┣ dependencies/
┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┗ inventory_settings_di.py
┃ ┃ ┣ models/
┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┗ product_category_model.py
┃ ┃ ┣ repositories/
┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┗ product_category_repository.py
┃ ┃ ┣ routers/
┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┗ category_router.py
┃ ┃ ┣ schemas/
┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┗ product_category_schema.py
┃ ┃ ┣ services/
┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┗ product_category_service.py
┃ ┃ ┗ __init__.py
┃ ┣ __init__.py
┃ ┗ main.py
┣ .env
┣ .env.example
┣ .gitignore
┣ README.md
┣ alembic.ini
┗ requirements.txt
```













