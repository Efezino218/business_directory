from flask import Flask, request, redirect, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from connect import get_db_connection  # Import the get_db_connection function
from werkzeug.utils import secure_filename
import re, os
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import socket



# from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for session management
# csrf = CSRFProtect(app)

# // Password Reset Configuration //#
# Set up the configuration for flask_mail.
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
# //update it with your gmail
app.config['MAIL_USERNAME'] = 'efezinorich@gmail.com'
# //update it with your password
app.config['MAIL_PASSWORD'] = 'pmro zhcu hxkd iwwq'
app.config['MAIL_USE_SSL'] = True

# Create an instance of Mail.
mail = Mail(app)
# Configure URLSafeTimedSerializer
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
# Define the route and send mail, Just to test If The App can send email out.

@app.route("/send_email")
def send_email():
  msg = Message('Hello from the other side!', sender = 'efezinorich@gmail.com', recipients = ['cyjustwebsolution@gmail.com'])
  msg.body = "hey, sending out email from flask!!!"
  msg.html = "<h1>Message Sent</h1>"
  mail.send(msg)
  return msg.html
# // Password Reset Configuration //#

# UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = "./static/uploads" #we specify the path the image will be uploaded 
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024  # 60 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'wmv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# UPLOAD Images and Videos Function
def upload_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename  
    return None


### Routes for User and Business Registration ###
@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        
        categories = []
        
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                
                # Check if username or email already exists in user_registration_requests or users
                cur.execute("SELECT * FROM user_registration_requests WHERE username = %s OR email = %s", (username, email))
                existing_user_request = cur.fetchone()
                
                cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
                existing_user = cur.fetchone()

                if existing_user_request or existing_user:
                    flash("Username or email already exists. Please try again with different credentials.", 'error')
                    return redirect(url_for('register_user'))

                else:
                    # Insert the registration request into user_registration_requests table
                    cur.execute("""
                        INSERT INTO user_registration_requests (username, password, email, name, phone)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (username, generate_password_hash(password, method='pbkdf2:sha256'), email, name, phone))
                    
                    conn.commit()
                    flash("Registration request submitted successfully. Your account will be created after admin approval.", 'success')
                
                cur.close()
                conn.close()
                return redirect(url_for('index'))
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                flash("Error occurred during registration.", 'error')
            finally:
                conn.close()
        else:
            flash("Could not connect to the database.", 'error')
            
    return render_template('register_user.html')




@app.route('/register_business', methods=['GET', 'POST'])
def register_business():
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))

    categories = []  # Initialize categories

    if request.method == 'POST':
        business_name = request.form['business_name']
        shop_no = request.form['shop_no']
        phone_number = request.form['phone_number']
        block_num = request.form['block_num']
        category = request.form['category']
        description = request.form['description']
        email = request.form['email']  # Get email address
        user_id = session.get('user_id')

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # Insert the new business registration request into the database
            cur.execute("""
                INSERT INTO business_registration_requests 
                (business_name, shop_no, phone_number, block_num, category, description, user_id, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (business_name, shop_no, phone_number, block_num, category, description, user_id, email))

            conn.commit()
            flash("Business registration request submitted successfully!", 'success')
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('user_business_profile'))

    elif request.method == 'GET':
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # Fetch categories for the GET request
            cur.execute("SELECT * FROM categories")
            categories = cur.fetchall()
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            cur.close()
            conn.close()

    return render_template('register_business.html', categories=categories)






# @app.route('/register_business', methods=['GET', 'POST'])
# def register_business():
#     if 'user_logged_in' not in session:
#         return redirect(url_for('user_login'))

#     if request.method == 'POST':
#         business_name = request.form['business_name']
#         shop_no = request.form['shop_no']
#         phone_number = request.form['phone_number']
#         block_num = request.form['block_num']
#         category = request.form['category']
#         description = request.form['description']
#         email = request.form['email']  # Get email address
#         user_id = session.get('user_id')

#         conn = get_db_connection()
#         cur = conn.cursor()

#         try:
#             # Insert the new business registration request into the database
#             cur.execute("""
#                 INSERT INTO business_registration_requests 
#                 (business_name, shop_no, phone_number, block_num, category, description, user_id, email)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """, (business_name, shop_no, phone_number, block_num, category, description, user_id, email))

#             conn.commit()
#             flash("Business registration request submitted successfully!", 'success')
#         except psycopg2.Error as e:
#             flash(f"Database error: {e}", 'error')
#         finally:
#             cur.close()
#             conn.close()

#         return redirect(url_for('user_business_profile'))

#     return render_template('register_business.html')

    


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        
        if conn:
            try:
                cur = conn.cursor()
                
                # Check if user exists in users table
                cur.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cur.fetchone()
                
                if user:
                    # User exists in users table
                    stored_password_hash = user[3]  # Assuming password is in the 4th column
                    is_approved = user[5]  # Assuming is_approved is in the 6th column
                    is_suspended = user[7]  # Assuming suspended is in the 8th column
                    
                    # Check if the user's account is suspended
                    if is_suspended:
                        flash("Your account is suspended. Please contact the admin.", 'error')
                    
                    # Check if the user's account is not approved (i.e., not activated)
                    elif not is_approved:
                        flash("Your account is not activated yet. Please check your email for the activation link.", 'error')
                    
                    # Check if the provided password matches the stored password hash
                    elif check_password_hash(stored_password_hash, password):
                        session['user_logged_in'] = True
                        session['user_id'] = user[0]  # Store user_id in the session
                        session['username'] = user[1]
                        session['avatar'] = user[6]
                        
                        # for x in user:
                        #     print(x)
                            
                        flash("Login successful.", 'success')
                        return redirect(url_for('index'))
                    else:
                        flash("Invalid credentials. Please check your password.", 'error')
                
                else:
                    # User not found in users table, check registration requests
                    cur.execute("SELECT * FROM user_registration_requests WHERE username = %s", (username,))
                    registration_request = cur.fetchone()
                    
                    if registration_request:
                        flash("Your account is not approved yet. Please wait for admin approval.", 'error')
                    else:
                        flash("Invalid credentials. User does not exist.", 'error')
                
                cur.close()
                conn.close()
            except psycopg2.Error as e:
                flash(f"Error occurred during login: {e}", 'error')
    return render_template('user_login.html')




