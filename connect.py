import traceback
import psycopg2
import mysql.connector
from mysql.connector import Error


# ______________________________________________________________________________
# __________________Comment Or Uncomment For POSTGRES DATABASE SETUP_______________
# -------------------------------------------------------------------------------

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='business_owners_db', 
            user='postgres', 
            password='postgres'
            )
        print("Successfully connected to database!")
        return conn
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return None
get_db_connection()


def create_tables():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Create the tables if it doesn't exist SQL COMMANDS                       
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_registration_requests (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE
                );
            """)
            cur.execute("""ALTER TABLE user_registration_requests ADD COLUMN IF NOT EXISTS name VARCHAR(250);""")           
            cur.execute("""ALTER TABLE user_registration_requests ADD COLUMN IF NOT EXISTS phone VARCHAR(250);""")           
                        
            
            cur.execute("""         
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    is_approved BOOLEAN DEFAULT FALSE,
                    profile_image TEXT  -- Adding profile_image column directly

            );
            """)
            cur.execute("""ALTER TABLE users ADD COLUMN IF NOT EXISTS suspended BOOLEAN DEFAULT FALSE;""")
            cur.execute("""ALTER TABLE users ADD COLUMN IF NOT EXISTS activation_token TEXT;""")
            cur.execute("""ALTER TABLE users ADD COLUMN IF NOT EXISTS is_activated BOOLEAN DEFAULT FALSE;""")
            cur.execute("""
                        ALTER TABLE users ADD COLUMN IF NOT EXISTS registration_request_id INTEGER REFERENCES user_registration_requests(id) ON DELETE CASCADE;
                    """)
            cur.execute("""ALTER TABLE users ADD COLUMN IF NOT EXISTS name VARCHAR(250);""")           
            cur.execute("""ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(250);""") 
                                    
            cur.execute("""
                ALTER TABLE users
                DROP CONSTRAINT IF EXISTS fk_users_registration_request;
            """)
            cur.execute("""
                ALTER TABLE users
                ADD CONSTRAINT fk_users_registration_request
                FOREIGN KEY (registration_request_id) REFERENCES user_registration_requests(id) ON DELETE CASCADE;
            """) 

            
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS business_registration_requests (
                    id SERIAL PRIMARY KEY,
                    business_name VARCHAR(100) NOT NULL,
                    shop_no VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(20),
                    description TEXT NOT NULL,
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    category VARCHAR(50) NOT NULL,
                    block_num VARCHAR(50)
                );
            """)
            cur.execute("""ALTER TABLE business_registration_requests ADD COLUMN IF NOT EXISTS email VARCHAR(100);""")

           
            cur.execute("""
                CREATE TABLE IF NOT EXISTS businesses (
                    id SERIAL PRIMARY KEY,
                    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    business_name VARCHAR(100) NOT NULL,
                    shop_no VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL,
                    description TEXT NOT NULL,
                    is_subscribed BOOLEAN DEFAULT FALSE,
                    media_type VARCHAR(10) CHECK (media_type IN ('image', 'video')),
                    media_url TEXT,
                    category VARCHAR(50) NOT NULL,
                    block_num VARCHAR(50)
                );
                """)
            cur.execute("""ALTER TABLE businesses ADD COLUMN IF NOT EXISTS email VARCHAR(100);""")
            cur.execute("""ALTER TABLE businesses ADD COLUMN IF NOT EXISTS category VARCHAR(100);""")

            # Populate the category column in the businesses table with data from business_registration_requests
            cur.execute("""
                UPDATE businesses b
                SET category = r.category
                FROM business_registration_requests r
                WHERE b.id = r.id;
            """)




            cur.execute("""
                CREATE TABLE IF NOT EXISTS images_videos (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER REFERENCES businesses(id),
                    media_type VARCHAR(10) CHECK (media_type IN ('image', 'video')),
                    media_url TEXT NOT NULL
                );
                """)


            cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id SERIAL PRIMARY KEY,
                    category_name VARCHAR(255) UNIQUE NOT NULL
                );
                """)


            cur.execute("""
                CREATE TABLE IF NOT EXISTS business_categories (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER REFERENCES businesses(id),
                    category_id INTEGER REFERENCES categories(id)
                );
                """)           
            cur.execute("""ALTER TABLE business_categories ADD CONSTRAINT unique_business_category UNIQUE (business_id, category_id);""")
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS admin (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
            );
            """)
            cur.execute("""ALTER TABLE admin ADD COLUMN IF NOT EXISTS profile_pic VARCHAR(255);""")

            
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS subscription_plans (
                    id SERIAL PRIMARY KEY,
                    plan_name VARCHAR(50) NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL, -- Amount in Naira
                    duration INTEGER NOT NULL, -- Duration in months
                    UNIQUE (plan_name, duration) -- Multi-column unique constraint
                );
                """)   
             
            cur.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id SERIAL PRIMARY KEY,
                    business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
                    subscription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) CHECK (status IN ('pending', 'confirmed')),
                    plan_id INTEGER REFERENCES subscription_plans(id)
                    );
                """)    
            cur.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id SERIAL PRIMARY KEY,
                    subscription_id INTEGER REFERENCES subscriptions(id) ON DELETE CASCADE,
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    amount DECIMAL(10, 2) NOT NULL,
                    payment_status VARCHAR(20) CHECK (payment_status IN ('pending', 'completed')),
                    payment_method VARCHAR(50)
                );
                """)
            
            cur.execute("""INSERT INTO subscription_plans (plan_name, amount, duration) VALUES 
                        ('Monthly', 10000, 1), 
                        ('Yearly', 85000, 12)
                        ON CONFLICT (plan_name, duration) DO NOTHING;""")    
            
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS claim_requests (
                        id SERIAL PRIMARY KEY,
                        business_id INTEGER REFERENCES businesses(id),
                        user_id INTEGER REFERENCES users(id),
                        phone_number VARCHAR(255),
                        email VARCHAR(255),
                        category VARCHAR(255),
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        reviewed BOOLEAN DEFAULT FALSE
                    );                        
                    """)

            
            print("Database tables created successfully")
            conn.commit()

        except psycopg2.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
    else:
        print("Could not open connection to the database")

