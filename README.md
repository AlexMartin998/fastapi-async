# FastAPI

Deps: 
```sh
pip install fastapi "uvicorn[standard]" sqlalchemy "databases[postgresql]" pydantic-settings python-dotenv psycopg2-binary alembic gunicorn


# sync engine db
pip install fastapi "uvicorn[standard]" sqlmodel pydantic-settings python-dotenv alembic psycopg2-binary gunicorn


# asycn engine db
pip install fastapi "uvicorn[standard]" sqlmodel pydantic-settings python-dotenv alembic asyncpg psycopg2-binary gunicorn fastapi-filter "fastapi-pagination[sqlalchemy]"
pip install "pyjwt[crypto]" "passlib[bcrypt]" redis "pydantic[email]"

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


### Dev
Levantar el api
```sh
uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8009 \
  --reload
```
Si es un nuevo ambiente con DB en cero
```sh
alembic upgrade head
```
Ahi si levantar de nuevo con el uviconr






DirTree:
```sh
project/
┣ alembic/
┃ ┣ versions/
┃ ┃ ┣ .gitkeep
┃ ┃ ┣ 3c87bb9e808b_code_added_in_prodcut_category.py
┃ ┃ ┗ 90b452226718_initial_sqlmodel_tables.py
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
┃ ┃ ┣ filter.py
┃ ┃ ┣ logging_cfg.py
┃ ┃ ┣ middleware.py
┃ ┃ ┣ routes.py
┃ ┃ ┗ settings.py
┃ ┣ inventory_settings/
┃ ┃ ┣ dependencies/
┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┗ inventory_settings_di.py
┃ ┃ ┣ filters/
┃ ┃ ┃ ┣ __init__.py
┃ ┃ ┃ ┗ product_category_filter.py
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















Gracias, mira mi fill tree del skeleton quedo asi incialemnte:

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


Ahora necesito todo un sistema de inventario con modelos de SQLModel para esta api de fastapi, separado por featrures, como `inventory_settings`, `products`, etc., algo como vertical slicing pero no para clea architecture, sino para algo como lo de Srpogn Boot que tiene repositories, services, routers, DI, y cosas si con fastapi, ahoranecesito mas quie nada los modelos para algo de inventario con separacion de features, es decir, en inventory settings pueden ir modelos como `ProductModel` `ProductType`, `Warehouse`, y cosas asi, entnoces algo super robusto para una empresa grande que quiere su gestion de inventario completo con contabilidad, facturacino electronica, proceso de ventas con ERP y demas cosas, pero ahora inciemos con el inventario netamente, que tendra cosas completas de un sitema real de empresas grandes como cuentas contables a las que se asocian los productos, ingresos, egresos, movimeitnos de inventario, solicitud de compras, solicitud de transferencia que deben ser aprobadas por un rol supervisor de bodega o cosas asi super reales con flujos de empresas grandes, kardex, etc. Todo super completo por favor, separado por features que engloban modelos. Entonces vamos con eso primero cone sos modelos con SQLModel











