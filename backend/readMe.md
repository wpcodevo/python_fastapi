pip install -r requirements.txt
<br>
create you .env file as .env.example
<br>
create your database on postgresql , the same database name in .env file
<br>

Run the command: alembic init alembic
<br>
Run the command: alembic revision --autogenerate -m "creat users table"
<br>
Run the command: alembic upgrade head
<br>
Run server: uvicorn app.main:app --host localhost --port 8000 --reload
