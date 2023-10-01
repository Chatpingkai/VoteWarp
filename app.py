from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = "peteza"


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login')
def login():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
        
    #     #test
    #     if username == 'admin' and password == 'password':
    #         session['username'] = username
    #         return redirect(url_for('home'))
    #     else:
    #         return render_template('index.html')
    # else:
    username = request.args.get('Username')
    password = request.args.get('Password')
    return render_template('testlogin.html', data = {"username":username, "password":password})




@app.route('/register')
def register():
    return render_template("Register.html")



@app.route('/home')
def home():
    return render_template("home.html")



@app.route('/lobby')
def lobby():
    return render_template("lobby.html")



if __name__ == "__main__":
    app.run(debug=True)

