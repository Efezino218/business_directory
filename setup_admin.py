from werkzeug.security import generate_password_hash
import psycopg2
from connect import get_db_connection, create_tables
import mysql.connector
from mysql.connector import Error


# ______________________________________________________________________________
# __________________Comment Or Uncomment For POATGRES DATABASE SETUP_______________
# -------------------------------------------------------------------------------

def setup_admin(username, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO admin (username, password) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING", (username, hashed_password))
            conn.commit()
            cur.close()
            print("Admin account created successfully.")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    
    # Set up the initial admin account
    setup_admin('admin', 'admin1234abcd')



# ______________________________________________________________________________
# __________________Comment Or Uncomment For MSQL DATABASE SETUP_______________
# -------------------------------------------------------------------------------
# def setup_admin(username, password):
#     hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
#     conn = get_db_connection()
#     if conn:
#         try:
#             cur = conn.cursor()
#             cur.execute("""
#                 INSERT INTO admin (username, password) VALUES (%s, %s)
#                 ON DUPLICATE KEY UPDATE password = VALUES(password)
#                 """, (username, hashed_password))
#             conn.commit()
#             cur.close()
#             print("Admin account created or updated successfully.")
#         except mysql.connector.Error as e:
#             print(f"Database error: {e}")
#         finally:
#             conn.close()

# if __name__ == "__main__":
#     setup_admin('admin', 'admin1234abcd')