## Forgotton password Route and Functions ##

def generate_reset_token(user_id):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(user_id, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None
    return user_id

def send_reset_email(email, token):
    reset_url = url_for('reset_password', token=token, _external=True)
    msg = Message('Password Reset Request', sender='efezinorich@gmail.com', recipients=[email])
    msg.body = f'To reset your password, click the following link: {reset_url}'
    msg.html = f'<p>To reset your password, click the following link: <a href="{reset_url}">{reset_url}</a></p>'
    mail.send(msg)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            token = generate_reset_token(user[0])
            send_reset_email(email, token)
            flash('An email with a password reset link has been sent to your email address.', 'info')
            return redirect(url_for('user_login'))
        else:
            flash('Email address not found.', 'error')
        

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user_id = verify_reset_token(token)
    if not user_id:
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users SET password = %s WHERE id = %s', (hashed_password, user_id))
        conn.commit()
        cur.close()
        conn.close()

        flash('Your password has been updated!', 'success')
        return redirect(url_for('user_login'))

    return render_template('reset_password.html')



# @app.route('/user_login', methods=['GET', 'POST'])
# def user_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         conn = get_db_connection()
        
#         if conn:
#             try:
#                 cur = conn.cursor()
                
#                 # Check if user exists in users table
#                 cur.execute("SELECT * FROM users WHERE username = %s", (username,))
#                 user = cur.fetchone()
                
#                 if user:
#                     # User exists in users table
#                     stored_password_hash = user[3]  # Assuming password is in the 4th column
#                     is_approved = user[5]  # Assuming is_approved is in the 6th column
                    
#                     if not is_approved:
#                         flash("Your account is not approved yet. Please wait for admin approval.", 'error')
#                     elif check_password_hash(stored_password_hash, password):
#                         session['user_logged_in'] = True
#                         session['user_id'] = user[0]  # Store user_id in the session
#                         session['username'] = user[1]
#                         flash("Login successful.", 'success')
#                         return redirect(url_for('index'))
#                     else:
#                         flash("Invalid credentials. Please check your password.", 'error')
#                 else:
#                     # User not found in users table, check registration requests
#                     cur.execute("SELECT * FROM user_registration_requests WHERE username = %s", (username,))
#                     registration_request = cur.fetchone()
                    
#                     if registration_request:
#                         flash("Your account is not approved yet. Please wait for admin approval.", 'error')
#                     else:
#                         flash("Invalid credentials. User does not exist.", 'error')
                
#                 cur.close()
#                 conn.close()
#             except psycopg2.Error as e:
#                 flash(f"Error occurred during login: {e}", 'error')
#     return render_template('user_login.html')



@app.route('/user_business_profile')
def user_business_profile():
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    user_id = session.get('user_id')
    conn = get_db_connection()
    businesses = None
    pending_businesses = None
    subscription_plans = None
    categories = []


    if conn:
        try:
            cur = conn.cursor()

            # Fetch categories
            cur.execute("SELECT * FROM categories")
            categories = cur.fetchall()
                
            # Fetch approved businesses
            cur.execute("""
                SELECT id, business_name, shop_no, phone_number, description, is_subscribed, media_type, media_url, category, email
                FROM businesses
                WHERE owner_id = %s
            """, (user_id,))
            businesses = cur.fetchall()
            
            # Fetch pending business requests
            cur.execute("""
                SELECT id, business_name, shop_no, phone_number, description, created_at
                FROM business_registration_requests
                WHERE user_id = %s AND processed = FALSE
            """, (user_id,))
            pending_businesses = cur.fetchall()
            
            # Fetch subscription plans
            cur.execute("""
                SELECT id, plan_name, amount, duration
                FROM subscription_plans
            """)
            subscription_plans = cur.fetchall()
            
            cur.close()
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            conn.close()

    return render_template('user_business_profile.html', 
                           businesses=businesses, 
                           pending_businesses=pending_businesses,
                           subscription_plans=subscription_plans, categories=categories)



@app.route('/edit_business_media/<int:business_id>', methods=['GET', 'POST'])
def edit_business_media(business_id):
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    user_id = session.get('user_id')
    conn = get_db_connection()
    business = None

    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, business_name, shop_no, phone_number, description, is_subscribed, media_type, media_url, category, email
                FROM businesses
                WHERE owner_id = %s AND id = %s
            """, (user_id, business_id))
            business = cur.fetchone()

            if request.method == 'POST' and business:
                media_type = request.form['media_type']
                file = request.files['file']

                if file and file.filename != '':
                    media_url = upload_file(file)
                    if media_url:
                        cur.execute("""
                            UPDATE businesses
                            SET media_type = %s, media_url = %s
                            WHERE id = %s AND owner_id = %s
                        """, (media_type, media_url, business_id, user_id))
                        conn.commit()
                        flash('Media uploaded successfully.', 'success')
                    else:
                        flash('Invalid file type.', 'error')
                else:
                    flash('No file selected.', 'error')

            cur.close()
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            conn.close()

    return render_template('edit_business_media.html', business=business)

def upload_file(file):
    # Save the file to the server and return the URL
    # This is a placeholder implementation
    file_path = f"static/uploads/{file.filename}"
    file.save(file_path)
    return file_path




## User Update Profile ##

@app.route('/view_profile')
def view_profile():
    if 'user_id' not in session:  # Ensure user is logged in
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()

    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT username, email, profile_image FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()
            cur.close()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            flash('Error fetching user details.', 'error')
            user = None
        finally:
            conn.close()

    if user:
        return render_template('view_profile.html', user=user)
    else:
        flash('User not found.', 'error')
        return redirect(url_for('index'))




@app.route('/profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:  # Assuming user_id is stored in session after login
        flash('Please log in to access your profile.', 'error')
        return redirect(url_for('user_login'))

    user_id = session['user_id']
    conn = get_db_connection()
    categories = []
    
    cur = conn.cursor()
    # Fetch categories
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        file = request.files['profile_image']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') if password else None

        if conn:
            try:
                cur = conn.cursor()

                # Update the username and password if provided
                if username:
                    cur.execute("UPDATE users SET username = %s WHERE id = %s", (username, user_id))
                if hashed_password:
                    cur.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))

                # Handle profile image upload if a file is provided
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    print("session-before", session['avatar'] )
                    # Update the profile_image column in the database
                    cur.execute("UPDATE users SET profile_image = %s WHERE id = %s", (file_path, user_id))
                    session['avatar'] = file_path # re-assigning the image to the new image that was uploaded by the user, so that the user dont need to logout and login before the profile image will show on the navbar
                    print("session-after", session['avatar'] )
                conn.commit()
                flash('Profile updated successfully!', 'success')
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                flash('Error updating profile.', 'error')
            finally:
                cur.close()
                conn.close()

        return redirect(url_for('update_profile'))

    # GET request: fetch the user's current details to display in the form
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT username, email, profile_image FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()
            cur.close()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            flash('Error fetching user details.', 'error')
        finally:
            conn.close()

    return render_template('profile.html', user=user, categories=categories)





### Admin Routes ###
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT * FROM admin WHERE username = %s", (username,))

                admin = cur.fetchone()
                cur.close()
                conn.close()
                
                if admin and check_password_hash(admin[2], password):  # Assuming password is in the 3rd column
                    session['admin_logged_in'] = True
                    session['admin_id'] = admin[0]  # Store admin id in the session
                    session['admin_username'] = admin[1]  # Store admin Username in the session
                    session['admin_profile_pic'] = admin[3]  # Store admin profile_pic in the session

                    
                    flash('Admin has been login sucessful.', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash("Invalid credentials.", 'error')
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                flash("Error occurred during login.", 'error')
    return render_template('admin_login.html')



@app.route('/admin/update_profile', methods=['GET', 'POST'])
def update_admin_profile():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    admin_id = session.get('admin_id')
    conn = get_db_connection()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        email = request.form['email']
        file = request.files.get('profile_pic')

        try:
            cur = conn.cursor()
            
            # Check current password if new password is being updated
            if new_password:
                cur.execute("SELECT password FROM admin WHERE id = %s", (admin_id,))
                current_password_hash = cur.fetchone()[0]
                
                if not check_password_hash(current_password_hash, password):
                    flash('Current password is incorrect.', 'error')
                else:
                    hashed_password = generate_password_hash(new_password)
                    cur.execute("""
                        UPDATE admin
                        SET password = %s
                        WHERE id = %s
                    """, (hashed_password, admin_id))
                    conn.commit()

            # Update username and email if provided
            if username:
                cur.execute("""
                    UPDATE admin
                    SET username = %s
                    WHERE id = %s
                """, (username, admin_id))
                conn.commit()
                
            if email:
                cur.execute("""
                    UPDATE admin
                    SET email = %s
                    WHERE id = %s
                """, (email, admin_id))
                conn.commit()
            
            # Check if the admin wants to update the profile picture
            if file and file.filename:
                profile_pic_url = upload_file(file)
                if profile_pic_url:
                    cur.execute("""
                        UPDATE admin
                        SET profile_pic = %s
                        WHERE id = %s
                    """, (profile_pic_url, admin_id))
                    conn.commit()
                    session['admin_profile_pic'] = profile_pic_url


            flash('Profile updated successfully.', 'success')
            cur.close()
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
 

    # Fetch current admin data
    cur = conn.cursor()
    cur.execute("SELECT * FROM admin WHERE id = %s", (admin_id,))
    admin = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('admin_update_profile.html', admin=admin)





@app.route('/admin/view_profile', methods=['GET'])
def admin_profile():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    admin_id = session.get('admin_id')
    conn = get_db_connection()

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE id = %s", (admin_id,))
        admin = cur.fetchone()
        cur.close()
    except psycopg2.Error as e:
        flash(f"Database error: {e}", 'error')
    finally:
        conn.close()

    if admin:
        return render_template('admin_profile.html', admin=admin)
    else:
        flash('Admin profile not found.', 'error')
        return redirect(url_for('admin_login'))




@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    user_requests = []
    business_requests = []
    users = []
    claim_requests = []
    pending_user_registration_request_count = 0
    pending_business_registration_requests_count = 0
    pending_approved_user_count = 0
    pending_claim_requests_count = 0  # New variable for claim requests count

    if conn:
        try:
            cur = conn.cursor()
            
            # Fetch pending claim requests
            cur.execute("""
                SELECT cr.id, b.business_name, u.username, cr.phone_number, cr.email, cr.category, cr.description, cr.created_at
                FROM claim_requests cr
                JOIN businesses b ON cr.business_id = b.id
                JOIN users u ON cr.user_id = u.id
                WHERE cr.reviewed = FALSE
            """)
            claim_requests = cur.fetchall()
            
            # Count pending claim requests
            cur.execute("SELECT COUNT(*) FROM claim_requests WHERE reviewed = FALSE")
            pending_claim_requests_count = cur.fetchone()[0]

            # Fetch admin profile picture URL
            admin_id = session.get('admin_id')
            cur.execute("SELECT profile_pic FROM admin WHERE id = %s", (admin_id,))
            profile_pic_path = cur.fetchone()[0]
            
            # Fetch all user registration requests
            cur.execute("SELECT * FROM user_registration_requests")
            user_requests = cur.fetchall()
            
            # Fetch all business registration requests
            cur.execute("SELECT * FROM business_registration_requests")
            business_requests = cur.fetchall()
            
            # Fetch all users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Count pending user registration requests
            cur.execute("SELECT COUNT(*) FROM user_registration_requests WHERE processed = FALSE")
            pending_user_registration_request_count = cur.fetchone()[0]
            
            # Count pending business registration requests
            cur.execute("SELECT COUNT(*) FROM business_registration_requests WHERE processed = FALSE")
            pending_business_registration_requests_count = cur.fetchone()[0]
            
            # Count unapproved users
            cur.execute("SELECT COUNT(*) FROM users WHERE is_approved = FALSE")
            pending_approved_user_count = cur.fetchone()[0]
            
            cur.close()
            conn.close()
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            flash("Error occurred during dashboard retrieval.", 'error')
        finally:
            conn.close()

    return render_template('admin_dashboard.html', 
                           user_requests=user_requests, 
                           business_requests=business_requests,  
                           users=users, 
                           pending_user_registration_request_count=pending_user_registration_request_count,
                           pending_business_registration_requests_count=pending_business_registration_requests_count,
                           pending_approved_user_count=pending_approved_user_count,
                           profile_pic_path=profile_pic_path,
                           claim_requests=claim_requests,
                           pending_claim_requests_count=pending_claim_requests_count)  # Pass count to template
  
    
    
    
@app.route('/admin/review_claim/<int:request_id>', methods=['GET', 'POST'])
def review_claim(request_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    print(f"Review Claim function called with request_id: {request_id}")

    conn = get_db_connection()
    try:
        cur = conn.cursor()

        if request.method == 'POST':
            print("Handling POST request")

            # Fetch the claim request details
            cur.execute("""
                SELECT business_id, user_id, phone_number, email, category, description
                FROM claim_requests
                WHERE id = %s
            """, (request_id,))
            claim_request = cur.fetchone()

            if claim_request:
                business_id, user_id, phone_number, email, category_name, description = claim_request
                print(f"Updating business with ID {business_id} to new owner ID {user_id}")

                # Check if the category already exists
                cur.execute("SELECT id FROM categories WHERE category_name = %s", (category_name,))
                category = cur.fetchone()

                # If the category does not exist, insert it
                if category is None:
                    cur.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING id", (category_name,))
                    category_id = cur.fetchone()[0]
                else:
                    category_id = category[0]

                # Update the claim request to mark it as reviewed
                cur.execute("""
                    UPDATE claim_requests
                    SET reviewed = TRUE
                    WHERE id = %s
                """, (request_id,))
                print("Claim request marked as reviewed")

                # Update the businesses table with the new owner and other details from the claim
                cur.execute("""
                    UPDATE businesses
                    SET owner_id = %s,
                        phone_number = %s,
                        email = %s,
                        description = %s,
                        category = %s
                    WHERE id = %s
                """, (user_id, phone_number, email, description, category_name, business_id))
                print("Business ownership, details, and category updated")

                # Link the business with its category
                cur.execute("""
                    INSERT INTO business_categories (business_id, category_id)
                    VALUES (%s, %s)
                    ON CONFLICT (business_id, category_id) DO NOTHING
                """, (business_id, category_id))
                print("Business linked with category")

                conn.commit()  # Ensure all changes are committed
                flash("Claim request approved and business ownership updated!", 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash("Claim request not found.", 'error')

        # Fetch the claim request details for display
        cur.execute("""
            SELECT cr.id, b.business_name, u.username, cr.phone_number, cr.email, cr.category, cr.description
            FROM claim_requests cr
            JOIN businesses b ON cr.business_id = b.id
            JOIN users u ON cr.user_id = u.id
            WHERE cr.id = %s
        """, (request_id,))
        claim_request = cur.fetchone()
        print(f"Claim Request for Display: {claim_request}")

    except psycopg2.Error as e:
        flash('Error occurred during claim review.', 'error')
        print(f"Database error: {e}")
    finally:
        cur.close()
        conn.close()

    return render_template('review_claim.html', claim_request=claim_request)








# @app.route('/admin_dashboard')
# def admin_dashboard():
#     if 'admin_logged_in' not in session:
#         return redirect(url_for('admin_login'))

#     conn = get_db_connection()
#     user_requests = []
#     business_requests = []
#     users = []
#     pending_user_registration_request_count = 0
#     pending_business_registration_requests_count = 0
#     pending_aproved_user_count = 0

    
#     if conn:
#         try:
#             cur = conn.cursor()
#             cur.execute("SELECT * FROM user_registration_requests")
#             user_requests = cur.fetchall()
#             cur.execute("SELECT * FROM business_registration_requests")
#             business_requests = cur.fetchall()
#             cur.execute("SELECT * FROM users")
#             users = cur.fetchall()
#             cur.close()
#             conn.close()
#         except psycopg2.Error as e:
#             print(f"Database error: {e}")
#             flash("Error occurred during dashboard retrieval.", 'error')
#         finally:
#             conn.close()
    
#     return render_template('admin_dashboard.html', user_requests=user_requests, business_requests=business_requests,  users=users)




@app.route('/process_business_registration', methods=['POST'])
def process_business_registration():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    user_id = session.get('user_id')
    business_name = request.form.get('business_name')
    shop_no = request.form.get('shop_no')
    phone_number = request.form.get('phone_number')
    description = request.form.get('description')
    category_name = request.form.get('category')
    block_num = request.form.get('block_num')
    email = request.form.get('email')  # Get email address

    print(f"Processing business registration with: {user_id}, {business_name}, {shop_no}, {phone_number}, {description}, {category_name}, {block_num}, {email}")

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Check if the category already exists
        cur.execute("SELECT id FROM categories WHERE category_name = %s", (category_name,))
        category = cur.fetchone()
        
        # If the category does not exist, insert it
        if category is None:
            cur.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING id", (category_name,))
            category_id = cur.fetchone()[0]
        else:
            category_id = category[0]
        
        # Insert the new business with the correct owner_id and email
        cur.execute("""
            INSERT INTO businesses (owner_id, business_name, shop_no, phone_number, description, block_num, email, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (user_id, business_name, shop_no, phone_number, description, block_num, email, category_name))
        business_id = cur.fetchone()[0]
        
        # Link the business with its category
        cur.execute("INSERT INTO business_categories (business_id, category_id) VALUES (%s, %s)", (business_id, category_id))
        
        # Update the registration request to mark it as processed
        cur.execute("UPDATE business_registration_requests SET processed = TRUE WHERE business_name = %s", (business_name,))
        
        conn.commit()
        flash('Business registered successfully and registration request marked as processed.', 'success')
    except psycopg2.Error as e:
        flash('Error occurred during business registration.', 'error')
        print(f"Database error: {e}")
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_dashboard'))





# @app.route('/process_business_registration', methods=['POST'])
# def process_business_registration():
#     if 'admin_logged_in' not in session:
#         return redirect(url_for('admin_login'))
    
#     user_id = session.get('user_id')
#     business_name = request.form.get('business_name')
#     shop_no = request.form.get('shop_no')
#     phone_number = request.form.get('phone_number')
#     description = request.form.get('description')
#     category_name = request.form.get('category')
#     block_num = request.form.get('block_num')

#     print(f"Processing business registration with: {user_id}, {business_name}, {shop_no}, {phone_number}, {description}, {category_name}, {block_num}")

#     conn = get_db_connection()
#     try:
#         cur = conn.cursor()
        
#         # Check if the category already exists
#         cur.execute("SELECT id FROM categories WHERE category_name = %s", (category_name,))
#         category = cur.fetchone()
        
#         # If the category does not exist, insert it
#         if category is None:
#             cur.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING id", (category_name,))
#             category_id = cur.fetchone()[0]
#         else:
#             category_id = category[0]
        
#         # Insert the new business with the correct owner_id
#         cur.execute("""
#             INSERT INTO businesses (owner_id, business_name, shop_no, phone_number, description, block_num)
#             VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
#         """, (user_id, business_name, shop_no, phone_number, description, block_num))
#         business_id = cur.fetchone()[0]
        
#         # Link the business with its category
#         cur.execute("INSERT INTO business_categories (business_id, category_id) VALUES (%s, %s)", (business_id, category_id))
        
#         # Update the registration request to mark it as processed
#         cur.execute("UPDATE business_registration_requests SET processed = TRUE WHERE business_name = %s", (business_name,))
        
#         conn.commit()
#         flash('Business registered successfully and registration request marked as processed.', 'success')
#     except psycopg2.Error as e:
#         flash('Error occurred during business registration.', 'error')
#         print(f"Database error: {e}")
#     finally:
#         cur.close()
#         conn.close()
    
#     return redirect(url_for('admin_dashboard'))




@app.route('/process_user_registration', methods=['POST'])
def process_user_registration():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    phone = request.form['phone']

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()

            # Insert the new user into the users table
            cur.execute(
                "INSERT INTO users (username, email, password, name, phone, is_admin, is_approved) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (username, email, password, name, phone, False, False)
            )

            # Mark the user registration request as processed
            cur.execute(
                "UPDATE user_registration_requests SET processed = TRUE WHERE username = %s",
                (username,)
            )

            conn.commit()
            flash('User registered successfully.', 'success')
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            flash('Error processing user registration.', 'error')
        finally:
            cur.close()
            conn.close()

    return redirect(url_for('admin_dashboard'))



@app.route('/approve_user', methods=['POST'])
def approve_user():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    username = request.form['username']

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()

            # Get the user's email and registration request ID from user_registration_requests
            cur.execute("SELECT id, email FROM user_registration_requests WHERE username = %s", (username,))
            registration_request = cur.fetchone()

            if registration_request:
                registration_request_id = registration_request[0]
                email = registration_request[1]

                # Create the activation token
                token = s.dumps(email, salt='email-activate')
                
                # Send activation email
                activation_url = url_for('activate_account', token=token, _external=True)
                msg = Message('Activate Your Account', sender='efezinorich@gmail.com', recipients=[email])
                msg.body = f"Please click the link to activate your account: {activation_url}"
                mail.send(msg)

                # Update the user to set is_approved to TRUE, is_activated to FALSE, and associate registration_request_id
                cur.execute("""
                    UPDATE users 
                    SET is_approved = TRUE, is_activated = FALSE, activation_token = %s, registration_request_id = %s 
                    WHERE username = %s
                """, (token, registration_request_id, username))
                
                conn.commit()
                
                # Notify the admin that an email has been sent
                flash(f'User approved. Activation email sent to {email}.', 'success')
            else:
                flash('User registration request not found.', 'error')
        except psycopg2.Error as e:
            flash(f'Database error: {e}', 'error')
        finally:
            cur.close()
            conn.close()

    return redirect(url_for('admin_dashboard'))




# @app.route('/approve_user', methods=['POST'])
# def approve_user():
#     if 'admin_logged_in' not in session:
#         return redirect(url_for('admin_login'))

#     username = request.form['username']

#     conn = get_db_connection()
#     if conn:
#         try:
#             cur = conn.cursor()
#             cur.execute("SELECT email FROM users WHERE username = %s", (username,))
#             user = cur.fetchone()
#             if user:
#                 email = user[0]
#                 # Create the activation token
#                 token = s.dumps(email, salt='email-activate')
                
#                 # Send activation email
#                 activation_url = url_for('activate_account', token=token, _external=True)
#                 msg = Message('Activate Your Account', sender='efezinorich@gmail.com', recipients=[email])
#                 msg.body = f"Please click the link to activate your account: {activation_url}"
#                 mail.send(msg)

#                 # Update user to set is_approved to TRUE and is_activated to FALSE
#                 cur.execute("UPDATE users SET is_approved = TRUE, is_activated = FALSE, activation_token = %s WHERE username = %s", (token, username))
#                 conn.commit()
                
#                 # Notify the admin that an email has been sent
#                 flash(f'User approved. Activation email sent to {email}.', 'success')
#             else:
#                 flash('User not found.', 'error')
#         except psycopg2.Error as e:
#             flash(f'Database error: {e}', 'error')
#         finally:
#             cur.close()
#             conn.close()

#     return redirect(url_for('admin_dashboard'))



@app.route('/activate_account/<token>')
def activate_account(token):
    try:
        email = s.loads(token, salt='email-activate', max_age=3600)  # Token expires after 1 hour
    except SignatureExpired:
        flash('The activation link has expired.', 'error')
        return redirect(url_for('home'))
    except BadSignature:
        flash('The activation link is invalid.', 'error')
        return redirect(url_for('home'))

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # Update the user's activation status
            cur.execute("UPDATE users SET is_activated = TRUE WHERE email = %s", (email,))
            conn.commit()
            flash('Account activated successfully. You can now log in.', 'success')
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            flash('Error activating account.', 'error')
        finally:
            cur.close()
            conn.close()

    return redirect(url_for('user_login'))



# @app.route('/approve_user', methods=['POST'])
# def approve_user():
#     if 'admin_logged_in' not in session:
#         return redirect(url_for('admin_login'))

#     username = request.form['username']

#     conn = get_db_connection()
#     if conn:
#         try:
#             cur = conn.cursor()
#             # Approve the user by setting is_approved to True
#             cur.execute(
#                 "UPDATE users SET is_approved = TRUE WHERE username = %s",
#                 (username,)
#             )
#             conn.commit()
#             flash('User approved successfully.', 'success')
#         except psycopg2.Error as e:
#             print(f"Database error: {e}")
#             flash('Error approving user.', 'error')
#         finally:
#             cur.close()
#             conn.close()

#     return redirect(url_for('admin_dashboard'))


@app.route('/admin/users')
def admin_users():
    if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
        return redirect(url_for('user_login'))
    
    conn = get_db_connection()
    users = []
    user_requests = []
    business_requests = []
    pending_user_registration_request_count = 0
    pending_business_registration_requests_count = 0
    pending_approved_user_count = 0
    
    if conn:
        try:
            cur = conn.cursor()
            admin_id = session.get('admin_id')
             # Fetch admin profile picture URL
            cur.execute("SELECT profile_pic FROM admin WHERE id = %s", (admin_id,))
            profile_pic_path = cur.fetchone()[0]
            
            cur.execute("SELECT id, username, email, is_admin, is_approved, suspended FROM users")
            users = cur.fetchall()
            
            # Fetch all user registration requests
            cur.execute("SELECT * FROM user_registration_requests")
            user_requests = cur.fetchall()
            
            # Fetch all business registration requests
            cur.execute("SELECT * FROM business_registration_requests")
            business_requests = cur.fetchall()
            
            # Fetch all users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Count pending user registration requests
            cur.execute("SELECT COUNT(*) FROM user_registration_requests WHERE processed = FALSE")
            pending_user_registration_request_count = cur.fetchone()[0]
            
            # Count pending business registration requests
            cur.execute("SELECT COUNT(*) FROM business_registration_requests WHERE processed = FALSE")
            pending_business_registration_requests_count = cur.fetchone()[0]
            
            # Count unapproved users
            cur.execute("SELECT COUNT(*) FROM users WHERE is_approved = FALSE")
            pending_approved_user_count = cur.fetchone()[0]
            cur.close()
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            conn.close()
    
    return render_template('admin_users.html', users=users, user_requests=user_requests, 
                           business_requests=business_requests,  
                           pending_user_registration_request_count=pending_user_registration_request_count,
                           pending_business_registration_requests_count=pending_business_registration_requests_count,
                           pending_approved_user_count=pending_approved_user_count, profile_pic_path=profile_pic_path)
    

@app.route('/admin/suspend_user/<int:user_id>')
def suspend_user(user_id):
    if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
        return redirect(url_for('user_login'))
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE users SET suspended = TRUE WHERE id = %s", (user_id,))
            conn.commit()
            cur.close()
            flash("User account suspended.", 'success')
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            conn.close()
    
    return redirect(url_for('admin_users'))

@app.route('/admin/unsuspend_user/<int:user_id>')
def unsuspend_user(user_id):
    if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
        return redirect(url_for('user_login'))
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE users SET suspended = FALSE WHERE id = %s", (user_id,))
            conn.commit()
            cur.close()
            flash("User account unsuspended.", 'success')
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            conn.close()
    
    return redirect(url_for('admin_users'))



@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
        return redirect(url_for('user_login'))

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()

            # Fetch the registration_request_id
            cur.execute("SELECT registration_request_id FROM users WHERE id = %s", (user_id,))
            registration_request_id = cur.fetchone()

            # Delete related claim requests
            cur.execute("DELETE FROM claim_requests WHERE user_id = %s", (user_id,))

            # Delete the user
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

            # Manually delete the related registration request if the cascade didn't work
            if registration_request_id and registration_request_id[0]:
                cur.execute("DELETE FROM user_registration_requests WHERE id = %s", (registration_request_id,))

            conn.commit()
            cur.close()
            flash('User and associated data deleted successfully.', 'success')
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            conn.close()

    return redirect(url_for('admin_users'))




# @app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
# def delete_user(user_id):
#     if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
#         return redirect(url_for('user_login'))

#     conn = get_db_connection()
#     if conn:
#         try:
#             cur = conn.cursor()

#             # First, fetch the registration_request_id
#             cur.execute("SELECT registration_request_id FROM users WHERE id = %s", (user_id,))
#             registration_request_id = cur.fetchone()

#             # Then delete the user
#             cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

#             # Manually delete the related registration request if the cascade didn't work
#             if registration_request_id and registration_request_id[0]:
#                 cur.execute("DELETE FROM user_registration_requests WHERE id = %s", (registration_request_id,))

#             conn.commit()
#             cur.close()
#             flash('User and associated registration request deleted successfully.', 'success')
#         except psycopg2.Error as e:
#             flash(f"Database error: {e}", 'error')
#         finally:
#             conn.close()

#     return redirect(url_for('admin_users'))




@app.route('/admin/user/<int:user_id>/businesses')
def view_user_businesses(user_id):
    if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
        return redirect(url_for('user_login'))
    
    conn = get_db_connection()
    businesses = []
    user_name = None

    if conn:
        try:
            cur = conn.cursor()
            admin_id = session.get('admin_id')
             # Fetch admin profile picture URL
            cur.execute("SELECT profile_pic FROM admin WHERE id = %s", (admin_id,))
            profile_pic_path = cur.fetchone()[0]
            
            # Query to fetch businesses along with the owner's username
            cur.execute("""
                SELECT b.id, b.business_name, b.shop_no, b.phone_number, b.description, b.is_subscribed, b.email, u.username
                FROM businesses b
                JOIN users u ON b.owner_id = u.id
                WHERE b.owner_id = %s
            """, (user_id,))
            
            businesses = cur.fetchall()
            
            # Extract the username from one of the fetched businesses (assuming all have the same owner)
            if businesses:
                user_name = businesses[0][7]  # Assuming the username is at index 7 in the result
            
            cur.close()
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            conn.close()

    return render_template('admin_user_businesses.html', businesses=businesses, user_id=user_id, user_name=user_name, profile_pic_path=profile_pic_path)




# @app.route('/admin/business/<int:business_id>/update', methods=['GET', 'POST'])
# def update_business(business_id):
#     if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
#         return redirect(url_for('user_login'))
    
#     conn = get_db_connection()
#     user_id = None

#     if request.method == 'POST':
#         business_name = request.form['business_name']
#         shop_no = request.form['shop_no']
#         phone_number = request.form['phone_number']
#         description = request.form['description']
#         email = request.form['email']
#         category = request.form.get('category', '')  # Empty string as default
#         is_subscribed = request.form.get('is_subscribed') == 'on'

#         try:
#             cur = conn.cursor()

#             # Get the user_id and old category before updating the business
#             cur.execute("SELECT owner_id FROM businesses WHERE id = %s", (business_id,))
#             result = cur.fetchone()
#             user_id = result[0]

#             # Update the business details (without the category for now)
#             cur.execute("""
#                 UPDATE businesses
#                 SET business_name = %s, shop_no = %s, phone_number = %s, description = %s, email = %s, is_subscribed = %s
#                 WHERE id = %s
#             """, (business_name, shop_no, phone_number, description, email, is_subscribed, business_id))

#             # Handle category update
#             if category:
#                 # Check if the category already exists
#                 cur.execute("SELECT id FROM categories WHERE category_name = %s", (category,))
#                 category_result = cur.fetchone()

#                 if category_result:
#                     category_id = category_result[0]
#                 else:
#                     # Insert new category if it doesn't exist
#                     cur.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING id", (category,))
#                     category_id = cur.fetchone()[0]

#                 # Update the business with the new category ID
#                 cur.execute("UPDATE businesses SET category = %s WHERE id = %s", (category_id, business_id))
            
#             else:
#                 # If category is empty or None, set the category field to NULL
#                 cur.execute("UPDATE businesses SET category = NULL WHERE id = %s", (business_id,))

#             conn.commit()
#             flash('Business updated successfully.', 'success')
#             cur.close()
#         except psycopg2.Error as e:
#             flash(f"Database error: {e}", 'error')
#         finally:
#             conn.close()

#         # Redirect to the user's business view route, passing the user_id
#         return redirect(url_for('view_user_businesses', user_id=user_id))
    
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM businesses WHERE id = %s", (business_id,))
#     business = cur.fetchone()
#     user_id = business[1]  # Assuming owner_id is the second column in the businesses table
#     cur.close()
#     conn.close()

#     if business:
#         return render_template('admin_update_business.html', business=business)
#     else:
#         flash('Business not found.', 'error')
#         return redirect(url_for('view_user_businesses', user_id=user_id))




@app.route('/admin/business/<int:business_id>/update', methods=['GET', 'POST'])
def update_business(business_id):
    if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
        return redirect(url_for('user_login'))
    
    conn = get_db_connection()
    user_id = None

    if request.method == 'POST':
        business_name = request.form['business_name']
        shop_no = request.form['shop_no']
        phone_number = request.form['phone_number']
        description = request.form['description']
        email = request.form['email']
        category = request.form['category']
        is_subscribed = request.form.get('is_subscribed') == 'on'

        try:
            cur = conn.cursor()
            # Get the user_id before updating the business
            cur.execute("SELECT owner_id FROM businesses WHERE id = %s", (business_id,))
            user_id = cur.fetchone()[0]

            # Update the business details
            cur.execute("""
                UPDATE businesses
                SET business_name = %s, shop_no = %s, phone_number = %s, description = %s, email = %s, is_subscribed = %s, category = %s
                WHERE id = %s
            """, (business_name, shop_no, phone_number, description, email, is_subscribed, category, business_id))
            conn.commit()
            flash('Business updated successfully.', 'success')
            cur.close()
        except psycopg2.Error as e:
            flash(f"Database error: {e}", 'error')
        finally:
            conn.close()

        # Redirect to the user's business view route, passing the user_id
        return redirect(url_for('view_user_businesses', user_id=user_id))
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM businesses WHERE id = %s", (business_id,))
    business = cur.fetchone()
    user_id = business[1]  # Assuming owner_id is the second column in the businesses table
    cur.close()
    conn.close()

    if business:
        return render_template('admin_update_business.html', business=business)
    else:
        flash('Business not found.', 'error')
        return redirect(url_for('view_user_businesses', user_id=user_id))




@app.route('/admin/business/<int:business_id>/delete', methods=['POST'])
def delete_business(business_id):
    if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
        return redirect(url_for('user_login'))
    
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        
        # Delete related claim requests
        cur.execute("DELETE FROM claim_requests WHERE business_id = %s", (business_id,))

        
        # Delete business data from related tables first
        cur.execute("DELETE FROM business_categories WHERE business_id = %s", (business_id,))
        
        # Optionally, delete the business registration request
        cur.execute("DELETE FROM business_registration_requests WHERE business_name = (SELECT business_name FROM businesses WHERE id = %s)", (business_id,))
        
        # Finally, delete the business
        cur.execute("DELETE FROM businesses WHERE id = %s", (business_id,))
        
        conn.commit()
        flash('Business and related registration request deleted successfully.', 'success')
    except psycopg2.Error as e:
        flash(f"Database error: {e}", 'error')
        print(f"Database error: {e}")
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('admin_users'))



