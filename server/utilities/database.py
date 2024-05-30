from dotenv import load_dotenv
import os
from psycopg2 import pool

load_dotenv()
connection_pool = None

db_config = {
    "host": os.environ.get('DB_HOSTNAME'),
    "port": os.environ.get('DB_PORT'),
    "database": os.environ.get('DB_DATABASE'),
    "user": os.environ.get('DB_USERNAME'),
    "password": os.environ.get('DB_PASSWORD'),
    "sslmode": os.environ.get('DB_SSL_MODE')
}

def create_db_connection_pool():
    global connection_pool
    try:
        # Create a connection pool
        connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            **db_config
        )
        print("Connection pool created successfully.")
        return connection_pool
    except Exception as e:
        print("Error creating connection pool:", e)
        return None

def get_connection(connection_pool):
    try:
        # Get a connection from the pool
        connection = connection_pool.getconn()
        print("Connection retrieved from pool.")
        return connection
    except Exception as e:
        print("Error getting connection from pool:", e)
        return None

def release_connection(connection_pool, connection):
    try:
        # Release the connection back to the pool
        connection_pool.putconn(connection)
        print("Connection released back to pool.")
    except Exception as e:
        print("Error releasing connection to pool:", e)

def execute_query(query, params=None, db_context='default'):
    print(query, params)
    
    global connection_pool  
    if(connection_pool == None):
        connection_pool = create_db_connection_pool()
    
    connection = None
    cursor = None
    try:
        # Get a connection from the pool
        connection = get_connection(connection_pool)
        if connection:
            # Create a cursor
            cursor = connection.cursor()

            # Execute the query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Fetch all results for SELECT queries
            if query.strip().upper().startswith('SELECT'):
                return [dict(zip([desc[0] for desc in cursor.description], record)) for record in cursor.fetchall()]
            
            # Commit the transaction for other DML queries (INSERT, UPDATE, DELETE)
            elif query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                connection.commit()
                return f"Query executed successfully. {cursor.rowcount} rows affected."
            
            # For other types of queries (DDL), return a success message
            else:
                return "Query executed successfully."
    except Exception as e:
        print("Error executing query:", e)
        return None
    finally:
        # Close cursor
        if cursor:
            cursor.close()

        # Release connection back to the pool
        if connection:
            release_connection(connection_pool, connection)
