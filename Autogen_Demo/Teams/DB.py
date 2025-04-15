import sqlite3

def get_db_summary(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Step 1: Get tables
    tables = get_table_names(cursor)
    
    db_summary = {}
    
    # Step 2: Get schema, row count, and relationships for each table
    for table in tables:
        schema = get_table_schema(cursor, table)
        row_count = get_row_count(cursor, table)
        foreign_keys = get_table_foreign_keys(cursor, table)
        
        db_summary[table] = {
            'schema': schema,
            'row_count': row_count,
            'foreign_keys': foreign_keys
        }
    
    conn.close()
    return db_summary

# Functions for retrieving data
def get_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in cursor.fetchall()]

def get_table_schema(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    return cursor.fetchall()

def get_row_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    return cursor.fetchone()[0]

def get_table_foreign_keys(cursor, table_name):
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    return cursor.fetchall()

# Example usage:
db_path = 'chinook.db'
summary = get_db_summary(db_path)
for table, info in summary.items():
    print(f"Table: {table}")
    print(f"Schema: {info['schema']}")
    print(f"Row Count: {info['row_count']}")
    print(f"Foreign Keys: {info['foreign_keys']}")
    print("\n")
