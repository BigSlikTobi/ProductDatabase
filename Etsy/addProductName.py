import sqlite3

def add_product_name_column():
    conn = sqlite3.connect('product_database.db')
    cursor = conn.cursor()

    # Add the product_name column to the product_reviews table
    cursor.execute("ALTER TABLE product_reviews ADD COLUMN product_name TEXT")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_product_name_column()
