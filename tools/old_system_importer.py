import requests
from hashlib import sha512
from getpass import getpass

def main():
    api_url = input('Api url: ')
    password = getpass('Password: ')
    data = fetch_data(api_url, password)
    with open('out.sql', 'w') as file:
        generate_sql(data, file)


def fetch_data(api_url, password):
    response = requests.get('https://' + api_url + '/api/backup/export', headers={
        'Authorization': sha512(password.encode('utf-8')).hexdigest()
    })
    response.raise_for_status()
    return response.json()

def generate_sql(data, file):
    categories_map = map_data_to_category_map(data)
    categories = [categories_map[category_id] for category_id in categories_map.keys()]
    no_category_transactions = filter(lambda t: t['categoryId'] == None, data['transactions'])
    for category in categories:
        query = """
-- CATEGORY {category_name}
INSERT INTO category (name) VALUES ('{category_name}');
SELECT LAST_INSERT_ID() INTO @inserted_category_id;
        """
        if len(category['regexps']) != 0:
            query += '\nINSERT INTO regular_expression (category_id, content) VALUES {regexp_values};'
        if len(category['transactions']) != 0:
            query += '\nINSERT INTO account_transaction (title, date, amount, create_date, category_id) VALUES {transaction_values};'
        transaction_values=', \n'.join(
            [ 
                """('{}', '{}', {}, CURRENT_TIMESTAMP(), @inserted_category_id)"""
                .format(escape_special(t['title']), convert_date(t['date']), t['amount']) for t in category['transactions'] 
            ]
        )
        regexp_values=', '.join(
            [
                """(@inserted_category_id, '{}')""".format(regexp['content']) for regexp in category['regexps'] 
            ]
        )
        query = query.format(
            category_name=category['category']['name'],
            regexp_values=regexp_values,
            transaction_values=transaction_values
        )
        file.write(query)


def convert_date(date):
    parts = date.split('-')
    return parts[2] + '-' + parts[1] + '-' + parts[0]

def escape_special(text):
    return text.replace("'", "''")

def map_data_to_category_map(data):
    categories = {}
    for category in data['categories']:
        categories[category['id']] = {
            'category': category,
            'regexps': [],
            'transactions': []
        }
    for regexp in data['regexps']:
        categories[regexp['categoryId']]['regexps'].append(regexp)
    for transaction in filter(lambda t: t['categoryId'] != None, data['transactions']):
        categories[transaction['categoryId']]['transactions'].append(transaction)
        
    return categories

main()