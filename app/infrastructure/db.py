import os
import psycopg2

def get_connection():
    try:
        dsn = os.environ.get('DATABASE_URL')
        return psycopg2.connect(dsn)
    except Exception as e:
        logger.warn("--- DATABASE CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DATABASE CONNECTION ERROR ---")
