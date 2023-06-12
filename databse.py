import psycopg2
from psycopg2 import Error
import asyncio
import pickle


def save_api_key(chat_id, api_key):
    conn = psycopg2.connect(
        host="dpg-ci1covndvk4kgoo1fcj0-a.oregon-postgres.render.com",
        port="5432",
        database="telegrambot_dy64",
        user="telegram",
        password="9gz5OWp5bAcxf0PxXgGvXp9peW6WKqCP"
    )

    try:
        cursor = conn.cursor()
        query = "INSERT INTO users (chat_id, api_key) VALUES (%s, %s) ON CONFLICT (chat_id) DO UPDATE SET api_key = EXCLUDED.api_key"
        cursor.execute(query, (chat_id, api_key))
        conn.commit()

    except (Exception, Error) as error:
        print("Error while saving API key:", error)
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_api_key(chat_id):
    conn = psycopg2.connect(
        host="dpg-ci1covndvk4kgoo1fcj0-a.oregon-postgres.render.com",
        port="5432",
        database="telegrambot_dy64",
        user="telegram",
        password="9gz5OWp5bAcxf0PxXgGvXp9peW6WKqCP"
    )

    try:
        cursor = conn.cursor()
        select_query = f"SELECT api_key FROM users WHERE chat_id = '{chat_id}'"
        cursor.execute(select_query)
        api_key = cursor.fetchone()
        return api_key[0] if api_key else None
    except (Exception, Error) as error:
        print("Error while retrieving API key:", error)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def save_main_id(chat_id: int, main_id: str) -> None:
    conn = psycopg2.connect(
        host="dpg-ci1covndvk4kgoo1fcj0-a.oregon-postgres.render.com",
        port="5432",
        database="telegrambot_dy64",
        user="telegram",
        password="9gz5OWp5bAcxf0PxXgGvXp9peW6WKqCP"
    )

    try:
        cursor = conn.cursor()

        query = "INSERT INTO users (chat_id, main_id) VALUES (%s, %s) ON CONFLICT (chat_id) DO UPDATE SET main_id = EXCLUDED.main_id"
        cursor.execute(query, (chat_id, main_id))
        conn.commit()
        cursor.close()
        conn.close()
        print("Main ID saved successfully.")
    except (Exception, psycopg2.Error) as error:
        print("Error while saving Main ID:", error)
    
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_main_id(chat_id: int) -> str:

    conn = psycopg2.connect(
        host="dpg-ci1covndvk4kgoo1fcj0-a.oregon-postgres.render.com",
        port="5432",
        database="telegrambot_dy64",
        user="telegram",
        password="9gz5OWp5bAcxf0PxXgGvXp9peW6WKqCP"
    )

    try:       
        cursor = conn.cursor()
        sql = "SELECT main_id FROM users WHERE chat_id = %s"
        cursor.execute(sql, (chat_id,))
        main_id = cursor.fetchone()

        cursor.close()
        conn.close()

        if main_id:
            return main_id[0]
        else:
            return None
    except (Exception, psycopg2.Error) as error:
        print("Error while retrieving MAIN ID:", error)
        return None


def get_cancel_flag(chat_id):

    conn = psycopg2.connect(
        host="dpg-ci1covndvk4kgoo1fcj0-a.oregon-postgres.render.com",
        port="5432",
        database="telegrambot_dy64",
        user="telegram",
        password="9gz5OWp5bAcxf0PxXgGvXp9peW6WKqCP"
    )

    cursor = conn.cursor()

    query = "SELECT cancel_flag FROM users WHERE chat_id = %s"
    cursor.execute(query, (chat_id,))
    result = cursor.fetchone()
    if result:
        serialized_cancel_flag = result[0]
        print(serialized_cancel_flag)
        cancel_flag = pickle.loads(serialized_cancel_flag)
    else:
        cancel_flag = asyncio.Event()
    return cancel_flag



def save_cancel_flag(chat_id, cancel_flag):
    conn = psycopg2.connect(
        host="dpg-ci1covndvk4kgoo1fcj0-a.oregon-postgres.render.com",
        port="5432",
        database="telegrambot_dy64",
        user="telegram",
        password="9gz5OWp5bAcxf0PxXgGvXp9peW6WKqCP"
    )

    cursor = conn.cursor()
    serialized_cancel_flag = pickle.dumps(cancel_flag)
    query = "INSERT INTO users (chat_id, cancel_flag) VALUES (%s, %s) ON CONFLICT (chat_id) DO UPDATE SET cancel_flag = EXCLUDED.cancel_flag"
    cursor.execute(query, (chat_id, serialized_cancel_flag))
    conn.commit()
    cursor.close()
    conn.close()