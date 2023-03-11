from flask import Flask, render_template
from db_models import db, role, user, file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:c55h32o5n4Mg@localhost/c_cloud'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/login')
def form():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
