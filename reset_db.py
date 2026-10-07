import sqlite3

DB_NAME = "smart_retail.db"

konfirmasi = input(
    "Semua data akan dihapus dan dibuat ulang. "
    "Ketik RESET untuk lanjut: "
)

if konfirmasi != "RESET":
    print("Dibatalkan.")
    raise SystemExit

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Hapus tabel lama (detail dulu karena punya foreign key)
for tabel in ("detail_transaksi", "transaksi", "produk", "users"):
    cursor.execute(f"DROP TABLE IF EXISTS {tabel}")

# Buat tabel
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_produk TEXT NOT NULL,
    harga_modal INTEGER NOT NULL,
    harga_jual INTEGER NOT NULL,
    stok INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal TEXT NOT NULL,
    total_bayar INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE detail_transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaksi INTEGER NOT NULL,
    id_produk INTEGER NOT NULL,
    jumlah INTEGER NOT NULL,
    subtotal INTEGER NOT NULL,
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id),
    FOREIGN KEY (id_produk) REFERENCES produk(id)
)
""")

# Data awal
cursor.executemany(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    [
        ("admin", "admin123", "admin"),
        ("kasir", "kasir123", "kasir"),
    ],
)

cursor.executemany(
    "INSERT INTO produk (nama_produk, harga_modal, harga_jual, stok) "
    "VALUES (?, ?, ?, ?)",
    [
        ("Beras 5 Kg", 65000, 75000, 20),
        ("Gula 1 Kg", 15000, 18000, 30),
        ("Minyak Goreng", 19000, 22000, 25),
        ("Mie Instan", 2500, 3500, 100),
    ],
)

conn.commit()
conn.close()

print("Database berhasil di-reset.")
