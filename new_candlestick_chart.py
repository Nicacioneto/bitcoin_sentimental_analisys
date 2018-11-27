import psycopg2
import datetime
def get_tweets():
    # Connect to an existing database
    conn = psycopg2.connect("dbname=testdb user=nicacio")
    # Open a cursor to perform database operations

    cur = conn.cursor()
    date = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # Query the database and obtain data as Python objects
    # cur.execute("insert into tweets (text, date) VALUES (%s, %s)",('Hello Word', datetime.datetime.utcnow()))

     cur.execute("select * from tweets WHERE date = %s", (datetime.datetime.utcnow(),))
     cur.fetchall()
     # Make the changes to the database persistent
     conn.commit()

     # Close communication with the database
     cur.close()
     conn.close()
