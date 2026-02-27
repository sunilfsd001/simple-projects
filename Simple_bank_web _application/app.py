from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "*********"

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='UserPassword*****',
    database='users'
)
cursor = conn.cursor()

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        userid = request.form.get("userid")
        password = request.form.get("password")
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        address = request.form.get("address")
        phone_number = request.form.get("phone")
        email = request.form.get("email")
        depamount = float(request.form.get("depamount"))

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO user_details (userid, password, first_name, last_name, address, phone_number, email) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (userid, hashed_password, first_name, last_name, address, phone_number, email)
        )
        cursor.execute(
            "INSERT INTO account (userid, acc_balance) VALUES (%s, %s)",
            (userid, depamount)
        )
        cursor.execute(
            "INSERT INTO transactions (userid, type, amount, details) VALUES (%s, %s, %s, %s)",
            (userid, "Deposit", depamount, "Initial Deposit")
        )

        conn.commit()
        return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        userid = request.form.get("userid")
        password = request.form.get("password")

        cursor.execute("SELECT * FROM user_details WHERE userid=%s", (userid,))
        user = cursor.fetchone()
        if user and check_password_hash(user[1], password):
            session['user'] = user
            cursor.execute("SELECT acc_balance FROM account WHERE userid=%s", (userid,))
            balance = cursor.fetchone()
            session['balance'] = balance
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Credentials"

@app.route("/dashboard")
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    balance = session.get('balance')
    return render_template("dashboard.html", user=user, balance=balance)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/profile")
def profile(): 
    user=session.get('user')
    if not user:
         return redirect(url_for('login')) 
    return render_template("profile.html", user=user)

@app.route("/update_profile", methods=["POST"])
def update_profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    address = request.form.get("address")
    phone = request.form.get("phone")
    email = request.form.get("email")

    cursor.execute(
        "UPDATE user_details SET first_name=%s, last_name=%s, address=%s, phone_number=%s, email=%s WHERE userid=%s",
        (firstname, lastname, address, phone, email, user[0])
    )
    conn.commit()

    session['user'] = (user[0], user[1], firstname, lastname, address, phone, email)
    return redirect(url_for('dashboard'))

@app.route("/change_password", methods=["POST"])
def change_password():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if not check_password_hash(user[1], current_password):
        return "Current password is incorrect"
    if new_password != confirm_password:
        return "New passwords do not match"

    hashed_new = generate_password_hash(new_password)
    cursor.execute("UPDATE user_details SET password=%s WHERE userid=%s", (hashed_new, user[0]))
    conn.commit()
    session['user'] = (user[0], hashed_new, user[2], user[3], user[4], user[5], user[6])
    return redirect(url_for('dashboard'))

@app.route('/deposit_ajax', methods=['POST'])
def deposit_ajax():
    data = request.get_json()
    amount = float(data['amount'])
    user = session.get('user')

    cursor.execute("UPDATE account SET acc_balance = acc_balance + %s WHERE userid=%s", (amount, user[0]))
    cursor.execute(
        "INSERT INTO transactions (userid, type, amount, details) VALUES (%s,%s,%s,%s)",
        (user[0], "Deposit", amount, "Deposit via dashboard")
    )
    conn.commit()

    cursor.execute("SELECT acc_balance FROM account WHERE userid=%s", (user[0],))
    new_balance = cursor.fetchone()[0]
    session['balance'] = (new_balance,)

    return jsonify({'new_balance': new_balance})

@app.route('/withdraw_ajax', methods=['POST'])
def withdraw_ajax():
    data = request.get_json()
    amount = float(data['amount'])
    user = session.get('user')

    cursor.execute("SELECT acc_balance FROM account WHERE userid=%s", (user[0],))
    balance = cursor.fetchone()[0]
    if amount > balance:
        return jsonify({'error': 'Insufficient balance'}), 400

    cursor.execute("UPDATE account SET acc_balance = acc_balance - %s WHERE userid=%s", (amount, user[0]))
    cursor.execute(
        "INSERT INTO transactions (userid, type, amount, details) VALUES (%s,%s,%s,%s)",
        (user[0], "Withdraw", amount, "Withdraw via dashboard")
    )
    conn.commit()

    cursor.execute("SELECT acc_balance FROM account WHERE userid=%s", (user[0],))
    new_balance = cursor.fetchone()[0]
    session['balance'] = (new_balance,)
    return jsonify({'new_balance': new_balance})

@app.route('/transfer_ajax', methods=['POST'])
def transfer_ajax():
    data = request.get_json()
    receiver = data['receiver']
    amount = float(data['amount'])
    sender = session.get('user')

    if sender[0] == receiver:
        return jsonify({'error': "Cannot transfer to self"}), 400

    cursor.execute("SELECT acc_balance FROM account WHERE userid=%s", (sender[0],))
    sender_balance = cursor.fetchone()[0]
    if amount > sender_balance:
        return jsonify({'error': "Insufficient balance"}), 400

    cursor.execute("SELECT acc_balance FROM account WHERE userid=%s", (receiver,))
    if not cursor.fetchone():
        return jsonify({'error': "Receiver does not exist"}), 400

    cursor.execute("UPDATE account SET acc_balance = acc_balance - %s WHERE userid=%s", (amount, sender[0]))
    cursor.execute("UPDATE account SET acc_balance = acc_balance + %s WHERE userid=%s", (amount, receiver))
    cursor.execute(
        "INSERT INTO transactions (userid, type, amount, details) VALUES (%s,%s,%s,%s)",
        (sender[0], "Transfer", amount, f"Transfered To {receiver}")
    )
    conn.commit()

    cursor.execute("SELECT acc_balance FROM account WHERE userid=%s", (sender[0],))
    new_balance = cursor.fetchone()[0]
    session['balance'] = (new_balance,)
    return jsonify({'new_balance': new_balance})

if __name__ == '__main__':
    app.run(debug=True)
