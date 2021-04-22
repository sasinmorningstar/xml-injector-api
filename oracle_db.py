import cx_Oracle
import config


# Defining and setting the database variables

# DATABASE_HOSTNAME = ""
# DATABASE_PORT = ""
# DATABASE_SID = ""




# Make sure to comment both the connection methods before executing the code as we are attempting to establish connection with the database in the "add_data" function itself.

# Connecting to the oracle database, standalone connections
# Method1
# connection = None
# try:
#     connection = cx_Oracle.connect(f'oe/oracle@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_SID}')
    
#     # Show the version of the Oracle Database
#     print(connection.version)

# except cx_Oracle.Error as error:
#     print(error)

# finally:
#     if connection:
#         connection.close()



# Method2
# connection = None
# try:
#     connection = cx_Oracle.connect(config.username, config.password, config.dsn, encoding=config.encoding)

#     # Show the version of the Oracle Database
#     print(connection.version)

# except cx_Oracle.Error as error:
#     print(error)

# finally:
#     # Release the connection
#     if connection:
#         connection.close()



def add_row(family, message_type, businessObjectId):
    query = ('insert into details(family, message_type, businessObjectId)' 'values(:family,:message_type,::businessObjectId)')

    try:
        with cx_Oracle.connect(config.username, config.password, config.dsn, encoding=config.encoding) as connection:
            
            with connection.cursor() as cursor:
                cursor.execute(query, [family, message_type, businessObjectId])

                connection.commit()

    except cx_Oracle.Error as error:
        print('Error Occured:')
        print(error)
