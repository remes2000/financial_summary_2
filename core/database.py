import mysql.connector
import yoyo
import json
from core import env
from datetime import datetime
from core.models import Category, RegularExpression

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
    results = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        for query in queries:
            cursor.execute(query.content, query.params)
            results.append(cursor.fetchall())
        connection.commit()
    except mysql.connector.Error as error:
        print('Failed to execute query error: {}'.format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return results

def insert_transactions(transactions):
    queries = []
    for transaction in transactions:
        content = """  
            INSERT INTO account_transaction (
                nordigen_transaction_id,
                title,
                category_id,
                date,
                amount,
                source,
                create_date
            ) VALUES (%(nordigen_transaction_id)s, %(title)s, %(category_id)s, %(date)s, %(amount)s, %(source)s, %(current_datetime)s)
            ON DUPLICATE KEY UPDATE amount = %(amount)s, source = %(source)s, last_edit_date = %(current_datetime)s;
        """
        params = {
            'nordigen_transaction_id': transaction.id,
            'title': transaction.title,
            'category_id': None if transaction.category == None else transaction.category.id,
            'date': transaction.date,
            'amount': transaction.amount,
            'source': json.dumps(transaction.source),
            'current_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        queries.append(DbQuery(content, params))
    execute_query(queries)

def get_categories():
    categories = {}
    query = """ 
        SELECT 
            c.id, c.name, r.id, r.content
        FROM category c 
        LEFT JOIN regular_expression r ON c.id = r.category_id 
    """
    rows = execute_query([DbQuery(query)])[0]
    for row in rows:
        category_values = row[0:2]
        regular_expression_values = row[2:4]
        category_id = category_values[0]
        regular_expression = RegularExpression(db_row=regular_expression_values)
        if category_id not in categories:
            categories[category_id] = Category(db_row=category_values)
        categories[category_id].regular_expressions.append(regular_expression)
    return [categories[key] for key in categories.keys()]

class DbQuery:
    def __init__(self, content, params = ()):
        self.content = content
        self.params = params