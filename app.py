from flask import Flask, render_template
from models import db, User, DimSiswa, DimBuku, FactAktivitasBaca

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/literasi_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'kunci_rahasia_literasi_2024'

# --- CONNECTING DB WITH APP ---
db.init_app(app)

# --- ROUTE ---
@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/buku_table')
def buku_table():
    return render_template('buku_table.html')

@app.route('/siswa_table')
def siswa_table():
    return render_template('siswa_table.html')

@app.route('/aktivitasbaca_table')
def aktivitasbaca_table():
    return render_template('aktivitasbaca_table.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

# --- MAIN ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)