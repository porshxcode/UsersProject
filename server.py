from flask import Flask, render_template, request , redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)

# first function shows all user data
@app.route("/userpage")
def index():
    mysql = connectToMySQL('users_db')	        # call the function, passing in the name of our db
    user_data = mysql.query_db('SELECT * FROM users;')  # call the query_db function, pass in the query as a string
    print(user_data)
    return render_template("userpage.html", user_data = user_data)
# second function is to show the form
@app.route('/adduser')
def form():
    print(request.form)
    return render_template('form.html')

# this is the process method adding the user to the database
@app.route('/adduserprocess', methods=["POST"])
def process():
    print (request.form)
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s ,%(ln)s ,%(em)s, NOW(), NOW() );"
    data = {
        'fn': request.form ['fn'],
        'ln': request.form ['ln'],
        'em': request.form ['em']
    }
    db = connectToMySQL('users_db')
    id= db.query_db(query,data)
    return redirect('/userpage/'+ str(id))

@app.route("/userpage/<id>")
def show(id):
    db = connectToMySQL('users_db')
    query = "SELECT * FROM users WHERE idusers = %(id)s;"

    data = {
        'id': int(id)
    }
    user_data = db.query_db(query,data)
    print (user_data)
    print(type(user_data))
    print(id)
    return render_template("show.html", user_data= user_data[0])


@app.route('/userpage/show_edit/<id>')
def show_edit(id):
    db = connectToMySQL('users_db')
    query = "SELECT * FROM users WHERE idusers = %(id)s;"
    
    data = {
        'id': int(id)
    }
    user_data = db.query_db(query,data)
    print (user_data)
    print(type(user_data))
    print(id)
    return render_template("edit.html",user_data= user_data[0])

@app.route("/editprocess/<id>", methods=["POST"])
def edit_process(id):
    print("inside edit process")
    db = connectToMySQL('users_db')
    query= "UPDATE users_db.users SET first_name = %(fn)s, last_name = %(ln)s , email = %(em)s WHERE (idusers = %(id)s);"

    data = {
        'fn': request.form ['fn'],
        'ln': request.form ['ln'],
        'em': request.form ['em'],
        'id': int(id)
    }
    user_data = db.query_db(query,data)
    print("*"*100)
    print (user_data)
    print(type(user_data))
    print(id)
    return redirect('/userpage/'+ str(id)) 

@app.route("/userpage/<id>/destroy")
def destroy(id):
    db = connectToMySQL("users_db")
    query = "DELETE FROM users WHERE idusers = %(id)s;"
    print(query)
    data = {
        'id': int(id)
    }
    db.query_db(query,data)
    return redirect("/userpage")


if __name__ == "__main__":
    app.run(debug=True)
