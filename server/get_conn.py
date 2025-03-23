import urllib.parse
import os

def get_connection_uri():

    # Read URI parameters from the environment
    dbhost = 'tradingbot.postgres.database.azure.com'
    print("dbhost:", dbhost)
    dbname = 'postgres'
    dbuser = urllib.parse.quote('datchuan')
    password = 'tradingbot25@'
    sslmode = 'require'
    db_uri = f"host={dbhost} dbname={dbname} user={dbuser} password={password} sslmode ={sslmode}"
    # Construct connection URI
    return db_uri