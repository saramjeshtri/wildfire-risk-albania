import psycopg2

def get_connection():
    db = psycopg2.connect(
        dbname="wildfire_risk_albania",
        user="saramjeshtri",
        host="localhost",
        port="5432"
    )
    return db