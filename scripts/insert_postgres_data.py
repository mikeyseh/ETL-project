import os
import logging
import psycopg2
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
postgres_host = os.getenv('POSTGRES_URL_FOR_INSERTION')
postgres_db = os.getenv('POSTGRES_DB')
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_port = os.getenv('POSTGRES_PORT')

try:
    # Connect to the PostgreSQL database
    logging.info("Connecting to the database...")
    conn = psycopg2.connect(
        host = postgres_host,
        database = postgres_db,
        user = postgres_user,
        password = postgres_password,
        port = postgres_port
    )
    cur = conn.cursor()
    logging.info("Connection successful.")

    # Create the employees table if it doesn't exist
    logging.info("Creating the employees table...")
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS employees (
        code SERIAL PRIMARY KEY,
        nom VARCHAR(100) NOT NULL,
        salaire NUMERIC(10, 2)
    );
    '''
    cur.execute(create_table_query)
    conn.commit()  # Commit the creation of the table
    logging.info("Employees table created successfully.")

    # SQL query to insert data
    insert_query = '''
    INSERT INTO employees (nom, salaire) 
    VALUES (%s, %s);
    '''

    # Values to insert
    employees_data = [
        ('Jean Dupont', 3500.00),
        ('Marie Durand', 4200.50),
        ('Pierre Martin', 2800.75)
    ]

    logging.info("Inserting data into the employees table...")
    # Insert data
    for employee in employees_data:
        cur.execute(insert_query, employee)

    conn.commit()  # Commit the inserted data
    logging.info("Data inserted successfully into the employees table.")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()
    logging.info("Connection closed.")
