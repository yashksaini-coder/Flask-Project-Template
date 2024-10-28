from flask import render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import User
from sqlalchemy.exc import IntegrityError
from ai import analyze_sentiment

def register_routes(app, db, bcrypt):
    @app.route("/")
    def index():
        return render_template("index.html", user=current_user)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("analyse"))
            flash("Invalid username or password")
        return render_template("login.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form["username"]
            name = request.form["name"]
            password = request.form["password"]
            email = request.form["email"]
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            new_user = User(
                name=name, username=username, email=email, password=hashed_password
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login"))
            except IntegrityError:
                db.session.rollback()
                flash("Username or email already exists")
        return render_template("signup.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route('/analyse', methods=['GET', 'POST'])
    @login_required
    def analyse():
        if request.method == 'GET':
            return render_template('analyse.html')
        
        if request.method == 'POST':
            user_input = request.form.get('text')
            if user_input:
                sentiment = analyze_sentiment(user_input)  
                return jsonify({'sentiment': sentiment})  
            return jsonify({'sentiment': 'No input provided'})
