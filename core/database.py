import mysql.connector
import yoyo
from core import env

def init():
    backend = yoyo.get_backend(get_connection_url())
    migrations = yoyo.read_migrations('../migrations')
    backend.apply_migrations(backend.to_apply(migrations))

def get_connection():
    return mysql.connector.connect(
        host=env.DB_HOST,
        user=env.DB_USER,
        passwd=env.DB_PASSWORD
    )

def get_connection_url():
    return 'mysql://{}:{}@{}/{}'.format(
        env.DB_USER, env.DB_PASSWORD, env.DB_HOST, env.DB_NAME
    )