from flask import Flask,render_template,redirect , request ,flash ,url_for ,session,g ,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager , login_user , login_required , logout_user ,current_user,UserMixin
from werkzeug.utils import secure_filename 
from flask_bcrypt import Bcrypt
import MySQLdb
import smtplib
from flask_mail import Mail, Message
from datetime import datetime
import time
import os
import random
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587  # Common port for TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tanusree20basuchoudhury1997@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'wlby thub jbnl ikiu'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'tanubasuchoudhury1997@gmail.com'
app.secret_key = "super_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql://root:@localhost/electricecom"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] ="static/media/"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(UserMixin,db.Model):
    id  = db.Column(db.Integer,primary_key=True)
    name  = db.Column(db.String(255),unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True,nullable=False)
    password = db.Column(db.String(255), unique=True,nullable=False)
    user_type = db.Column(db.Integer,nullable=False, default=0)
    phone = db.Column(db.String(255), unique=True,nullable=False)
    image = db.Column(db.String(255),nullable=True)
    orders = db.relationship('Orders', backref='users',lazy=True)
    carts = db.relationship('Carts', backref='users',lazy=True)
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    image2 = db.Column(db.String(255), nullable=False)
    image3  = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(5000), nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'), nullable=False)
    brand_id =  db.Column(db.Integer,db.ForeignKey('brands.id'), nullable=False)
    cart_items = db.relationship('Carts', backref='products', lazy=True)
    orders =  db.relationship('Orders', backref='products', lazy=True)
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Email =db.Column(db.String(255), unique=True, nullable=False)
    Phone = db.Column(db.String(255), nullable=False)
    alternate_number = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text(255), nullable=False)
    Payment_mode = db.Column(db.String(255), nullable=False)
    order_status =db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    Order_date = db.Column(db.Date, default=time.strftime("%Y-%m-%d"), nullable=False)
    Delivery_date = db.Column(db.Date,   nullable=True)
    
    
    total_price = db.Column(db.Float, nullable=False)

class Carts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer)
class Contact(db.Model):
    id  = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email  = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text(1000), nullable=False)
class Website(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String(255),nullable=True)
    logo = db.Column(db.String(255),nullable=True)
    image1 = db.Column(db.String(255),nullable=False)
    image2 = db.Column(db.String(255),nullable=False)
    image3 =db.Column(db.String(255),nullable=False)
    about_heading = db.Column(db.String(255),nullable=False)
    about_text = db.Column(db.String(255),nullable=False)
    versetile_bands =db.Column(db.String(255),nullable=True)
    digital_agency = db.Column(db.String(255),nullable=True)
    footer = db.Column(db.String(255), nullable=True)
class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    products = db.relationship('Products', backref='category', lazy=True)
class Brands(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255), nullable=False)    
    products = db.relationship('Products', backref='brands', lazy=True)
with app.app_context():
    db.create_all()
@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        password_hash = bcrypt.generate_password_hash(confirm_password)
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            image.save(image_path)
            
            if password == confirm_password:
                    user_add=Users()
                    user_add.name = name
                    user_add.email = email
                    user_add.password =password_hash
                    user_add.phone = phone
                    user_add.image = filename
            try:
                    db.session.add(user_add)
                    db.session.commit()
                    flash('Account Created successfully','success')
                    return redirect('/login')
            except Exception as e:
                    print('e')
                    flash('Account not Created successfully','success')
    return render_template('signup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            if user.user_type == 1:  
                login_user(user)
                flash('Logged in successfully.', 'warning')
                return redirect(url_for('admin'))
            else:
                 login_user(user)
                 flash('Logged in successfully.', 'success')
                 return redirect(url_for('home'))
            
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html')
@app.route('/admin')
@login_required
def admin():
    if current_user.user_type==1:
      products = Products.query.count()
      users = Users.query.count()
      orders = Orders.query.count()
      contacts = Contact.query.count()
      return render_template("admin.html", products=products,users=users,orders=orders,contacts=contacts)
    else:
        flash("Unauthorized Access","danger")
        return redirect(url_for("login"))
@app.route('/')
def home():
    products = Products.query.all()
    random_product = random.sample(products, min(len(products),6))
    category = Category.query.all()
    brands = Brands.query.all()
    website = Website.query.filter_by(id=1).first()
    
    return render_template('index.html',category=category,brands=brands,products=random_product, product=products, website=website)

@app.route('/logout')
@login_required
def logout():
    if current_user.user_type ==1:
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('admin'))
    else:
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))
@app.route('/adminproduct', methods=['GET','POST'])
@login_required
def adminproduct():
    if current_user.user_type == 1:
        
        page = request.args.get('page',1 , type=int)
        per_page = 3
        products = Products.query.paginate(page=page,per_page=per_page)
        category = Category.query.all()
        brands = Brands.query.all()
        return render_template('adminproduct.html', products=products,category=category,brands=brands)
    else:
         flash('You are not authorized to access this page.', 'danger')
         return redirect(url_for('login'))
