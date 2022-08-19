from app import app
from flask import render_template,url_for,redirect,flash
from app.forms import AddressRegister, UserRegister, Login
from app.models import Address, User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    address = Address.query.order_by(Address.name).all()
    lst = []
    for i in address:
        lst.append({'name':i.name, 'phone':i.phone, 'address':i.address})
    print(lst)
    return render_template('index.html', lst = lst)


@app.route('/addressregister', methods=["GET","POST"])
@login_required
def addressregister():
    form = AddressRegister()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        Address(name=name, phone=phone, address=address, user_id=current_user.id)
        flash("The new address has been added","success")
        return redirect(url_for('index'))
    return render_template('addressregister.html', form=form)

@app.route('/signup', methods=["GET","POST"])
def signup():
    form = UserRegister()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("User or Email is Token !!","danger")
            return redirect(url_for('signup'))
        User(username=username, email=email, password=password)
        flash("The new user has been created","success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=["GET","POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if user.check_password(password):
                login_user(user)
                flash(f'{user.username} logged in successfully','success')
                return redirect(url_for('index'))
            else:
                flash("Incorrect password !","danger")
        else:
            flash("Incorrect Username","danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logedout scuccessfully","info")
    return redirect(url_for('index'))