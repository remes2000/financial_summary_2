import os
import mysql.connector
import yoyo

DB_HOST = os.getenv('DB_HOST') or 'localhost:3306'
DB_USER = os.getenv('DB_USER') or 'root'
DB_PASSWORD = os.getenv('DB_PASSWORD') or 'ZAQ!2wsx'
DB_NAME = os.getenv('DB_NAME') or 'financial_summary'

def init():
    backend = yoyo.get_backend(get_connection_url())
    migrations = yoyo.read_migrations('../../migrations')
    backend.apply_migrations(backend.to_apply(migrations))

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD
    )

def get_connection_url():
    return 'mysql://{}:{}@{}/{}'.format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
    )