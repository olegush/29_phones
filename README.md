# Microservice for Search Index of Phone Numbers

This microservice can help with search phone numbers in the database. First script, using [Alembic](https://alembic.sqlalchemy.org/en/latest/), adds new column in the orders table. Second one, using [phonenumbers library](https://github.com/daviddrysdale/python-phonenumbers) normalizes phone numbers and save them in the new column. It runs in the background, awaits new orders and updates rows.


# How to Install

Python 3 and libraries from **requirements.txt** should be installed. Use virtual environment tool, for example **virtualenv**.

```bash

virtualenv virtualenv_folder_name
source virtualenv_folder_name/bin/activate
python3 -m pip install -r requirements.txt
```

Put all necessary parameters to .env file.

```bash
PG_HOST=postgresql_host
PG_PORT=postgresql_port
PG_DB=postgresql_db
PG_TABLE=postgresql_table
PG_USER=postgresql_user
PG_PWD=postgresql_password
PG_NEW_COLUMN_NAME=name_of_new_colunm

```

# Quickstart

1. Run **add_column.py**.

```bash
$ python add_column.py
```

2. Check if table has new column.

3. Run **normalize_phone.py**.

4. Check if new column contains normalized phone numbers.


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
