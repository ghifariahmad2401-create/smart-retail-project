import sqlite3
from datetime import datetime


# ==========================================
# KONEKSI DATABASE
# ==========================================

conn = sqlite3.connect("smart_retail.db")
cursor = conn.cursor()


# ==========================================
# MEMBUAT TABEL USERS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")


# ==========================================
# MEMBUAT TABEL PRODUK
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_produk TEXT NOT NULL,
    harga_modal INTEGER NOT NULL,
    harga_jual INTEGER NOT NULL,
    stok INTEGER NOT NULL
)
""")


# ==========================================
# MEMBUAT TABEL TRANSAKSI
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal TEXT NOT NULL,
    total_bayar INTEGER NOT NULL
)
""")


# ==========================================
# MEMBUAT TABEL DETAIL TRANSAKSI
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS detail_transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaksi INTEGER NOT NULL,
    id_produk INTEGER NOT NULL,
    jumlah INTEGER NOT NULL,
    subtotal INTEGER NOT NULL,

    FOREIGN KEY (id_transaksi)
    REFERENCES transaksi(id),

    FOREIGN KEY (id_produk)
    REFERENCES produk(id)
)
""")


# ==========================================
# DATA USER AWAL
# ==========================================

users_awal = [
    ("admin", "admin123", "admin"),
    ("kasir", "kasir123", "kasir")
]

for username, password, role in users_awal:
    cursor.execute("""
    INSERT OR IGNORE INTO users
    (username, password, role)
    VALUES (?, ?, ?)
    """, (username, password, role))


# ==========================================
# DATA PRODUK AWAL
# ==========================================

produk_awal = [
    ("Beras 5 Kg", 65000, 75000, 20),
    ("Gula 1 Kg", 15000, 18000, 30),
    ("Minyak Goreng", 19000, 22000, 25),
    ("Mie Instan", 2500, 3500, 100)
]

for nama, modal, jual, stok in produk_awal:

    cursor.execute("""
    INSERT INTO produk
    (nama_produk, harga_modal, harga_jual, stok)
    SELECT ?, ?, ?, ?
    WHERE NOT EXISTS (
        SELECT 1
        FROM produk
        WHERE nama_produk = ?
    )
    """, (nama, modal, jual, stok, nama))


conn.commit()


# ==========================================
# FUNGSI LIHAT PRODUK
# ==========================================

def lihat_produk():

    cursor.execute("""
    SELECT id, nama_produk, harga_modal, harga_jual, stok
    FROM produk
    ORDER BY id
    """)

    data_produk = cursor.fetchall()

    print("\n================================")
    print("         DAFTAR PRODUK")
    print("================================")

    if not data_produk:
        print("Belum ada produk.")
        return

    for produk in data_produk:

        print("--------------------------------")
        print("ID          :", produk[0])
        print("Nama        :", produk[1])
        print("Harga Modal : Rp", produk[2])
        print("Harga Jual  : Rp", produk[3])
        print("Stok        :", produk[4])

    print("--------------------------------")


# ==========================================
# FUNGSI TAMBAH PRODUK
# ==========================================

def tambah_produk():

    print("\n================================")
    print("         TAMBAH PRODUK")
    print("================================")

    nama = input("Nama produk : ")

    try:
        modal = int(input("Harga modal : "))
        jual = int(input("Harga jual  : "))
        stok = int(input("Jumlah stok : "))

        if modal < 0 or jual < 0 or stok < 0:
            print("Nilai tidak boleh negatif.")
            return

    except ValueError:
        print("Harga dan stok harus berupa angka.")
        return

    cursor.execute("""
    INSERT INTO produk
    (nama_produk, harga_modal, harga_jual, stok)
    VALUES (?, ?, ?, ?)
    """, (nama, modal, jual, stok))

    conn.commit()

    print("\nProduk berhasil ditambahkan!")


# ==========================================
# FUNGSI HAPUS PRODUK
# ==========================================

def hapus_produk():

    print("\n================================")
    print("         HAPUS PRODUK")
    print("================================")

    lihat_produk()

    try:
        id_produk = int(input("\nMasukkan ID produk : "))
    except ValueError:
        print("ID harus berupa angka.")
        return

    cursor.execute("""
    SELECT nama_produk
    FROM produk
    WHERE id = ?
    """, (id_produk,))

    produk = cursor.fetchone()

    if produk is None:
        print("Produk tidak ditemukan.")
        return

    konfirmasi = input(
        f"Yakin ingin menghapus {produk[0]}? (y/n): "
    ).lower()

    if konfirmasi == "y":

        cursor.execute("""
        DELETE FROM produk
        WHERE id = ?
        """, (id_produk,))

        conn.commit()

        print("Produk berhasil dihapus!")

    else:
        print("Penghapusan dibatalkan.")


# ==========================================
# MENU KELOLA PRODUK
# ==========================================

def menu_produk():

    while True:

        print("\n================================")
        print("         KELOLA PRODUK")
        print("================================")
        print("1. Lihat Produk")
        print("2. Tambah Produk")
        print("3. Hapus Produk")
        print("4. Kembali")
        print("================================")

        pilihan = input("Pilih menu : ")

        if pilihan == "1":

            lihat_produk()

        elif pilihan == "2":

            tambah_produk()

        elif pilihan == "3":

            hapus_produk()

        elif pilihan == "4":

            break

        else:

            print("Pilihan tidak tersedia!")


# ==========================================
# LIHAT TRANSAKSI
# ==========================================

def lihat_transaksi():

    print("\n================================")
    print("         DATA TRANSAKSI")
    print("================================")

    cursor.execute("""
    SELECT id, tanggal, total_bayar
    FROM transaksi
    ORDER BY id DESC
    """)

    transaksi = cursor.fetchall()

    if not transaksi:
        print("Belum ada transaksi.")
        return

    for data in transaksi:

        print("--------------------------------")
        print("ID Transaksi :", data[0])
        print("Tanggal      :", data[1])
        print("Total Bayar  : Rp", data[2])


# ==========================================
# LIHAT USER
# ==========================================

def lihat_user():

    print("\n================================")
    print("           DATA USER")
    print("================================")

    cursor.execute("""
    SELECT id, username, role
    FROM users
    ORDER BY id
    """)

    users = cursor.fetchall()

    for user in users:

        print("--------------------------------")
        print("ID       :", user[0])
        print("Username :", user[1])
        print("Role     :", user[2])


# ==========================================
# LIHAT STOK
# ==========================================

def lihat_stok():

    print("\n================================")
    print("           STOK PRODUK")
    print("================================")

    cursor.execute("""
    SELECT id, nama_produk, stok
    FROM produk
    ORDER BY id
    """)

    stok_produk = cursor.fetchall()

    for produk in stok_produk:

        print("--------------------------------")
        print("ID     :", produk[0])
        print("Produk :", produk[1])
        print("Stok   :", produk[2])


# ==========================================
# TRANSAKSI KASIR
# ==========================================

def transaksi_kasir():

    print("\n================================")
    print("          TRANSAKSI")
    print("================================")

    lihat_produk()

    try:
        id_produk = int(input("\nMasukkan ID produk : "))
        jumlah = int(input("Jumlah beli        : "))

        if jumlah <= 0:
            print("Jumlah harus lebih dari 0.")
            return

    except ValueError:
        print("ID dan jumlah harus berupa angka.")
        return

    cursor.execute("""
    SELECT nama_produk, harga_jual, stok
    FROM produk
    WHERE id = ?
    """, (id_produk,))

    produk = cursor.fetchone()

    if produk is None:

        print("Produk tidak ditemukan.")
        return

    nama_produk = produk[0]
    harga_jual = produk[1]
    stok = produk[2]

    if jumlah > stok:

        print("\nStok tidak mencukupi!")
        print("Stok tersedia :", stok)

        return

    subtotal = harga_jual * jumlah

    print("\n================================")
    print("        DETAIL TRANSAKSI")
    print("================================")
    print("Produk   :", nama_produk)
    print("Harga    : Rp", harga_jual)
    print("Jumlah   :", jumlah)
    print("Subtotal : Rp", subtotal)

    konfirmasi = input("\nSimpan transaksi? (y/n): ").lower()

    if konfirmasi != "y":

        print("Transaksi dibatalkan.")
        return

    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simpan transaksi
    cursor.execute("""
    INSERT INTO transaksi
    (tanggal, total_bayar)
    VALUES (?, ?)
    """, (tanggal, subtotal))

    id_transaksi = cursor.lastrowid

    # Simpan detail transaksi
    cursor.execute("""
    INSERT INTO detail_transaksi
    (id_transaksi, id_produk, jumlah, subtotal)
    VALUES (?, ?, ?, ?)
    """, (
        id_transaksi,
        id_produk,
        jumlah,
        subtotal
    ))

    # Kurangi stok
    cursor.execute("""
    UPDATE produk
    SET stok = stok - ?
    WHERE id = ?
    """, (jumlah, id_produk))

    conn.commit()

    print("\n================================")
    print("     TRANSAKSI BERHASIL")
    print("================================")
    print("ID Transaksi :", id_transaksi)
    print("Produk       :", nama_produk)
    print("Jumlah       :", jumlah)
    print("Total Bayar  : Rp", subtotal)
    print("Tanggal      :", tanggal)


# ==========================================
# MENU ADMIN
# ==========================================

def menu_admin():

    while True:

        print("\n==============================")
        print("          MENU ADMIN")
        print("==============================")
        print("1. Kelola Produk")
        print("2. Kelola Transaksi")
        print("3. Kelola User")
        print("4. Lihat Stok")
        print("5. Logout")
        print("==============================")

        pilihan = input("Pilih menu : ")

        if pilihan == "1":

            menu_produk()

        elif pilihan == "2":

            lihat_transaksi()

        elif pilihan == "3":

            lihat_user()

        elif pilihan == "4":

            lihat_stok()

        elif pilihan == "5":

            print("\nLogout berhasil.")
            break

        else:

            print("\nPilihan tidak tersedia!")


# ==========================================
# MENU KASIR
# ==========================================

def menu_kasir():

    while True:

        print("\n==============================")
        print("          MENU KASIR")
        print("==============================")
        print("1. Lihat Produk")
        print("2. Transaksi")
        print("3. Lihat Stok")
        print("4. Logout")
        print("==============================")

        pilihan = input("Pilih menu : ")

        if pilihan == "1":

            lihat_produk()

        elif pilihan == "2":

            transaksi_kasir()

        elif pilihan == "3":

            lihat_stok()

        elif pilihan == "4":

            print("\nLogout berhasil.")
            break

        else:

            print("\nPilihan tidak tersedia!")


# ==========================================
# SISTEM LOGIN
# ==========================================

print("\n================================")
print("          SMART RETAIL")
print("================================")
print("          SISTEM LOGIN")
print("================================")

username = input("Username : ")
password = input("Password : ")


cursor.execute("""
SELECT id, username, role
FROM users
WHERE username = ?
AND password = ?
""", (username, password))

user = cursor.fetchone()


# ==========================================
# HASIL LOGIN
# ==========================================

if user:

    user_id = user[0]
    username_login = user[1]
    role = user[2]

    print("\n================================")
    print("        LOGIN BERHASIL")
    print("================================")
    print("Selamat datang,", username_login)
    print("Role :", role)
    print("================================")

    if role == "admin":

        print("\nSelamat datang, Admin!")
        menu_admin()

    elif role == "kasir":

        print("\nSelamat datang, Kasir!")
        menu_kasir()

    else:

        print("Role tidak dikenali.")

else:

    print("\n================================")
    print("          LOGIN GAGAL")
    print("================================")
    print("Username atau password salah!")


# ==========================================
# MENUTUP DATABASE
# ==========================================

conn.close()

print("\nProgram selesai.")