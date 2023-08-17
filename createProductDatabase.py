import sqlite3
import requests
from bs4 import BeautifulSoup
import json

def get_product_data(url):
    full_url = "https://" + url  # Add the scheme and the prefix otto.de
    try:
        response = requests.get(full_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        product_name = soup.find('h1', class_='pdp_variation-name').text.strip()
        product_description = soup.find('div', class_='pdp_description__text-expander').text.strip()
        review_link = soup.find('a', class_='cr_js_customerReviewPageLink')
        review_url = review_link['href'] if review_link else None
        return product_name, product_description, review_url
    except (requests.exceptions.RequestException, AttributeError) as e:
        print(f"Failed to fetch data for URL: {full_url}, Error: {e}")
        return None, None, None

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
            description TEXT,
            review_url TEXT,
            hasReview INTEGER DEFAULT 0
        )
    ''')
    conn.commit()

    # Iterate through product info and fetch data
    for product_info in product_info_list:
        href = product_info['href']
        brand = product_info['brand_name']
        url = 'otto.de' + href  # Add "otto.de" prefix to URL

        product_name, product_description, review_url = get_product_data(url)

        if product_name:
            cursor.execute('''
                INSERT INTO products (url, brand, name, description, review_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (url, brand, product_name, product_description, review_url))
            conn.commit()
            print("Inserted data for:", product_name)

    conn.close()

if __name__ == '__main__':
    main()
