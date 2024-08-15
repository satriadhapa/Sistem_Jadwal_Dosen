from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Tambahkan logika autentikasi di sini
        return redirect(url_for('main.home'))
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Tambahkan logika pendaftaran di sini
        return redirect(url_for('main.login'))
    return render_template('register.html')
