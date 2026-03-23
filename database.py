import psycopg2

connection = psycopg2.connect(
    host ="localhost",
    database="crypto_db",
    user="geckosayian",
    password="pass"
)
cursor = connection.cursor()