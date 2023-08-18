import sqlite3

def count_items_in_table(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    
    conn.close()
    return count

if __name__ == '__main__':
    db_path = 'product_database.db'  # Replace with your database path
    table_name = 'products'  # Replace with your table name
    
    item_count = count_items_in_table(db_path, table_name)
    print(f"Number of items in the '{table_name}' table: {item_count}")