@app.route('/adminaddproduct',methods=['GET','POST'])
@login_required
def addproduct():
    if current_user.user_type ==1:
        if request.method == "POST":
                product_name = request.form['product_name']
                product_price = request.form['product_price']
                product_category = request.form['product_category']
                product_brand = request.form['product_brands']
                product_image = request.files['product_image']
                product_image2 = request.files['product_image2']
                product_image3 = request.files['product_image3']
                product_description  = request.form['description']
                if product_image and product_image2 and product_image3  :
                    ##product image 1 insert
                    file_name = secure_filename(product_image.filename)
                    product_image_path = os.path.join(app.config['UPLOAD_FOLDER'],file_name)
                    product_image.save(product_image_path)
                    ## product image 2 insert
                    file_name2 = secure_filename(product_image2.filename)
                    product_image2_path = os.path.join(app.config['UPLOAD_FOLDER'],file_name2)
                    product_image2.save(product_image2_path)
                    ## product image 3 insert
                    file_name3 = secure_filename( product_image3.filename)
                    product_image3_path = os.path.join(app.config['UPLOAD_FOLDER'],file_name3)
                    product_image3.save(product_image3_path)
                    product = Products()
                    product.name = product_name
                    product.price = product_price
                    product.category_id = product_category
                    product.brand_id = product_brand
                    product.image =file_name
                    product.image2 = file_name2
                    product.image3 = file_name3
                    product.description =product_description
                    try:
                        db.session.add(product)
                        db.session.commit()
                        flash('Product Added','success')
                        return redirect(url_for('adminproduct'))
                    except Exception as e:
                        print(e)
                        flash('Product not added','danger')
                        return redirect(url_for('adminproduct'))
            
        category = Category.query.all()
        brands = Brands.query.all()
        return render_template("add_product.html",category=category, brands=brands)
    else:
         flash('You are not authorized to access this page.', 'danger')
         return redirect(url_for('login'))
            
@app.route('/adminproductedit/<int:id>', methods=['GET','POST'])
@login_required
def adminproductedit(id):
    if current_user.user_type == 1:
        products = Products.query.get(id)
        if request.method == "POST":
           
            product_name = request.form['product_name']
            product_price = request.form['product_price']
            product_desc = request.form['description']
            product_category = request.form['product_category']
            product_brand = request.form['product_brands']
            product_image = request.files['product_image']
            product_image2 = request.files['product_image2']
            product_image3 = request.files['product_image3']
            # print(product_name,product_price, product_desc , product_category,product_brand,product_image,product_image2,product_image3)
            # first Image Insert 
            if product_image.filename == '' or product_image2.filename == '' or product_image3.filename == '':
                products.name = product_name
                products.price =  product_price
                products.category_id =product_category
                products.brand_id  = product_brand
                products.description = product_desc
                
                try:
                    db.session.commit()
                    flash('Product Data Updated','success')
                    return redirect(url_for('adminproduct'))
                except Exception as e:
                 flash('Product not Data Updated','danger')
            else:
    
    # Save images to the upload folder
                filename = secure_filename(product_image.filename)
                filename2 = secure_filename(product_image2.filename)
                filename3 = secure_filename(product_image3.filename)
                image1_path = os.path.join(app.config['UPLOAD_FOLDER'], product_image.filename)
                image2_path = os.path.join(app.config['UPLOAD_FOLDER'], product_image2.filename)
                image3_path = os.path.join(app.config['UPLOAD_FOLDER'], product_image3.filename)

                product_image.save(image1_path)
                product_image2.save(image2_path)
                product_image3.save(image3_path)
                
                products.name = product_name
                products.price =  product_price
                products.category_id =product_category
                products.brand_id  = product_brand
                products.description = product_desc
                products.image = filename
                products.image2 = filename2
                products.image3 = filename3
                try:
                    db.session.commit()
                    flash('Product Data Updated','success')
                    return redirect(url_for('adminproduct'))
                except Exception as e:
                    flash('Product not Data Updated','danger')
                
        brands = Brands.query.all()
        category =Category.query.all()
        return render_template('edit_product.html',products=products, category=category,brands=brands)
    else:
        flash('Ypu are not authorized to access this page','danger')
        return redirect(url_for('login'))
        
