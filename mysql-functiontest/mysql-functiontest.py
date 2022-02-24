import argparse
import MySQLdb
import sys

# Database name to create temporarily for testing
DATABASENAME = "functiontest1337"

def argument_parser():
    parser = argparse.ArgumentParser(prog='mysql-functiontest', add_help=False)
    parser.add_argument("-u", "--user", action='store', dest="user", type=ascii, help="mysql user to use for testing.", required=True)
    parser.add_argument("-p", "--password",  action='store', dest="password", type=ascii, help="Password for the user to test.", required=True)
    parser.add_argument("-h", "--host",  action='store', dest="host", type=ascii, help="DNS or IP for the host DB.", required=True)
    args = parser.parse_args()
    return args

def connect_to_server(user, password, host):
    print("Connecting to server.")
    try:
        db = MySQLdb.connect(host=host, user=user, passwd=password)
    except Exception as connservererr:
        print(f"Unable to connect to MySQL server: {connservererr}")
        sys.exit(1)
    return db

def create_db(dbcursor):
    print("Creating database.")
    try:
        dbcursor.execute(f"DROP DATABASE IF EXISTS {DATABASENAME}")
        dbcursor.execute(f"CREATE DATABASE {DATABASENAME}")
    except Exception as createdberr:
        print(f"Unable to create test database: {createdberr}")
        sys.exit(1)

def connect_to_db(user, password, host, database):
    print("Connecting to server + db.")
    try:
        db = MySQLdb.connect(host=host, user=user, passwd=password, database=database)
    except Exception as conndberr:
        print(f"Unable to connect to database: {conndberr}")
        sys.exit(1)
    return db

def create_table(dbcursor):
    print("Creating test table.")
    try:
        dbcursor.execute("CREATE TABLE TESTTABLE(id INT PRIMARY KEY, value VARCHAR(255))")
    except Exception as createtableerr:
        print(f"Unable to create table: {createtableerr}")
        sys.exit(1)

def add_value(dbcursor):
    print("Adding value to table.")
    sql = "INSERT INTO TESTTABLE (id, value) VALUES (%s, %s)"
    val = ('1000', "abcdef")
    dbcursor.execute(sql, val)

def verify_value(dbcursor):
    print("Verifying value.")
    dbcursor.execute("SELECT * FROM TESTTABLE")
    data = dbcursor.fetchall()
    for record in data:
        print(record)
        if "abcdef" in record:
            return True
    return False

def drop_database(dbcursor):
    print("Dropping database.")
    try:
        dbcursor.execute(f"DROP DATABASE IF EXISTS {DATABASENAME}")
    except Exception as dropdberr:
        print(f"Unable to drop database: {dropdberr}")


def main():
    args = argument_parser()

    user = args.user
    password = args.password
    host = args.host

    user = user.strip('\'')
    password = password.strip('\'')
    host = host.strip('\'')

    db = connect_to_server(user, password, host)
    dbcursor = db.cursor()
    create_db(dbcursor)

    # close connection
    print("Closing connection.")
    dbcursor.close()
    db.close()

    # Connect to server + database
    db = connect_to_db(user, password, host, DATABASENAME)
    dbcursor = db.cursor()

    # create table
    create_table(dbcursor)
    db.commit()

    # add value
    add_value(dbcursor)
    db.commit()

    # verify value
    if verify_value(dbcursor):
        print("Verification passed. *** All OK ***")
        verified = True
    else:
        print("Verification failed.")
        verified = False

    # drop database
    drop_database(dbcursor)
    db.commit()

    # close connection
    print("Closing connection.")
    dbcursor.close()
    db.close()

    # exit with return code
    if verified:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()