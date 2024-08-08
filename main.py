from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
import requests
from flask_login import login_required

import openai
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv() 

openai.api_key =os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))

def create_tables():
    db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    # Render the 404.html template with a custom message
    return render_template('404.html'), 404

@app.route('/not-found')
def not_found():
    abort(404)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if 'user' not in session:
        error1 = "Please login to continue."
        return render_template('login.html', error=error1)
    else:
        if request.method == 'POST':
            title = request.form['title']
            keywords = request.form['keywords']
            prompt = f"""As a technical writer experienced in SEO, please create a detailed blog post outline that provides a step-by-step guide for using {title}, with these keywords : {keywords} targeting beginners with a friendly and helpful tone and a desired length of 800-1000 words."""
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            generated_blog = response.choices[0].text
            return render_template('blog.html', generated_blog=generated_blog)
        return render_template('blog.html')

@app.route('/email', methods=['GET', 'POST'])
def email():
    if 'user' not in session:
        error1 = "Please login to continue."
        return render_template('login.html', error=error1)
    else:
        if request.method == 'POST':
            title = request.form['title']
            tone = request.form['tone']
            keywords = request.form['keywords']
            prompt = """Hi OpenAI,
    
            I need your help to write an email. I have the following variables:
            
            - Title: {}
            - Tone: {}
            - Keywords: {}
    
            I would like you to generate an email for me using these variables. The email should have a friendly tone and should be addressed to a professional contact.
    
            Please make sure that the email is well-written and free of grammatical errors. Thank you in advance for your help!
    
            Best regards,
            [Your Name]
            """.format(title, tone, keywords)
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            generated_email = response.choices[0].text
            return render_template('email.html', generated_email=generated_email)
        return render_template('email.html')

@app.route('/extra')
def extra():
    return render_template('extra.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user'] = email
            return redirect('/')
        else:
            error = "Invalid Email/Password."
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    # clear the session variables
    session.clear()
    return redirect('/login')
@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        error1 = "You are already logged in"
        return render_template('home.html', error=error1)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        terms_accepted = request.form.get('terms')

        # Check if email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists.')
            return redirect(url_for('login'))

        # Validate form data
        if not email or not password or not confirm_password:
            flash('Please fill out all fields.')
            return redirect(url_for('register'))
        elif password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))
        elif not terms_accepted:
            flash('Please accept the terms and conditions.')
            return redirect(url_for('register'))

        # Hash password and create new user
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # Log in user and redirect to main page
        session['email'] = email
        return redirect(url_for('home'))

    # Render the registration form
    return render_template('signup.html')

@app.route('/social', methods=['GET', 'POST'])
def social():
    if 'user' not in session:
        error1 = "Please login to continue."
        return render_template('login.html', error=error1)
    else:
        if request.method == 'POST':
            topic = request.form['topic']
            platform = request.form['mood']
            keywords = request.form['title']
            promt = f"""You want to create a 1 social media post with hashtags to promote a {topic} on {platform}. The post should include {keywords} and it must be 250-300 words. 
    Examples: 
    - You want to create a social media post with hashtags to promote a new book on Instagram. The post should include #booklovers, #readingtime, and #newrelease.
    - You want to create a social media post with hashtags to promote a sale on Twitter. The post should include #discounts, #limitedoffer, and #shopnow."""
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=promt,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            generated_post = response.choices[0].text
            return render_template('social.html', generated_post=generated_post)

    return render_template('social.html')


if __name__ == '__main__':
    if not os.path.exists('mydatabase.db'):
        with app.app_context():
            create_tables()
    app.run(debug=True)