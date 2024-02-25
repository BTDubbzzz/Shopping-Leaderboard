import psycopg2
from config import DB_CONFIG

DB_NAME = DB_CONFIG['dbname']
DB_USER = DB_CONFIG['user']
DB_PASSWORD = DB_CONFIG['password']
DB_HOST = DB_CONFIG['host']

def connect_db():
    try:
        return psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
        return None

def add_shopping_trip(conn, date, total):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO shopping_trips (date, total) VALUES (%s, %s)",
            (date, total)
        )
        conn.commit()

def add_user_guess(conn, user_id, date, guess):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO user_guesses (user_id, date, guess) VALUES (%s, %s, %s)",
            (user_id, date, guess)
        )
        conn.commit()

def add_user(conn, name):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO users (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (name,))
        conn.commit()

def fetch_all_users(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT user_id, name FROM users ORDER BY name")
        return cur.fetchall()

def calculate_leaderboard(conn):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT u.name, SUM(ABS(ug.guess - st.total)) AS total_difference
        FROM user_guesses ug
        JOIN shopping_trips st ON ug.date = st.date
        JOIN users u ON ug.user_id = u.user_id
        GROUP BY u.name
        ORDER BY total_difference ASC
        """)
        leaderboard = cur.fetchall()
    return leaderboard