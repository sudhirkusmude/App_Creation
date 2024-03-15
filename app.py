from flask import Flask,render_template,redirect,request,url_for
import mysql.connector


app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('login.html')

@app.route('/greet')
def greet():
    return render_template("greet.html")

# MySQL Configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'salesdb'
}

def execute_query(query, params=None):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor = execute_query(query, (username, password))
    
    # Check if cursor is None (query execution failed)
    if cursor is None:
        return "An error occurred while processing your request."
    
    user = cursor.fetchone()
    if user:
        return "Login successful!"
    else:
        return "Invalid username or password."


if __name__=="__main__":
    app.run(debug=True)