## Delete from Users and user_registration_requests Table ##
@app.route("/delete/<int:id_number>")
def delete(id_number):
    # we use this syntax <int:id_number> to get an interger or number, NOTE: the int is required,
    #but the id_number can be name anything
    
    connection = get_db_connection()
    mycusor = connection.cursor()
    mycusor.execute('DELETE FROM user_form WHERE id = %s', (id_number,))
    
    connection.commit()
    mycusor.close()
    connection.close()
    
    return redirect(url_for('fetch'))
## Delete from Users and user_registration_requests Table ##





@app.route('/subscribe/<int:business_id>', methods=['POST'])
def subscribe(business_id):
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    user_id = session.get('user_id')
    plan_id = request.form.get('plan_id')
    
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Check if the business belongs to the user
            cur.execute("SELECT owner_id FROM businesses WHERE id = %s", (business_id,))
            owner = cur.fetchone()
            
            if owner and owner[0] == user_id:
                # Insert subscription into the subscriptions table
                cur.execute("""
                    INSERT INTO subscriptions (business_id, plan_id, status) 
                    VALUES (%s, %s, 'confirmed')
                """, (business_id, plan_id))
                
                # Update the business as subscribed
                cur.execute("""
                    UPDATE businesses
                    SET is_subscribed = TRUE
                    WHERE id = %s
                """, (business_id,))
                
                conn.commit()
                flash("Subscription successful!", "success")
            else:
                flash("Unauthorized action.", "error")
            
            cur.close()
        except psycopg2.Error as e:
            conn.rollback()
            flash(f"Database error: {e}", "error")
        finally:
            conn.close()
    
    return redirect(url_for('user_business_profile'))




