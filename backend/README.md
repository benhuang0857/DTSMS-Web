# DTSMS-Web

## alembic setting
* alembic.ini
    * Modify base on your db connection information:
    * Like: ```sqlalchemy.url = postgresql://dtsms_user:dtsms_password@db:5432/dtsms_db```

* Migration
    * ```alembic revision --autogenerate -m "Initial```migration"
    * Will create a file locate in alembic/versions/
        * alembic/versions/20240211120000_initial_migration.py
    * Do migration
        * ```alembic upgrade head```

alembic revision -m "create user table"
alembic upgrade head
alembic downgrade -1

## dummy data
python create_dummy_data.py

https://ithelp.ithome.com.tw/articles/10333168