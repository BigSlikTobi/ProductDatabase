import sqlite3

def reset_has_review():
    conn = sqlite3.connect('product_database.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE products SET hasReview = 0")
    conn.commit()

    conn.close()

if __name__ == '__main__':
    reset_has_review()
