import sqlite3
import json

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('reviews_database.db')
    cursor = conn.cursor()

    # Create the product_reviews table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_reviews (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            product_name TEXT,
            review_text TEXT
        )
    ''')
    conn.commit()

    # Read data from the reviews.json file
    with open('reviews.json', 'r', encoding='utf-8') as json_file:
        products_reviews = json.load(json_file)

        for product_reviews in products_reviews:  # Loop through each product's reviews
            product_id = product_reviews[0]['product_id']
            product_name = product_reviews[0]['product_name']

            for review in product_reviews:  # Loop through each review of the product
                review_text = review['review_text']

                # Insert the data into the product_reviews table
                cursor.execute('''
                    INSERT INTO product_reviews (product_id, product_name, review_text)
                    VALUES (?, ?, ?)
                ''', (product_id, product_name, review_text))
                conn.commit()

                print(f"Inserted review for Product ID: {product_id}")

    conn.close()

if __name__ == '__main__':
    main()
