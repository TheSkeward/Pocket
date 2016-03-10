#! py -3

import sqlite3
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect("pocket.db")
c = conn.cursor()
logging.info("Connected to pocket.db")

# Create the triggers table if it doesn't exist
query = open('pocket.sql', 'r').read()
c.executescript(query)
conn.commit()

query = open("sample.sql", 'r').read()
c.executescript(query)
conn.commit()

c.close()
conn.close()
