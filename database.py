import sqlite3

def init_db():
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            desc TEXT,
            img TEXT,
            cal TEXT
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        initial_products = [
            ('kahve', 'Caffè Latte', 75, 'Taze çekilmiş espresso, buharla ısıtılmış kadifemsi süt ve süt köpüğü.', 'https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?auto=format&fit=crop&w=400&q=80', '180 kcal'),
            ('kahve', 'Americano', 65, 'Sıcak su ile inceltilmiş yoğun espresso lezzeti.', 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=400&q=80', '15 kcal'),
            ('soguk', 'Iced Caramel Macchiato', 85, 'Espresso, soğuk süt, vanilya şurubu ve üzerinde nefis karamel sosu.', 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=400&q=80', '240 kcal'),
            ('tatli', 'San Sebastian Cheesecake', 120, 'İçi kremsi akışkan, üzeri hafif yanık İspanyol usulü orijinal cheesecake.', 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=400&q=80', '450 kcal'),
            ('tatli', 'Tiramisu Klasik', 110, 'Eski İtalyan tarifine sadık kalınarak mascarpone peyniri ve espresso ile hazırlanmış.', 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=400&q=80', '320 kcal'),
            ('kahvalti', 'Avokado & Poşe Yumurta Toast', 140, 'Ekşi mayalı ekmek üzerine ezilmiş avokado, poşe yumurta ve baharatlar.', 'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=400&q=80', '380 kcal')
        ]
        cursor.executemany('INSERT INTO products (category, name, price, desc, img, cal) VALUES (?, ?, ?, ?, ?, ?)', initial_products)
        conn.commit()
        
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Veritabanı başarıyla oluşturuldu!")