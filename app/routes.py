from app import app
from flask import render_template
from app.forms import AddressRegister
from app.models import Address

@app.route('/')
def index():
    address = Address.query.order_by(Address.name).all()
    lst =[]
    for i in address:
        lst.append({'name':i.name, 'phone':i.phone, 'address':i.address})
    print(lst)
    return render_template('index.html', lst = lst)


@app.route('/addressregister', methods=["GET","POST"])
def addressregister():
    form = AddressRegister()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        Address(name=name, phone=phone, address=address)
    return render_template('addressregister.html', form=form)