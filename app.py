from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'qrmenu_gizli_admin_anahtari_123'

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

def get_db_connection():
    # Render üzerinde /tmp klasörünü kullanmak çökmesini engeller
    db_path = 'menu.db'
    if os.environ.get('RENDER'):
        db_path = '/tmp/menu.db'
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanı tablolarını güvenli oluşturma
with app.app_context():
    try:
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                image TEXT,
                description TEXT,
                kcal INTEGER
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_no TEXT NOT NULL,
                call_type TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Veritabanı oluşturulurken hata: {e}")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        import traceback
        return f"Kritik Hata Detayı: <pre>{traceback.format_exc()}</pre>", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['logged_in'] = True
                return redirect(url_for('admin'))
            else:
                error = 'Hatalı kullanıcı adı veya şifre!'
        return render_template('login.html', error=error)
    except Exception as e:
        return f"Kritik Login Hatası: {str(e)}", 500

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return render_template('admin.html')
    except Exception as e:
        return f"Admin Sayfası Hatası: {str(e)}", 500

@app.route('/waiter')
def waiter():
    try:
        return render_template('waiter.html')
    except Exception as e:
        return f"Garson Sayfası Hatası: {str(e)}", 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()
        return jsonify([dict(p) for p in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    if not session.get('logged_in'):
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO products (name, price, category, image, description, kcal) VALUES (?, ?, ?, ?, ?, ?)',
            (data['name'], data['price'], data['category'], data.get('image', ''), data.get('description', ''), data.get('kcal', 0))
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ürün eklendi!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Yetkisiz erişim'}), 403
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Ürün silindi!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/call', methods=['POST'])
def create_call():
    try:
        data = request.json
        table_no = data.get('table_no', 'Belirtilmemiş')
        call_type = data.get('call_type', 'Garson Çağır')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO calls (table_no, call_type) VALUES (?, ?)',
            (table_no, call_type)
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Çağrı iletildi!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calls', methods=['GET'])
def get_calls():
    try:
        conn = get_db_connection()
        calls = conn.execute("SELECT * FROM calls WHERE status = 'Pending' ORDER BY id DESC").fetchall()
        conn.close()
        return jsonify([dict(c) for c in calls])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calls/<int:call_id>/resolve', methods=['POST'])
def resolve_call(call_id):
    try:
        conn = get_db_connection()
        conn.execute("UPDATE calls SET status = 'Done' WHERE id = ?", (call_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Çağrı kapatıldı!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
