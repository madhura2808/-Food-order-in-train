# from curses import flash
from flask import Flask, make_response, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

# In-memory storage for orders (for demonstration purposes)
orders = []

def create_connection():
    con = sqlite3.connect('instance/database.db')
    cur = con.cursor()
    return con, cur

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        food_item = request.form['food_item']
        train_number = request.form['train_number']
        delivery_location = request.form['delivery_location']
        orders.append({
            'food_item': food_item,
            'train_number': train_number,
            'delivery_location': delivery_location
        })
        return redirect(url_for('orders_list'))
    return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def order_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        food_item = request.form['food_item']
        quantity = request.form['quantity']
        train_number = request.form['train_number']
        compartment_no = request.form['compartment_no']
        seat_number = request.form['seat_number']
        orders.append({
            'name': name,
            'email': email,
            'food_item': food_item,
            'quantity': quantity,
            'train_number': train_number,
            'compartment_no': compartment_no,
            'seat_number': seat_number
        })
        return redirect(url_for('orders_list'))
    return render_template('order_form.html')

@app.route('/orders')
def orders_list():
    return render_template('orders_list.html', orders=orders)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            username = request.form.get('username').title()
            email = request.form.get('email').title()
            password = request.form.get('password').title()
            print(username, email, password)
            
            con, cur= create_connection()
            isAdmin=cur.execute('select name from access').fetchone()
            if isAdmin:
                role = request.form.get('role').title()

                cur.execute("insert into access(name, email, role, password) values(?, ?, ?, ?)",(username, email, role, password))
                con.commit()
                return "<script>alert('You are registered as Shopkeeper or Salesman. Kindly login with your credentials.');window.location.href = '/signup';</script>"

                
            else:
                cur.execute("insert into access(name, email, role, password) values(?, ?, ?, ?)",(username, email, 'Admin', password))
                con.commit()
                return "<script>alert('You are registered as admin. Kindly login with your credentials.');window.location.href = '/signup';</script>"

                
            # You might want to add the user to a database here
        
        return render_template('signup.html')

    except Exception as error:
        return f"<script>alert('{error}');window.location.href = '/signup';</script>"
    
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            number = request.form.get('number')
            message = request.form.get('message')

            # Print to console (for debugging)
            print(f"Name: {name}, Email: {email}, Number: {number}, Message: {message}")

            # Insert into feedback table
            con, cur = create_connection()
            cur.execute(
                "INSERT INTO feedback (name, email, number, message) VALUES (?, ?, ?, ?)",
                (name, email, number, message)
            )
            con.commit()
            con.close()

            return "<script>alert('Thank you for your feedback!');window.location.href = '/feedback';</script>"
        except Exception as e:
            return f"<script>alert('Error: {e}');window.location.href = '/feedback';</script>"

    return render_template('index.html')

@app.route('/admindash')
def admin_dashboard():
    return render_template('admin-dash-menu.html')


@app.route('/toggle_theme_admin', methods=['POST'])
def toggle_theme_admin():
    theme = request.form.get('theme')
    response = make_response(render_template('Admin-Dashboard.html'))
    response.set_cookie('theme', theme)
    return response


@app.route('/manage_train', methods=['GET'])
def manage_train():
    try:
        con, cur = create_connection()
        sql_query = "SELECT * FROM traininfo"
        cur.execute(sql_query)
        train = cur.fetchall()
        return render_template('manage_train.html', train=train)
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/manage_train';</script>"

# Route to add a new train
@app.route('/add_train', methods=['POST'])
def add_train():
    train_no = request.form['train_no']
    train_name = request.form['train_name']
    date = request.form['date']
    route = request.form['route']

    try:
        con, cur = create_connection()
        cur.execute("INSERT INTO traininfo(train_no, name, date, route) VALUES(?, ?, ?, ?)",
                    (train_no, train_name, date, route))
        con.commit()
        return redirect('/manage_train')
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/manage_train';</script>"