# Call the function to initialize the database
create_tables()




# ______________________________________________________________________________
# __________________Comment Or Uncomment For MSQL DATABASE SETUP_______________
# -------------------------------------------------------------------------------


# def get_db_connection():
#     try:
#         conn = mysql.connector.connect(
#             host='localhost',
#             database='business_owners_db',
#             user='root',  # Default MySQL username in XAMPP
#             password=''   # Default MySQL password in XAMPP is usually empty
#         )
#         if conn.is_connected():
#             print("Successfully connected to MySQL database!")
#         return conn
#     except Error as e:
#         print(f"Error: {e}")
#     return None

# get_db_connection()



# def create_tables():
#     conn = get_db_connection()
#     if conn:
#         try:
#             cur = conn.cursor()

#             # Drop tables if they exist (for a clean slate)
#             cur.execute("DROP TABLE IF EXISTS claim_requests;")
#             cur.execute("DROP TABLE IF EXISTS payments;")
#             cur.execute("DROP TABLE IF EXISTS subscriptions;")
#             cur.execute("DROP TABLE IF EXISTS subscription_plans;")
#             cur.execute("DROP TABLE IF EXISTS admin;")
#             cur.execute("DROP TABLE IF EXISTS business_categories;")
#             cur.execute("DROP TABLE IF EXISTS categories;")
#             cur.execute("DROP TABLE IF EXISTS images_videos;")
#             cur.execute("DROP TABLE IF EXISTS businesses;")
#             cur.execute("DROP TABLE IF EXISTS business_registration_requests;")
#             cur.execute("DROP TABLE IF EXISTS users;")
#             cur.execute("DROP TABLE IF EXISTS user_registration_requests;")

