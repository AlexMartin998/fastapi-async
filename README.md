# FastAPI

Deps: 
```sh
pip install fastapi "uvicorn[standard]" sqlalchemy "databases[postgresql]" pydantic-settings python-dotenv psycopg2-binary alembic gunicorn


# sync engine db
pip install fastapi "uvicorn[standard]" sqlmodel pydantic-settings python-dotenv alembic psycopg2-binary gunicorn


# asycn engine db
pip install fastapi "uvicorn[standard]" sqlmodel pydantic-settings python-dotenv alembic asyncpg psycopg2-binary gunicorn

```

Paso:
```sh
alembic init alembic

```



DirTree:
```sh
project/
┣ alembic/
┃ ┣ versions/
┃ ┣ README
┃ ┣ env.py
┃ ┗ script.py.mako
┣ src/
┃ ┣ core/
┃ ┃ ┣ __init__.py
┃ ┃ ┣ config.py
┃ ┃ ┣ database.py
┃ ┃ ┣ logging_cfg.py
┃ ┃ ┗ routes.py
┃ ┣ __init__.py
┃ ┗ main.py
┣ .env
┣ .gitignore
┣ README.md
┣ alembic.ini
┗ requirements.txt
```