# Route to update an existing train
@app.route('/update_train', methods=['POST'])
def update_train():
    train_id = request.form['train_id']
    train_no = request.form['train_no']
    train_name = request.form['train_name']
    date = request.form['date']
    route = request.form['route']

    try:
        con, cur = create_connection()
        cur.execute("UPDATE traininfo SET train_no = ?, name = ?, date = ?, route = ? WHERE id = ?",
                    (train_no, train_name, date, route, train_id))
        con.commit()
        return redirect('/manage_train')
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/manage_train';</script>"

# Route to delete a train
@app.route('/delete_train', methods=['POST'])
def delete_train():
    train_id = request.form['train_id']

    try:
        con, cur = create_connection()
        cur.execute("DELETE FROM traininfo WHERE id = ?", (train_id,))
        con.commit()
        return redirect('/manage_train')
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/manage_train';</script>"





@app.route('/shopdetails', methods=['GET'])
def shopdetails():
    try:
        con,  cur = create_connection()
        cur.execute("SELECT * FROM shopinfo")
        shop = cur.fetchall()
        return render_template('shop_details.html', shop=shop)
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/shopdetails';</script>"

@app.route('/add_shop', methods=['POST'])
def add_shop():
    name = request.form['name']
    username = request.form['username']
    shop_name = request.form['shop_name']
    address = request.form['address']
    
    try:
        con, cur = create_connection()
        cur.execute("INSERT INTO shopinfo (name, username, shop_name, address) VALUES (?, ?, ?, ?)",
                    (name, username, shop_name, address))
        con.commit()
        return redirect('/shopdetails')
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/shopdetails';</script>"

@app.route('/update_shop', methods=['POST'])
def update_shop():
    shop_id = request.form['shop_id']
    name = request.form['name']
    username = request.form['username']
    shop_name = request.form['shop_name']
    address = request.form['address']
    
    try:
        con, cur = create_connection()
        cur.execute("UPDATE shopinfo SET name = ?, username = ?, shop_name = ?, address = ? WHERE id = ?",
                    (name, username, shop_name, address, shop_id))
        con.commit()
        return redirect('/shopdetails')
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/manage_train';</script>"

@app.route('/delete_shop', methods=['POST'])
def delete_shop():
    shop_id = request.form['shop_id']
    
    try:
        con, cur = create_connection()
        cur.execute("DELETE FROM shopinfo WHERE id = ?", (shop_id,))
        con.commit()
        return redirect('/shopdetails')
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/shopdetails';</script>"
 
        
@app.route('/adminfeedback')
def adminfeedback():
    try:
        con, cur = create_connection()
        cur.execute(f"select * from feedback order by id desc")
        feedback=cur.fetchall()
        con.commit()
        con.close()
        return render_template('feedback.html', feedback=feedback)
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/adminfeedback';</script>"


@app.route('/viewbills')
def viewbills():
    return render_template('adm-viewbills.html')



@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/orderdetails')
def orderdetails():
    return render_template('adm-order_details.html')

@app.route('/salesmandash')
def salesman_dashboard():
    return render_template('salesman-dash-menu.html')

@app.route('/salesmancustomer')
def salesmancustomer():
    return render_template('salesman-customers.html')

@app.route('/update/<int:customer_id>')
def update_customer(customer_id):
    # Implement the logic to update customer with ID customer_id
    return f"Update customer {customer_id}"

@app.route('/delete/<int:customer_id>')
def delete_customer(customer_id):
    # Implement the logic to delete customer with ID customer_id
    return f"Delete customer {customer_id}"


@app.route('/salesmanbill')
def salesmanbill():
    return render_template('salesmanBills.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Placeholder for user authentication logic
        # user = register_collection.find_one({'email': username, 'password': password})
        # if user:
        #     session['username'] = username
        #     return redirect(url_for('admin_dashboard'))
        # else:
        #     msg = 'Invalid username or password'
    return render_template('login.html', msg=msg)

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/train_details')
def train_details():
    try:
        con, cur, = create_connection()
        cur.execute(f"select * from traininfo ORDER BY id DESC")
        train=cur.fetchall()
        con.commit()
        con.close()
        return render_template('train_detail.html', train=train)
    except Exception as e:
        return f"<script>alert('Error: {e}');window.location.href = '/train_details';</script>"


if __name__ == '__main__':
    app.run(debug=True)
