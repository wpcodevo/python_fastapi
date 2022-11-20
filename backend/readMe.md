pip install fastapi[all]
<br>
pip install sqlalchemy psycopg2
<br>
pip install "passlib[bcrypt]"
<br>
pip install 'fastapi-jwt-auth[asymmetric]'
<br>
pip install alembic
<br>
alembic init alembic
<br>
alembic revision --autogenerate -m "creat users table"
<br>
alembic upgrade head