@app.route('/search_business', methods=['GET', 'POST'])
def search_business():
    search_query = request.args.get('search_query', '')  # Get the search query from the URL parameters
    businesses = []

    if search_query:
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                        # Fetch categories
                cur.execute("SELECT * FROM categories")
                categories = cur.fetchall()

                # Query to search subscribed businesses and unsubscribed businesses with no owner
                query = """
                    SELECT DISTINCT ON (b.id) b.*, c.category_name
                    FROM businesses b
                    LEFT JOIN business_categories bc ON b.id = bc.business_id
                    LEFT JOIN categories c ON bc.category_id = c.id
                    WHERE 
                        (
                            b.is_subscribed = TRUE OR
                            (b.is_subscribed = FALSE AND b.owner_id IS NULL)
                        ) 
                    AND (
                        c.category_name ILIKE %s OR
                        b.business_name ILIKE %s OR 
                        b.shop_no ILIKE %s
                    )
                """
                # Prepare search patterns with wildcards for partial matches
                search_pattern = f"%{search_query}%"
                
                cur.execute(query, (search_pattern, search_pattern, search_pattern))
                businesses = cur.fetchall()

                cur.close()
            except psycopg2.Error as e:
                flash(f"Database error: {e}", 'error')
            finally:
                conn.close()

    # Check if businesses list is empty and pass an additional variable to the template
    if not businesses:
        no_results_message = "No businesses found for your search."
    else:
        no_results_message = None

    return render_template('search_result.html', businesses=businesses, search_query=search_query, no_results_message=no_results_message, categories=categories)







