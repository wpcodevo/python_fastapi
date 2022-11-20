pip install fastapi[all]
pip install sqlalchemy psycopg2
pip install "passlib[bcrypt]"
pip install 'fastapi-jwt-auth[asymmetric]'
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "creat users table"
alembic upgrade head
