import psycopg2

def connection():
    conn = psycopg2.connect(
        host="localhost",
        password="ilikeschool",
        user="postgres",
        port="5432",
        database="postgres"
    )
    return conn

def connection1():
    conn = psycopg2.connect(
        host="localhost",
        password="ilikeschool",
        user="postgres",
        port="5432",
        database="postgres"
    )
    return conn