@app.route('/categories')
def categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('categories.html', categories=categories)



@app.route('/category/<int:category_id>')
def category_view(category_id):
    conn = get_db_connection()
    categories = []
    businesses = []

    try:
        cur = conn.cursor()
        
        # Fetch categories
        cur.execute("SELECT * FROM categories")
        categories = cur.fetchall()
        
        # Fetch the category name
        cur.execute("SELECT category_name FROM categories WHERE id = %s", (category_id,))
        category_name = cur.fetchone()[0]
        
        # Fetch businesses in this category
        cur.execute("""
            SELECT b.*
            FROM businesses b
            INNER JOIN business_categories bc ON b.id = bc.business_id
            WHERE bc.category_id = %s AND b.is_subscribed = TRUE
        """, (category_id,))
        businesses = cur.fetchall()
        
        cur.close()
    except psycopg2.Error as e:
        flash(f"Database error: {e}", 'error')
        businesses = []
    finally:
        conn.close()

    return render_template('category_view.html', category_name=category_name, businesses=businesses, categories=categories)




@app.route('/logout')
def logout():
    print("Session before logout:", session)  # Debug: Print session variables
    session.clear()
   
    flash('No one is logged in.', 'warning')
    return redirect(url_for('index'))






@app.route('/claim_business/<int:business_id>', methods=['GET', 'POST'])
def claim_business(business_id):
    username = session.get('username')
    user_id = session.get('user_id')

    if not username or not user_id:
        flash("You need to be logged in to claim a business.", 'warning')
        return redirect(url_for('index'))

    conn = get_db_connection()
    business = None

    try:
        cur = conn.cursor()

        # Fetch the business details
        cur.execute("SELECT * FROM businesses WHERE id = %s", (business_id,))
        business = cur.fetchone()

        if request.method == 'POST':
            # Process the form submission
            phone_number = request.form['phone_number']
            email = request.form['email']
            category = request.form['category']
            description = request.form['description']

            cur.execute("""
                INSERT INTO claim_requests (business_id, user_id, phone_number, email, category, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (business_id, user_id, phone_number, email, category, description))

            conn.commit()
            flash("Claim request submitted successfully! The admin will review your request.", 'success')
            return redirect(url_for('index'))

        cur.close()
    except psycopg2.Error as e:
        flash(f"Database error: {e}", 'error')
    finally:
        conn.close()

    return render_template('claim_business.html', business=business)







@app.route('/')
def index():
    username = session.get('username')
    user_id = session.get('user_id')
    user_profile = None  # Initialize user_profile to None

    conn = get_db_connection()
    categories = []
    businesses = []

    try:
        cur = conn.cursor()

        # Fetch categories
        cur.execute("SELECT * FROM categories")
        categories = cur.fetchall()

        # Fetch publicly available businesses (not subscribed and no owner)
        cur.execute("""
            SELECT * FROM businesses
            WHERE is_subscribed = FALSE AND owner_id IS NULL
        """)
        businesses = cur.fetchall()

        # Fetch subscribed businesses (including those belonging to the logged-in user)
        cur.execute("""
            SELECT * FROM businesses
            WHERE is_subscribed = TRUE
        """)
        subscribed_businesses = cur.fetchall()

        # Combine the lists
        businesses.extend(subscribed_businesses)

        # Fetch user profile if username is available
        if username:
            cur.execute("SELECT username, profile_image FROM users WHERE username = %s", (username,))
            user_profile = cur.fetchone()

        cur.close()
    except psycopg2.Error as e:
        flash(f"Database error: {e}", 'error')
    finally:
        conn.close()

    return render_template('index.html', username=username, businesses=businesses, categories=categories, user_profile=user_profile)






if __name__ == '__main__':
    app.run(debug=True)
