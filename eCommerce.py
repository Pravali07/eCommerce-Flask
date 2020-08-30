from flask import Flask,render_template,redirect,url_for,request,flash
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin,LoginManager,login_user,logout_user,current_user,login_required
from db import Base,Products
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask,render_template
from werkzeug.utils import secure_filename
app=Flask(__name__)
app.secret_key="1234"

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(id):
	return session.query(Products).get(int(id))

engine=create_engine('sqlite:///product.db',connect_args={'check_same_thread':False},echo=True)
DBsession=sessionmaker(bind=engine)
session=DBsession()
Base.metadata.bind=engine

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

@app.route('/', methods = ['GET', 'POST'])
def viewProducts():
	dbData=session.query(Products).all()
	for i in dbData:
		no = "photo" + str(i.id)
		write_file(i.image, "E:\\Garbage\\WebDesignPython\\eCommerce\\static\\images\\" + no + ".jpg")
	return render_template('index.html',data = dbData)
@app.route('/admin',methods=['GET','POST'])
def admin():
	if request.method=='POST':
		imageData = request.files['image']
		if not imageData:
			return 'No pic uploaded!',400
		img = Products(image = imageData.read(),
			name = request.form['name'],
			description = request.form['description'],
			price = request.form['price'],
			tax = request.form['tax'],
			inCart = False)
		session.add(img)
		session.commit()
		return redirect(url_for('viewProducts'))
	return render_template('admin.html')

@app.route('/<int:r_id>/view',methods = ['GET','POST'])
def viewDetails(r_id):
	dbData = session.query(Products).all()
	return render_template('viewDetails.html',id = r_id, details = dbData )

@app.route('/<int:r_id>/cart',methods=['GET','POST'])
def viewCart(r_id):
	if (r_id != 0):
		update = session.query(Products).filter_by(id = r_id).first()
		update.inCart = False
		session.commit()
	dbData = session.query(Products).all()
	flag = False
	total = 0
	for i in dbData:
		if i.inCart == True:
			total += (i.price+i.tax)
			flag = True
	return render_template('viewCart.html',details = dbData, flag = flag,total = total)

@app.route('/<int:r_id>/sample',methods=['GET','POST'])
def sample(r_id):
	dbData = session.query(Products).all()
	update_this = session.query(Products).filter_by(id = r_id).first()
	if update_this.inCart == True:
		update_this.inCart = False
	else:
		update_this.inCart = True
	session.commit()
	return render_template('viewDetails.html',id = r_id,details = dbData)

app.run(debug=True)
