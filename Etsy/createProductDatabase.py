import sqlite3
import requests
from bs4 import BeautifulSoup
import json

def get_product_data(url):
    full_url = url  # Add the scheme and the prefix otto.de
    try:
        response = requests.get(full_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        product_name = soup.find('h1', class_='wt-text-body-01 wt-line-height-tight wt-break-word wt-mt-xs-1').text.strip()
        product_description = soup.find('p', class_='wt-text-body-01 wt-break-word').text.strip()
        return product_name, product_description
    except (requests.exceptions.RequestException, AttributeError) as e:
        print(f"Failed to fetch data for URL: {full_url}, Error: {e}")
        return None, None

def main():
    # Load product info data from JSON
    with open('product_info.json', 'r') as json_file:
        product_info_list = json.load(json_file)

    # Create SQLite database and table
    conn = sqlite3.connect('product_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            brand TEXT,
            name TEXT,
            description TEXT
        )
    ''')
    conn.commit()

    # Iterate through product info and fetch data
    for product_info in product_info_list:
        href = product_info['href']
        brand = product_info['brand_name']
        url = href  

        product_name, product_description = get_product_data(url)

        if product_name:
            cursor.execute('''
                INSERT INTO products (url, brand, name, description)
                VALUES (?, ?, ?, ?)
            ''', (url, brand, product_name, product_description))
            conn.commit()
            print("Inserted data for:", product_name)

if __name__ == '__main__':
    main()