@app.route('/adminproductdelete/<int:id>', methods=['GET','POST'])
@login_required
def adminproductdelete(id):
    product = Products.query.get(id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product Deleted Successfully','danger')
        return redirect(url_for('adminproduct'))
    except Exception as e:
        print(e)
        flash('Product not Deleted Successfully','danger')
        return redirect(url_for('adminproduct'))
    

                
@app.route('/admincategory', methods=['GET','POST'])
@login_required
def admincategory():
    if current_user.user_type == 1:
        if request.method =="POST":
            cat_name = request.form.get('cat_name')
            category = Category(name=cat_name)
            db.session.add(category)
            db.session.commit()
            flash('Category Added','success')
            return redirect(url_for('admincategory'))
        page = request.args.get('page', 1, type=int)  # বর্তমান পেজ নম্বর
        per_page = 3
        category = Category.query.paginate(page=page, per_page=per_page)
        print(len(category.items))
        return render_template('admincategories.html',categories=category)
    else:
         flash('You are not authorized to access this page.', 'danger')
         return redirect(url_for('login'))
@app.route('/admincategoryedit/<int:id>', methods=['GET','POST'])
@login_required
def admincategoryedit(id):
    category= Category.query.get_or_404(id)
    if request.method == "POST":
        category.name= request.form['cat_name']
        try:
            db.session.commit()
            flash('Category Edited Successfully','info')
            return redirect(url_for('admincategory'))
        except Exception as e:
            print(e)
            flash('Category not Edited Successfully','info')
    return render_template('admincategories.html',category=category)
@app.route('/admincategorydelete/<int:id>', methods=['GET','POST'])
@login_required
def admincategorydelete(id):
    category = Category.query.get(id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash('Category Deleted Successfully','danger')
        return redirect(url_for('admincategory'))
    except Exception as e:
        print(e)
        flash('Category not Deleted Successfully','danger')
        return redirect(url_for('admincategory'))
## Category End ##
## Brand Start ##

@app.route('/adminbrands', methods=['GET','POST'])
@login_required
def adminbrands():
    if current_user.user_type == 1:
        if request.method =="POST":
            brand_name = request.form.get('brand_name')
            brand = Brands(name=brand_name)
            db.session.add(brand)
            db.session.commit()
            flash('Brand Added','success')
            return redirect(url_for('adminbrands'))
        page = request.args.get('page', 1, type=int)  # বর্তমান পেজ নম্বর
        per_page = 3
        brand = Brands.query.paginate(page=page, per_page=per_page)
        print(len(brand.items))
        return render_template('adminbrands.html',brands=brand)
    else:
         flash('You are not authorized to access this page.', 'danger')
         return redirect(url_for('login'))
@app.route('/adminbrandedit/<int:id>', methods=['GET','POST'])
@login_required
def adminbrandedit(id):
    brand= Brands.query.get_or_404(id)
    if request.method == "POST":
        brand.name= request.form['brand_name']
        try:
            db.session.commit()
            flash('Brand Edited Successfully','info')
            return redirect(url_for('adminbrands'))
        except Exception as e:
            print(e)
            flash('Brand not Edited Successfully','info')
    return render_template('admincategories.html',brand=brand)
@app.route('/adminbranddelete/<int:id>', methods=['GET','POST'])
@login_required
def adminbranddelete(id):
    brand = Brands.query.get(id)
    try:
        db.session.delete(brand)
        db.session.commit()
        flash('Brand Deleted Successfully','danger')
        return redirect(url_for('adminbrands'))
    except Exception as e:
        print(e)
        flash('Brand not Deleted Successfully','danger')
        return redirect(url_for('adminbrands'))
    
##product details
@app.route('/productdetails/<int:id>')
def productdetails(id):
    products = Products.query.filter_by(id=id).first()
    
    return render_template('products_description.html',products=products)
@app.route('/showcategory/<int:id>')
def showcategory(id):
    products = Products.query.filter_by(category_id=id).all()
    website = Website.query.filter_by(id=1).first()
    return render_template('show-category.html', products=products, website=website)
@app.route('/showbrand/<int:id>')
def showbrand(id):
    products = Products.query.filter_by(brand_id=id).all()
    website = Website.query.filter_by(id=1).first()
    return render_template('show-brand.html', products=products,website=website)
@app.route('/change-profile/<int:id>')
@login_required
def changeprofile(id):
    if current_user.id == id:
        user = Users.query.get(id)
        print(user.name)
        website = Website.query.filter_by(id=1).first()
        return render_template('change-profile.html',users=user,website=website )
@app.route('/change-profileDetails/<int:id>', methods=['GET','POST'])
@login_required
def changeprofileDetails(id):
    if current_user.id == id:
        user = Users.query.get(id)
        if request.method == "POST":
            name = request.form.get('user_name')
            email = request.form.get('user_email')
            password1 =request.form.get('user_password')
            password2  = request.form.get('user_password2')
            password3 = request.form.get('user_password3')
            image = request.files['user_image']
            if image:
                filename =secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                image.save(image_path)
                
                user.name = name
                user.email = email
                user.image =filename
                if  bcrypt.check_password_hash(user.password,password1):
                    if password2 == password3:
                        user.password = bcrypt.generate_password_hash(password3)
                    
                        try:
                            db.session.commit()
                            flash('data updated','success')
                            return redirect(url_for('changeprofile',id=user.id))
                        except Exception as e:
                             print(e)
                             flash('data updated','success')
                             return redirect(url_for('changeprofile',id=user.id))
                    else:
                            flash('password doesnt match','danger')
                            return redirect(url_for('changeprofile',id=user.id))
                else:
                    flash('wrong password you remembered','danger')
                    return redirect(url_for('changeprofile',id=user.id))
            else:
                user.name = name
                user.email = email
                
                if  bcrypt.check_password_hash(user.password,password1):
                    if password2 == password3:
                        user.password = bcrypt.generate_password_hash(password3)
                    
                        try:
                            db.session.commit()
                            flash('data updated','success')
                            return redirect(url_for('changeprofile',id=user.id))
                        except Exception as e:
                            flash('data updated','success')
                            return redirect(url_for('changeprofile',id=user.id))
        return redirect(url_for('changeprofile',id=user.id))
@app.route('/all_products')
def all_products():
    products = Products.query.all()
    category= Category.query.all()
    brand= Brands.query.all() 
    website = Website.query.filter_by(id=1).first()
    return render_template('all_products.html', products=products, category=category, brands=brand, website=website)
def update_total_price(order_id):
    """Update the total price of an order."""
    order = Orders.query.get(order_id)
    if order:
        total = sum(item.quantity * item.product.price for item in order.items)
        order.total_price = total
        db.session.commit()
@app.route('/add-to-cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
   
    item_to_add = Products.query.get(item_id)
    item_exists = Carts.query.filter_by(product_id=item_id,user_id=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            flash(f' Quantity of { item_exists.products.name } has been updated','success')
            return redirect(request.referrer)
        except Exception as e:
            print('Quantity not Updated', e)
            flash(f'Quantity of { item_exists.products.name } not updated','danger')
            return redirect(request.referrer)

    new_cart_item = Carts()
    new_cart_item.quantity = 1
    new_cart_item.product_id = item_to_add.id
    new_cart_item.user_id = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.products.name} added to cart','success')
        return redirect(request.referrer)
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.products.name} has not been added to cart','danger')
@app.route('/view_cart')
@login_required
def view_cart():
    website = Website.query.filter_by(id=1).first()
    current_user_id = current_user.id  # Assuming user is logged in with id 1
    cart_items = Carts.query.filter_by(user_id=current_user_id).all()
    total = sum([item.quantity * item.products.price for item in cart_items])
    return render_template('cart.html', cart=cart_items, total=total ,    website = website)

@app.route('/update_cart_quantity', methods=['POST'])
@login_required
def update_cart_quantity():
    data = request.json
    cart_item_id = data.get('cart_item_id')
    new_quantity = data.get('quantity')

    cart_item = Carts.query.get(cart_item_id)
    if cart_item:
        cart_item.quantity = new_quantity
        db.session.commit()
        updated_total_price = cart_item.quantity * cart_item.products.price
        return jsonify({"message": "Cart item updated successfully", "quantity": cart_item.quantity, "updated_total_price": updated_total_price})
    else:
        return jsonify({"error": "Cart item not found"}), 404
@app.route('/remove_cart_item', methods=['POST'])
@login_required
def remove_cart_item():
    data = request.json
    cart_item_id = data.get('cart_item_id')

    cart_item = Carts.query.get(cart_item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Cart item removed successfully"})
    else:
        return jsonify({"error": "Cart item not found"}), 404
@app.route('/place-order', methods=['GET','POST'])
@login_required
def place_order():
    current_user_id = current_user.id  # Assuming the user is logged in with id 1
   
    
    if request.method == "POST":
        id = request.form.get('product_id')
        cart_items = Carts.query.filter_by(user_id=current_user_id, product_id=id).first()
        product = Products.query.filter_by(id=id).first()
        
       
        new_order = Orders(
        user_id=current_user_id,
        product_id=cart_items.product_id,
        Name = request.form['name'],
        Email = request.form['email'],
        Phone = request.form['phone'],
        alternate_number = request.form['alt_num'],
        address = request.form['address'], 
        order_status='Pending',
        Payment_mode=request.form.get('Payment_mode'),# Example payment mode
        total_price = product.price,
        Delivery_date = ""
        )
        db.session.add(new_order)

        Carts.query.filter_by(user_id=current_user_id,product_id=id).delete()
        db.session.commit()
        return redirect(url_for('view_cart'))
@app.route('/order-shipping/<int:id>')
@login_required
def ordershipping(id):
    product_id = id
    website = Website.query.filter_by(id=1).first()
    return render_template("place_order.html",product_id=product_id,website=website)
@app.route('/all-orders')
@login_required
def all_orders():
    user_active = Users.query.filter_by(id=current_user.id).first()
    website = Website.query.filter_by(id=1).first()
    all_orders = Orders.query.filter_by(Email=user_active.email).all()
    print(all_orders)
    return render_template('orders_all.html', orders=all_orders, website=website)
@app.route('/admin-show-users', methods=['GET','POST'])
@login_required
def show_users():
   if current_user.user_type==1:
        
        page = request.args.get('page', 1, type=int)  # বর্তমান পেজ নম্বর
        per_page = 3
        user = Users.query.paginate(page=page, per_page=per_page)
        print(len(user.items))
        return render_template('admin-show_users.html',users=user)
   else:
       flash("unauthorized access",'danger')
       return redirect(url_for('home'))
@app.route("/update-role/<int:id>",methods=['GET','POST'])
@login_required
def update_role(id):
    if request.method == "POST":
            user_role=request.form.get('user_type')
            print(user_role)
            user_id = id
            users = Users.query.filter_by(id=user_id).first()
            users.user_type = user_role
            try:
                db.session.commit()
                flash(f"{users.name} Role Changed","success")
                return redirect(url_for("show_users"))
            except Exception as e:
               flash(f"{users.name} Role Changed","success")
               return redirect(url_for("show_users"))
@app.route("/delete-user/<int:id>")
@login_required
def delete_user(id):
    if current_user.user_type == 1:
        user = Users.query.filter_by(id=id).first()
        try:
            db.session.delete(user)
            db.session.commit()
            flash(f"{user.name} Deleted Successfully" ,'success')
            return redirect(url_for('show_users'))
        except Exception as e:
            flash(f"{user.name} Deleted Successfully" ,'success')
            return redirect(url_for('show_users'))
    else:
         flash(f"{user.name} not Deleted Successfully",'danger')
         return redirect(url_for('show_users'))
    
@app.route('/admin_all_orders')
@login_required
def admin_all_orders():
    if current_user.user_type == 1:
        page = request.args.get('page',1 ,type=int)
        per_page = 3
        all_orders = Orders.query.paginate(page=page, per_page=per_page)
        return render_template("all_orders.html",orders=all_orders)
    else:
        flash("Unauthorized access","danger")
        return redirect(url_for('login'))
@app.route("/edit_order/<int:id>",methods=['GET','POST'])
@login_required
def edit_orders(id):
    if current_user.user_type == 1:
        if request.method == "POST":
            delivery_date = request.form.get("delivery_date")
            order_status = request.form.get("order_status")
            order = Orders.query.filter_by(id=id).first()
            order.Delivery_date =  delivery_date
            order.order_status = order_status
            try:
                db.session.commit()
                flash(f"{order.products.name} data Updated" , 'success')
                return redirect(url_for('admin_all_orders'))
            except Exception as e:
                print(e)
                flash(f"{order.products.name} data not Updated",'danger')
                return redirect(url_for('admin_all_orders'))
@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Save the contact query to the database
        contact_query = Contact(name=name, email=email, message=message)
        db.session.add(contact_query)
        db.session.commit()
        subject = f'Contact Form Submission from {name}'
        msg = Message(subject, recipients=['tanubasuchoudhury1997@gmail.com'])  # Change to your recipient
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        try:
            mail.send(msg)
            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send email: {str(e)}', 'error')
        
        return redirect(url_for('contact'))
    return redirect(url_for('home'))
        
        
        
@app.route('/admin-contact-info')
@login_required
def admincontact():
    if current_user.user_type == 1:
        page= request.args.get('page',1,type=int)
        per_page = 3
        contacts = Contact.query.paginate(page=page,per_page=per_page)
        return render_template("admin-contact.html", contacts=contacts)
    return render_template('index.html')
@app.route('/admin-contact-info/delete/<int:id>')
@login_required
def deletemsg(id):
    if current_user.user_type == 1:
        contact = Contact.query.filter_by(id=id).first()
        try:
            db.session.delete(contact)
            db.session.commit()
            flash("Message deleted",'success')
            return redirect(url_for('admincontact'))
        except Exception as e:
             flash("Message not deleted",'danger')
             return redirect(url_for('admincontact'))
    
@app.route('/website', methods= ['GET','POST'])
@login_required

def website():
    if current_user.user_type ==1:
        website = Website.query.filter_by(id=1).first()
        if request.method == "POST":
            name = request.form.get('site_name')
            about_heading = request.form.get('aboutheading')
            about_text = request.form.get('abouttext')
            versetile_brand =request.form.get('versetile_brand')
            digital_agency = request.form.get('digital_agency')
            footer = request.form.get('footer')
            logo_img = request.files['logo']
            image1= request.files['image1']
            image2 =request.files['image2']
            image3 =request.files['image3']
            if logo_img and image1 and image2 and image3:
                logo_filename = secure_filename(logo_img.filename)
                logo_path  = os.path.join(app.config['UPLOAD_FOLDER'],logo_filename)
                logo_img.save(logo_path)
                print(logo_img)
                image1_filename = secure_filename(image1.filename)
                image1_path = os.path.join(app.config['UPLOAD_FOLDER'],image1_filename)
                image1.save(image1_path)
                image2_filename = secure_filename(image2.filename)
                image2_path = os.path.join(app.config['UPLOAD_FOLDER'],image2_filename)
                image2.save(image2_path)
                image3_filename = secure_filename(image3.filename)
                image3_path = os.path.join(app.config['UPLOAD_FOLDER'],image3_filename)
                image3.save(image3_path)
                website.name = name
                website.about_heading = about_heading
                website.about_text = about_text
                website.versetile_band = versetile_brand
                website.digital_agency = digital_agency
                website.footer = footer
                website.logo =logo_filename
                website.image1 = image1_filename
                website.image2 = image2_filename
                website.image3 = image3_filename
                try:
                    db.session.commit()
                    flash("website Data Updated", 'success')
                    return redirect(url_for('website'))
                except Exception as e:
                    print(e)
                    flash("website not Data Updated", 'danger')
                    return redirect(url_for('website'))
            else:
                website.name = name
                website.about_heading = about_heading
                website.about_text = about_text
                website.versetile_band = versetile_brand
                website.digital_agency = digital_agency
                website.footer = footer   
                try:
                    db.session.commit()
                    flash("website Data Updated", 'success')
                    return redirect(url_for('website'))
                except Exception as e:
                    print(e)
                    flash("website not Data Updated", 'danger')
                    return redirect(url_for('website'))
        return render_template("admin-websitechange.html",website=website)
def search_products(search_term):
    return Products.query.filter(Products.name.ilike(f'%{search_term}%')).all()
@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('q', '')
    
    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400
    
    results = search_products(search_term)
    return render_template('search.html', search_term=search_term, results=results)
    
if __name__ == "__main__":
    app.run(debug=True)
