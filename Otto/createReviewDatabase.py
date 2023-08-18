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
            review_title TEXT,
            review_text TEXT
        )
    ''')
    conn.commit()

    # Read data from the reviews.json file
    with open('reviews.json', 'r', encoding='utf-8') as json_file:
        reviews_data = json.load(json_file)

        for reviews in reviews_data:  # Loop through each product's reviews
            for review in reviews:
                product_id = review['product_id']
                product_name = review['product_name']
                review_title = review['review_title']
                review_text = review['review_text']

                # Insert the data into the product_reviews table
                cursor.execute('''
                    INSERT INTO product_reviews (product_id, product_name, review_title, review_text)
                    VALUES (?, ?, ?, ?)
                ''', (product_id, product_name, review_title, review_text))
                conn.commit()

                print(f"Inserted review for Product ID: {product_id}")

    conn.close()

if __name__ == '__main__':
    main()
