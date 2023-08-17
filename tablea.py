import psycopg2
from psycopg2 import Error


conn = psycopg2.connect(
        host="dpg-ci1covndvk4kgoo1fcj0-a.oregon-postgres.render.com",
        port="5432",
        database="telegrambot_dy64",
        user="telegram",
        password="9gz5OWp5bAcxf0PxXgGvXp9peW6WKqCP"
    )


# Function to create the table in the database
def create_table() -> None:

    try:
        # Create a cursor object to interact with the database
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")

        # Define the SQL statement to create the table
        # sql = """
        #     DROP TABLE IF EXISTS users;
        #     CREATE TABLE IF NOT EXISTS users (
        #         chat_id BIGINT PRIMARY KEY,
        #         api_key VARCHAR(255),
        #         main_id VARCHAR(255),
        #         cancel_flag BOOLEAN
        #     )
        # """

        # # Execute the SQL statement to create the table
        # cursor.execute(sql)

        # Commit the transaction to save the changes
        conn.commit()

        # Close the cursor and database conn
        cursor.close()
        conn.close()

        print("Table created successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while creating table:", error)

create_table()