from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3
import database

app = Flask(__name__)

def get_db_products():
    conn = sqlite3.connect('menu.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    conn.close()
    
    products = []
    for row in rows:
        products.append({
            'id': row['id'],
            'category': row['category'],
            'name': row['name'],
            'price': row['price'],
            'desc': row['desc'],
            'img': row['img'],
            'cal': row['cal']
        })
    return products

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/products')
def api_products():
    products = get_db_products()
    return jsonify(products)

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        category = request.form.get('category')
        name = request.form.get('name')
        price = float(request.form.get('price'))
        desc = request.form.get('desc')
        img = request.form.get('img')
        cal = request.form.get('cal')
        
        if not img:
            img = "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=400&q=80"

        conn = sqlite3.connect('menu.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (category, name, price, desc, img, cal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (category, name, price, desc, img, cal))
        conn.commit()
        conn.close()
        
        return redirect(url_for('admin_panel'))
        
    products = get_db_products()
    return render_template('admin.html', products=products)

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)