from app import app
from flask import render_template,url_for,redirect,flash
from app.forms import AddressRegister, UserRegister, Login
from app.models import Address, User
from flask_login import login_user, logout_user, login_required, current_user
import requests
import json

@app.route('/')
def index():
    if current_user.is_authenticated:
        addresses = Address.query.filter_by(user_id=current_user.id)
        return render_template('index.html', addresses=addresses)
    return render_template('index.html')

@app.route('/addressregister', methods=["GET","POST"])
@login_required
def addressregister():
    form = AddressRegister()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        street = form.street.data
        zipcode = form.zipcode.data
        result = validate_address(street, zipcode)
        if 'error' not in result and result['valid_address']:
            city = result["components"]["city"]
            state = result["components"]["state"]
            county = result["components"]["county"]
            address_type = result["components"]["address_type"]
            Address(name=name, phone=phone, street=street, zipcode=zipcode, city=city, state=state,county=county,address_type=address_type, user_id=current_user.id)
            flash("The new address has been added","success")
            return redirect(url_for('index'))
        else:
            flash("Wrong address !", "danger")
    return render_template('addressregister.html', form=form)

@app.route('/editaddress/<address_id>', methods=["GET","POST"])
@login_required
def editaddress(address_id):
    print(address_id)
    address_to_edit = Address.query.get_or_404(address_id)
    if address_to_edit.user != current_user:
        flash("You are not authorized to modify this address")
        return redirect(url_for('index'))
    form = AddressRegister()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        street = form.street.data
        zipcode = form.zipcode.data
        result = validate_address(street, zipcode)
        if 'error' not in result and result['valid_address']:
            city = result["components"]["city"]
            state = result["components"]["state"]
            county = result["components"]["county"]
            address_type = result["components"]["address_type"]
            address_to_edit.update(name=name, phone=phone, street=street, zipcode=zipcode, city=city, state=state,county=county,address_type=address_type, user_id=current_user.id)
            flash("The new address has been added","success")
            return redirect(url_for('index'))
        else:
            flash("Wrong address !", "danger")
    return render_template('editaddress.html', address=address_to_edit, form=form)

@app.route('/deleteaddress/<address_id>')
def deleteaddress(address_id):
    address_to_delete = Address.query.get_or_404(address_id)
    if address_to_delete.user != current_user:
        flash("You are not authorized to modify this address","danger")
        return redirect(url_for('index'))
    address_to_delete.delete()
    flash(f"{address_to_delete.name}'s address has been deleted successfully","info")
    return redirect(url_for('index')) 

def validate_address(street, zip_code):
    base_url ="https://api.lob.com/v1"
    api_method = "/us_verifications"
    Api_key = "live_82bd4dc5f202bc4752ee348d00f671baf71"
    url = base_url+api_method

    d= {'primary_line':street,'zip_code':zip_code}

    address_res = requests.post(url, data = d,auth=(Api_key,''))  
    return address_res.json()



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

