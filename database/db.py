import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent


def get_connection():
	return sqlite3.connect(DB_PATH)


def init_db():
	with get_connection() as conn:
		cur = conn.cursor()
		cur.execute("""
		CREATE TABLE IF NOT EXISTS products (
			  id INTEGER PRIMARY KEY AUTOINCREMENT,
			  category TEXT,
			  country TEXT,
			  title TEXT,
			  description TEXT,
			  price TEXT,
			  photo TEXT,
			  in_stock INTEGER DEFAULT 1);

""")
		
		cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            product TEXT,
            comment TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
		conn.commit()
            
def get_products(category: str, country: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, title, description, price, photo, in_stock FROM products WHERE category=? AND country=?",
            (category, country),
        )
        rows = cur.fetchall()
        return [
            {
                "id": r[0],
                "title": r[1],
                "description": r[2],
                "price": r[3],
                "photo": r[4],
                "in_stock": bool(r[5]),
            }
            for r in rows
        ]

def add_lead(name: str, phone: str, product: str, comment: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO leads (name, phone, product, comment) VALUES (?, ?, ?, ?)",
            (name, phone, product, comment),
        )
        conn.commit()
        
if __name__ == "__main__":
      init_db()