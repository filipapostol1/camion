import sqlite3
from datetime import datetime

DB_FILE = "gestionale.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cronologia
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  data TEXT,
                  tipo TEXT,
                  cliente TEXT,
                  tratta TEXT,
                  totale TEXT)''')
    conn.commit()
    conn.close()

def salva_in_cronologia(tipo, cliente, tratta, totale):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    data_odierna = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.execute("INSERT INTO cronologia (data, tipo, cliente, tratta, totale) VALUES (?, ?, ?, ?, ?)",
              (data_odierna, tipo, cliente, tratta, totale))
    conn.commit()
    conn.close()

def carica_cronologia():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT data, tipo, cliente, tratta, totale FROM cronologia ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    
    return [{"Data": r[0], "Tipo": r[1], "Cliente": r[2], "Tratta": r[3], "Totale": r[4]} for r in rows]
