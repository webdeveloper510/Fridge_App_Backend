import mysql.connector

# Database connection details
host = 'db5013126247.hosting-data.io'
database = 'dbs11016943'
user = 'dbu5440706'
password = 'adminadmin@123123'

# Establish database connection
try:
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    if connection.is_connected():
        print('Connected to the database')
        # Perform database operations here
        # ...
except mysql.connector.Error as e:
    print('Error connecting to the database:', str(e))
