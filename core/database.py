import mysql.connector
import yoyo
import json
from core import env
from datetime import datetime

def init():
    backend = yoyo.get_backend(get_connection_url())
    migrations = yoyo.read_migrations('./core/migrations')
    backend.apply_migrations(backend.to_apply(migrations))

def get_connection():
    return mysql.connector.connect(
        host=env.DB_HOST,
        port=env.DB_PORT,
        database=env.DB_NAME,
        user=env.DB_USER,
        passwd=env.DB_PASSWORD
    )

def get_connection_url():
    return 'mysql://{}:{}@{}:{}/{}'.format(
        env.DB_USER, env.DB_PASSWORD, env.DB_HOST, env.DB_PORT, env.DB_NAME
    )

def execute_query(queries):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query.content, query.params)
        connection.commit()
    except mysql.connector.Error as error:
        print('Failed to execute query error: {}'.format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_transactions(transactions):
    queries = []
    for transaction in transactions:
        content = """  
            INSERT INTO account_transaction (
                nordigen_transaction_id,
                title,
                date,
                amount,
                source,
                create_date
            ) VALUES (%(nordigen_transaction_id)s, %(title)s, %(date)s, %(amount)s, %(source)s, %(current_datetime)s)
            ON DUPLICATE KEY UPDATE amount = %(amount)s, source = %(source)s, last_edit_date = %(current_datetime)s;
        """
        params = {
            'nordigen_transaction_id': transaction.id,
            'title': transaction.title,
            'date': transaction.date,
            'amount': transaction.amount,
            'source': json.dumps(transaction.source),
            'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        queries.append(DbQuery(content, params))
    execute_query(queries)


class DbQuery:
    def __init__(self, content, params):
        self.content = content
        self.params = params