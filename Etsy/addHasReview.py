import sqlite3

def main():
    conn = sqlite3.connect('product_database.db')
    cursor = conn.cursor()

    # Add the 'hasReview' column to the 'products' table
    cursor.execute("ALTER TABLE products ADD COLUMN hasReview INTEGER DEFAULT 0")
    conn.commit()

    conn.close()

if __name__ == '__main__':
    main()
