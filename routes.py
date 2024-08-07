from app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Roles, Influencer, Sponsor
import os
import re
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/influencer_dashboard')
def influencer_dashboard():
    return render_template('influencer_dashboard.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('user_login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('logged_in', False)
        return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        t_errors = 0
        error = ""
        email_error = ""
        password_error = ""
        print(email)
        print(password)
        if not email or not password:
            flash('Please fill out all the fields.')
            email_error = "Please fill out all the fields."
            t_errors+=1
            print(t_errors)
            print(email_error)
            return redirect(url_for('login'))
        user =  User.query.filter_by(email=email).first()
        if not user:
            flash('Email does not exist')
            error = "Email does not exist"
            t_errors+=1
            print(t_errors)
            print(error)
            return redirect(url_for('login'))
        if user.user_status == 0:
            flash('User has been blocked!')
            error = "User has been blocked!"
            t_errors+=1
            print(t_errors)
            print(error)
            return redirect(url_for('login'))
        if user.password != password:
            flash('Password does not match!') 
            password_error = "Password does not match!"
            t_errors+=1      
            print(t_errors)     
            print(password_error)
            return redirect(url_for('login'))

        else:
            session['logged_in'] = True
            session['username'] = user.username
            session['user_status'] = user.user_status
            session['role'] = user.r_id
            session['profile_created'] = user.profile_created
            print(session['role'])
            print(session['profile_created'])
            return redirect(url_for('influencer_dashboard'))

    return render_template('user_login.html')

@app.route('/create_profile', methods = ['GET', 'POST'])
def create_profile():
    return render_template('create_profile.html')

@app.route('/profile', methods=["POST", "GET"])

# def display_profile():
#     return render_template('display_profile.html')

# def create_profile():
#     return render_template('create_profile.html')
# def create_profile():
#     if request.method == "POST":
#         fname = request.form.get("fname")
#         lname = request.form.get("lname")
#         birthday = request.form.get("birthday")
#         bio = request.form.get("bio")
#         link = request.form.get("link")
#         display_picture = request.form.file("displaypicture")
#         if display_picture:
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], display_picture.filename)
#             display_picture.save(file_path)
#         error = ""
#         t_errors = 0
#         if not fname or not lname or not birthday or not bio or not link or not display_picture:
#             flash("Please fill out all the fields.")
#             error = "Please fill out all the fields."
#             t_errors+=1
#         session['profile_created'] == 1
#         return redirect(url_for('/display_profile'))
#     else:
#         return render_template('create_profile.html')        
#     # return render_template('create_profile.html')    
def profile():
    if 'username' in session:
        print("Username: ", session['username'])
        if (session['profile_created'] == 0):
            print("Profile not created")
            return redirect(url_for('create_profile'))
    
    # return render_template('display_profile.html')

@app.route('/campaigns')
def campaigns():
    return render_template('campaigns.html')



# @app.route('/login')
# def login():
#     return render_template('user_login.html')

# @app.route('logout')
# @login_required

@app.route('/register_influencer', methods=['GET','POST'])
def register_influencer():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        # category = request.form.get('category')
        niche = request.form.get('niche')
        platform = request.form.get('platform')
        reach = request.form.get('reach')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        r_id = Roles.query.filter_by(r_id=2).with_entities(Roles.r_id).scalar()
        user_status = 1
        profile_created = 0
        username_error = ""
        email_error = ""
        password_error = ""
        category_error = ""
        t_errors = 0

        print("R_id: ", r_id)
        print("Niche: ", niche)
        print("Platform: ", r_id)
        
        if not password:
            password_error = "Password cannot be blank!"
            flash("Password cannot be blank!")
            t_errors+=1

        if not confirm_password: 
            password_errror = "Confirm password cannot be blank!"
            flash("Confirm password cannot be blank!")
            t_errors+=1

        if not len(password) >= 8 and t_errors == 0:
            password_error = "Password should be atleast 8 characters long"
            flash("Password should be atleast 8 characters long")
            t_errors+=1

        elif (password != confirm_password):
            password_error = "Passwords don't match!"
            flash("Passwords don't match!")
            t_errors += 1

        if not email:
            email_error = "Email cannot be blank!"
            flash("Email cannot be blank")
            t_errors+=1
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_error = "Invalid email address"
            flash("Invalid email address")

            t_errors+=1
        else:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                email_error = "Email already exists. Try logging in or register using another email address."
                flash("Email already exists. Try logging in or register using another email address.")
                t_errors+=1

        if not reach:
            category_error = "Reach cannot be blank!"
            flash("Reach cannot be blank!")
            t_errors+=1
        if not niche:
            category_error = "Niche cannot be blank!"
            flash("Niche cannot be blank!")
            t_errors+=1
        print(t_errors)
        if t_errors == 0:
            user = User(
                username = username,
                email = email,
                password = password,
                user_status = user_status,
                r_id = r_id,
                profile_created = profile_created
            )
            db.session.add(user)
            db.session.commit()

            influencer = Influencer(
                user_id = user.user_id,
                niche = niche,
                platform = platform,
                reach = reach
            )
            db.session.add(influencer)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('influencer_reg.html', email_error=email_error, password_error=password_error, category_error=category_error)
        return redirect(url_for('login'))
    
    return render_template('influencer_reg.html')

@app.route('/register_sponsor', methods=['GET', 'POST'])
def register_sponsor():
    if request.method == 'POST':
        pass
    return render_template('sponsor_reg.html')
# @app.route('/register_sponsor', methods=['GET', 'POST'])
# def register_sponsor():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         budget = request.form.get('budget')
#         industry = request.form.get('industry')
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirm_password')
#         r_id = 3
#         r_name = "sponsor"
#         user_status = 1
#         username_error = ""
#         email_error = ""
#         password_error = ""
#         industry_error = ""
#         budget_error = ""
#         t_errors = 0

#         if not password:
#             password_error = "Password cannot be blank!"
#             t_errors+=1

#         if not confirm_password: 
#             password_errror = "Confirm password cannot be blank!"
#             t_errors+=1

#         if not len(password) >= 8 and t_errors == 0:
#             password_error = "Password should be atleast 8 characters long"
#             t_errors+=1

#         elif (password != confirm_password):
#             password_error = "Passwords don't match!"
#             t_errors += 1

#         if not email:
#             email_error = "Email cannot be blank!"
#             t_errors+=1
#         elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             email_error = "Invalid email address"
#             t_errors+=1
#         else:
#             existing_email = User.query.filter_by(email=email).first()
#             if existing_email:
#                 email_error = "Email already exists. Try logging in or register using another email address."
#                 t_errors+=1

#         if not industry:
#             industry_error = "Industry cannot be blank!"
#             t_errors+=1
#         if not budget:
#             budget_error = "Budget cannot be blank!"
#             t_errors+=1
#         elif budget.isalpha() == True:
#             budget_error = "Budget should be a numeric value."
#             t_errors+=1
        
#         if t_errors==0:
#             user = User(
#             username = username,
#             email = email,
#             password = password,
#             user_status = 1
#             )
#             db.session.add(user)
#             db.session.commit()
#             role = Roles(
#                 r_id = r_id,
#                 r_name = r_name
#             )
#             db.session.add(role)
#             db.session.commit()
#             sponsor = Sponsor(
#                 industry = industry,
#                 budget = budget, 
#             )
#             db.session.add(sponsor)
#             db.session.commit()
#         else:
#             return render_template('sponsor_reg.html', email_error=email_error, password_error=password_error, industry_error=industry_error, budget_error=budget_error)
#         return redirect(url_for('login'))
#     return render_template('sponsor_reg.html')
            