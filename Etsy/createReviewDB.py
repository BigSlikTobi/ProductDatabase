import sqlite3
import json

# Open the JSON file and load the data
with open("reviews.json", "r") as json_file:
    data = json.load(json_file)

# Connect to the SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect("product_reviews.db")
cursor = conn.cursor()

# Create a table to store product reviews
cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_reviews (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        product_name TEXT,
        product_url TEXT,
        review_text TEXT,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
""")

# Loop through the JSON data and insert it into the database
for product_reviews in data:
    for review in product_reviews:
        product_id = review["product_id"]
        product_name = review["product_name"]
        product_url = review["product_url"]
        review_text = review["review_text"]
        
        # Insert the data into the product_reviews table
        cursor.execute("""
            INSERT INTO product_reviews (product_id, product_name, product_url, review_text)
            VALUES (?, ?, ?, ?)
        """, (product_id, product_name, product_url, review_text))

# Commit the changes and close the database connection
conn.commit()
conn.close()