#             # Create tables with foreign key constraints
#             cur.execute("""
#                 CREATE TABLE user_registration_requests (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     username VARCHAR(50) UNIQUE NOT NULL,
#                     password TEXT NOT NULL,
#                     email VARCHAR(100) UNIQUE NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     processed BOOLEAN DEFAULT FALSE,
#                     name VARCHAR(250),
#                     phone VARCHAR(250)
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE users (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     username VARCHAR(255) UNIQUE NOT NULL,
#                     email VARCHAR(100) UNIQUE NOT NULL,
#                     password VARCHAR(255) NOT NULL,
#                     is_admin BOOLEAN DEFAULT FALSE,
#                     is_approved BOOLEAN DEFAULT FALSE,
#                     profile_image TEXT,
#                     suspended BOOLEAN DEFAULT FALSE,
#                     activation_token TEXT,
#                     is_activated BOOLEAN DEFAULT FALSE,
#                     registration_request_id INT,
#                     name VARCHAR(250),
#                     phone VARCHAR(250),
#                     FOREIGN KEY (registration_request_id) REFERENCES user_registration_requests(id) ON DELETE CASCADE
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE business_registration_requests (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     business_name VARCHAR(100) NOT NULL,
#                     shop_no VARCHAR(100) NOT NULL,
#                     phone_number VARCHAR(20),
#                     description TEXT NOT NULL,
#                     processed BOOLEAN DEFAULT FALSE,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     user_id INT,
#                     category VARCHAR(50) NOT NULL,
#                     block_num VARCHAR(50),
#                     email VARCHAR(100),
#                     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE businesses (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     owner_id INT,
#                     business_name VARCHAR(100) NOT NULL,
#                     shop_no VARCHAR(100) NOT NULL,
#                     phone_number VARCHAR(20) NOT NULL,
#                     description TEXT NOT NULL,
#                     is_subscribed BOOLEAN DEFAULT FALSE,
#                     media_type ENUM('image', 'video'),
#                     media_url TEXT,
#                     category VARCHAR(50) NOT NULL,
#                     block_num VARCHAR(50),
#                     email VARCHAR(100),
#                     FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE images_videos (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     business_id INT,
#                     media_type ENUM('image', 'video'),
#                     media_url TEXT NOT NULL,
#                     FOREIGN KEY (business_id) REFERENCES businesses(id)
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE categories (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     category_name VARCHAR(255) UNIQUE NOT NULL
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE business_categories (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     business_id INT,
#                     category_id INT,
#                     FOREIGN KEY (business_id) REFERENCES businesses(id),
#                     FOREIGN KEY (category_id) REFERENCES categories(id),
#                     UNIQUE (business_id, category_id)
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE admin (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     username VARCHAR(255) UNIQUE NOT NULL,
#                     password VARCHAR(255) NOT NULL,
#                     profile_pic VARCHAR(255)
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE subscription_plans (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     plan_name VARCHAR(50) NOT NULL,
#                     amount DECIMAL(10, 2) NOT NULL,
#                     duration INT NOT NULL,
#                     UNIQUE (plan_name, duration)
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE subscriptions (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     business_id INT,
#                     subscription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     status ENUM('pending', 'confirmed'),
#                     plan_id INT,
#                     FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE,
#                     FOREIGN KEY (plan_id) REFERENCES subscription_plans(id)
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE payments (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     subscription_id INT,
#                     payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     amount DECIMAL(10, 2) NOT NULL,
#                     payment_status ENUM('pending', 'completed'),
#                     payment_method VARCHAR(50),
#                     FOREIGN KEY (subscription_id) REFERENCES subscriptions(id) ON DELETE CASCADE
#                 );
#             """)

#             cur.execute("""
#                 CREATE TABLE claim_requests (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     business_id INT,
#                     user_id INT,
#                     phone_number VARCHAR(255),
#                     email VARCHAR(255),
#                     category VARCHAR(255),
#                     description TEXT,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     reviewed BOOLEAN DEFAULT FALSE,
#                     FOREIGN KEY (business_id) REFERENCES businesses(id),
#                     FOREIGN KEY (user_id) REFERENCES users(id)
#                 );
#             """)

#             print("Database tables created successfully")
#             conn.commit()

#         except mysql.connector.Error as e:
#             print(f"Database error: {e}")
#         except Exception as e:
#             print(f"Error: {e}")
#         finally:
#             cur.close()
#             conn.close()
#     else:
#         print("Could not open connection to the database")

# # Call the function to initialize the database
# create_tables()



"""#SQL COMMAND TO DELETE A USER FROM TABLE and also to DELETE A TABLE THAT IS REFERENCE TO OTHERS TABLESBELOW:
DELETE FROM tablename WHERE id = 5;

DROP TABLE IF EXISTS subscription_plans CASCADE;

"""







