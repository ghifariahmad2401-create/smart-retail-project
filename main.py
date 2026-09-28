import sqlite3
import os
from datetime import datetime

# ==========================================
# 1. KONEKSI & INISIALISASI DATABASE
# ==========================================
DB_NAME = "smart_retail.db"

def inisialisasi_database():
    """Membuat tabel-tabel database dan user default jika belum ada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Membuat Tabel Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    
    # Membuat Tabel Produk
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_produk TEXT,
            harga_modal INTEGER,
            harga_jual INTEGER,
            stok INTEGER
        )
    ''')
    
    # Membuat Tabel Transaksi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            total_bayar INTEGER
        )
    ''')
    
    # Membuat Tabel Detail Transaksi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detail_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_transaksi INTEGER,
            id_produk INTEGER,
            jumlah INTEGER,
            subtotal INTEGER,
            FOREIGN KEY(id_transaksi) REFERENCES transaksi(id),
            FOREIGN KEY(id_produk) REFERENCES produk(id)
        )
    ''')
    
    # Insert Data Default User (Admin & Kasir) jika kosong
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", [
            ('admin', '1234', 'Admin'),
            ('kasir', '1234', 'Kasir')
        ])
        
    # Insert Data Sesuai Studi Kasus jika kosong
    cursor.execute("SELECT COUNT(*) FROM produk")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO produk (nama_produk, harga_modal, harga_jual, stok) VALUES (?, ?, ?, ?)", [
            ('Beras 5 Kg', 65000, 75000, 20),
            ('Gula 1 Kg', 15000, 18000, 30),
            ('Minyak Goreng', 18000, 22000, 25),
            ('Mie Instan', 2500, 3500, 100),
            ('Kopi Sachet', 1000, 1500, 50)
        ])
        
    conn.commit()
    conn.close()

# ==========================================
# 2. MODUL LOGIN SISTEM
# ==========================================
def login_sistem():
    """Fungsi otentikasi login pengguna."""
    print("\n" + "="*35)
    print("      LOGIN SYSTEM SMART-RETAIL      ")
    print("="*35)
    username = input("Username : ")
    password = input("Password : ")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        print(f"\n[✓] Login Berhasil! Selamat Datang, {user[0]} ({user[1]})")
        return {"username": user[0], "role": user[1]}
    else:
        print("\n[X] Login Gagal! Username atau Password salah.")
        return None

# ==========================================
# 3. MODUL KELOLA PRODUK (CRUD)
# ==========================================
def tambah_produk():
    print("\n--- TAMBAH PRODUK BARU ---")
    nama = input("Nama Barang : ")
    harga_modal = int(input("Harga Modal : "))
    harga_jual = int(input("Harga Jual  : "))
    stok = int(input("Stok        : "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produk (nama_produk, harga_modal, harga_jual, stok) VALUES (?, ?, ?, ?)",
                   (nama, harga_modal, harga_jual, stok))
    conn.commit()
    conn.close()
    print("[✓] Produk berhasil ditambahkan!")

def lihat_produk():
    print("\n------------------------------------------------------------")
    print(f"{'ID':<5} | {'Nama Barang':<25} | {'Harga Jual':<12} | {'Stok':<5}")
    print("------------------------------------------------------------")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama_produk, harga_jual, stok FROM produk")
    for row in cursor.fetchall():
        print(f"{row[0]:<5} | {row[1]:<25} | Rp{row[2]:<10,} | {row[3]:<5}")
    print("------------------------------------------------------------")
    conn.close()

def update_produk():
    lihat_produk()
    id_produk = int(input("\nMasukkan ID Produk yang ingin diubah: "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk WHERE id=?", (id_produk,))
    if not cursor.fetchone():
        print("[X] ID Produk tidak ditemukan!")
        conn.close()
        return
        
    nama = input("Nama Baru       : ")
    harga_jual = int(input("Harga Jual Baru : "))
    stok = int(input("Stok Baru       : "))
    
    cursor.execute("UPDATE produk SET nama_produk=?, harga_jual=?, stok=? WHERE id=?", 
                   (nama, harga_jual, stok, id_produk))
    conn.commit()
    conn.close()
    print("[✓] Data produk berhasil diperbarui!")

def hapus_produk():
    lihat_produk()
    id_produk = int(input("\nMasukkan ID Produk yang ingin dihapus: "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nama_produk FROM produk WHERE id=?", (id_produk,))
    produk = cursor.fetchone()
    
    if not produk:
        print("[X] ID Produk tidak ditemukan!")
        conn.close()
        return
        
    konfirmasi = input(f"Yakin menghapus produk '{produk[0]}'? (Y/T): ").upper()
    if konfirmasi == 'Y':
        cursor.execute("DELETE FROM produk WHERE id=?", (id_produk,))
        conn.commit()
        print("[✓] Produk berhasil dihapus!")
    else:
        print("[-] Penghapusan dibatalkan.")
    conn.close()

def kelola_produk_menu():
    while True:
        print("\n===== SUB-MENU KELOLA PRODUK =====")
        print("1. Tambah Produk")
        print("2. Lihat Daftar Produk")
        print("3. Update Data Produk")
        print("4. Hapus Produk")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih Menu (1-5): ")
        
        if pilihan == '1': tambah_produk()
        elif pilihan == '2': lihat_produk()
        elif pilihan == '3': update_produk()
        elif pilihan == '4': hapus_produk()
        elif pilihan == '5': break
        else: print("[X] Pilihan tidak valid!")

# ==========================================
# 4. MODUL PENCARIAN PRODUK
# ==========================================
def cari_produk():
    print("\n===== FITUR CARI PRODUK =====")
    print("1. Cari Berdasarkan Nama")
    print("2. Cari Berdasarkan ID Produk")
    pilihan = input("Pilih metode (1-2): ")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if pilihan == '1':
        keyword = input("Masukkan Kata Kunci Nama: ")
        cursor.execute("SELECT id, nama_produk, harga_jual, stok FROM produk WHERE nama_produk LIKE ?", (f"%{keyword}%",))
    elif pilihan == '2':
        id_cari = input("Masukkan ID Produk: ")
        cursor.execute("SELECT id, nama_produk, harga_jual, stok FROM produk WHERE id=?", (id_cari,))
    else:
        print("[X] Pilihan tidak valid.")
        conn.close()
        return

    hasil = cursor.fetchall()
    conn.close()
    
    if hasil:
        print("\n------------------------------------------------------------")
        print(f"{'ID':<5} | {'Nama Barang':<25} | {'Harga Jual':<12} | {'Stok':<5}")
        print("------------------------------------------------------------")
        for row in hasil:
            print(f"{row[0]:<5} | {row[1]:<25} | Rp{row[2]:<10,} | {row[3]:<5}")
        print("------------------------------------------------------------")
    else:
        print("\n[!] Produk tidak ditemukan.")

# ==========================================
# 5. MODUL KELOLA PRODUK (CRUD)
# ==========================================
def tambah_produk():
    """Fungsi bagi Admin untuk menambahkan item produk baru ke database."""
    print("\n--- TAMBAH PRODUK BARU ---")
    nama = input("Nama Barang : ")
    harga_modal = int(input("Harga Modal : "))
    harga_jual = int(input("Harga Jual  : "))
    stok = int(input("Stok        : "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produk (nama_produk, harga_modal, harga_jual, stok) VALUES (?, ?, ?, ?)",
                   (nama, harga_modal, harga_jual, stok))
    conn.commit()
    conn.close()
    print("[✓] Produk berhasil ditambahkan!")

def lihat_produk():
    """Menampilkan semua daftar produk aktif dalam bentuk tabel console."""
    print("\n------------------------------------------------------------")
    print(f"{'ID':<5} | {'Nama Barang':<25} | {'Harga Jual':<12} | {'Stok':<5}")
    print("------------------------------------------------------------")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama_produk, harga_jual, stok FROM produk")
    for row in cursor.fetchall():
        print(f"{row[0]:<5} | {row[1]:<25} | Rp{row[2]:<10,} | {row[3]:<5}")
    print("------------------------------------------------------------")
    conn.close()

def update_produk():
    """Mengubah nama, harga jual, dan stok produk berdasarkan input ID."""
    lihat_produk()
    id_produk = int(input("\nMasukkan ID Produk yang ingin diubah: "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk WHERE id=?", (id_produk,))
    if not cursor.fetchone():
        print("[X] ID Produk tidak ditemukan!")
        conn.close()
        return
        
    nama = input("Nama Baru       : ")
    harga_jual = int(input("Harga Jual Baru : "))
    stok = int(input("Stok Baru       : "))
    
    cursor.execute("UPDATE produk SET nama_produk=?, harga_jual=?, stok=? WHERE id=?", 
                   (nama, harga_jual, stok, id_produk))
    conn.commit()
    conn.close()
    print("[✓] Data produk berhasil diperbarui!")

def hapus_produk():
    """Menghapus produk dari database setelah melakukan konfirmasi konseptual (Y/T)."""
    lihat_produk()
    id_produk = int(input("\nMasukkan ID Produk yang ingin dihapus: "))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nama_produk FROM produk WHERE id=?", (id_produk,))
    produk = cursor.fetchone()
    
    if not produk:
        print("[X] ID Produk tidak ditemukan!")
        conn.close()
        return
        
    konfirmasi = input(f"Yakin menghapus produk '{produk[0]}'? (Y/T): ").upper()
    if konfirmasi == 'Y':
        cursor.execute("DELETE FROM produk WHERE id=?", (id_produk,))
        conn.commit()
        print("[✓] Produk berhasil dihapus!")
    else:
        print("[-] Penghapusan dibatalkan.")
    conn.close()

def kelola_produk_menu():
    """Sub-menu internal navigasi CRUD khusus manajemen produk."""
    while True:
        print("\n===== SUB-MENU KELOLA PRODUK =====")
        print("1. Tambah Produk")
        print("2. Lihat Daftar Produk")
        print("3. Update Data Produk")
        print("4. Hapus Produk")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih Menu (1-5): ")
        
        if pilihan == '1': tambah_produk()
        elif pilihan == '2': lihat_produk()
        elif pilihan == '3': update_produk()
        elif pilihan == '4': hapus_produk()
        elif pilihan == '5': break
        else: print("[X] Pilihan tidak valid!")


# ==========================================
# 6. MODUL PENCARIAN PRODUK
# ==========================================
def cari_produk():
    """Mencari data produk fleksibel berdasarkan kata kunci Nama atau ID khusus."""
    print("\n===== FITUR CARI PRODUK =====")
    print("1. Cari Berdasarkan Nama")
    print("2. Cari Berdasarkan ID Produk")
    pilihan = input("Pilih metode (1-2): ")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if pilihan == '1':
        keyword = input("Masukkan Kata Kunci Nama: ")
        cursor.execute("SELECT id, nama_produk, harga_jual, stok FROM produk WHERE nama_produk LIKE ?", (f"%{keyword}%",))
    elif pilihan == '2':
        id_cari = input("Masukkan ID Produk: ")
        cursor.execute("SELECT id, nama_produk, harga_jual, stok FROM produk WHERE id=?", (id_cari,))
    else:
        print("[X] Pilihan tidak valid.")
        conn.close()
        return

    hasil = cursor.fetchall()
    conn.close()
    
    if hasil:
        print("\n------------------------------------------------------------")
        print(f"{'ID':<5} | {'Nama Barang':<25} | {'Harga Jual':<12} | {'Stok':<5}")
        print("------------------------------------------------------------")
        for row in hasil:
            print(f"{row[0]:<5} | {row[1]:<25} | Rp{row[2]:<10,} | {row[3]:<5}")
        print("------------------------------------------------------------")
    else:
        print("\n[!] Produk tidak ditemukan.")


# ==========================================
# 7. MODUL TRANSAKSI PENJUALAN & CETAK STRUK
# ==========================================
def cetak_struk_ke_file(no_transaksi, tanggal, keranjang, total, bayar, kembalian):
    """BONUS (+10%): Mencetak struk belanja transaksi secara fisik ke berkas berkstensi file .txt"""
    nama_file = f"struk_TX_{no_transaksi}.txt"
    with open(nama_file, "w") as f:
        f.write("======== SMART RETAIL ========\n")
        f.write("        Toko Maju Jaya        \n")
        f.write("   Jl. Merdeka No. 10, Kota   \n")
        f.write("------------------------------\n")
        f.write(f"No Transaksi : TX-{no_transaksi}\n")
        f.write(f"Tanggal      : {tanggal}\n")
        f.write("------------------------------\n")
        for item in keranjang:
            f.write(f"{item['nama'][:14]:<14} {item['jumlah']:>2} x {item['harga']:>6,} = Rp{item['subtotal']:>7,}\n")
        f.write("------------------------------\n")
        f.write(f"TOTAL BELANJA : Rp{total:,}\n")
        f.write(f"UANG BAYAR    : Rp{bayar:,}\n")
        f.write(f"KEMBALIAN     : Rp{kembalian:,}\n")
        f.write("------------------------------\n")
        f.write("  Terima Kasih Atas Kunjungan \n")
        f.write("             Anda!            \n")
    print(f"[✓] Struk berhasil dicetak ke file eksternal: {nama_file}")

def transaksi_penjualan():
    """Modul antarmuka Kasir utama: entri keranjang, kalkulasi, serta validasi batas stok."""
    keranjang = []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    while True:
        lihat_produk()
        try:
            id_barang = int(input("Masukkan ID Barang yang ingin dibeli: "))
            cursor.execute("SELECT nama_produk, harga_jual, stok FROM produk WHERE id=?", (id_barang,))
            produk = cursor.fetchone()
            
            if not produk:
                print("[X] Produk tidak ditemukan! Silakan masukkan ID yang valid.")
                continue
                
            nama_produk, harga_jual, stok_tersedia = produk
            jumlah_beli = int(input(f"Masukkan Jumlah Pembelian untuk '{nama_produk}' (Stok: {stok_tersedia}): "))
            
            # 7. VALIDASI EVALUASI KUANTITAS STOK
            if jumlah_beli > stok_tersedia:
                print("\n" + "!"*40)
                print("ERROR: Stok tidak mencukupi.")
                print("Silakan masukkan jumlah yang lebih kecil.")
                print("!"*40)
                continue
                
            subtotal = harga_jual * jumlah_beli
            
            keranjang.append({
                'id_produk': id_barang,
                'nama': nama_produk,
                'harga': harga_jual,
                'jumlah': jumlah_beli,
                'subtotal': subtotal
            })
            print(f"[✓] Berhasil menambahkan {jumlah_beli} {nama_produk} ke keranjang belanja.")
            
        except ValueError:
            print("[X] Masukan input data wajib angka numerik!")
            continue

        ulang = input("\nTambah barang lain? (Y/T): ").upper()
        if ulang != 'Y':
            break
            
    if not keranjang:
        print("[-] Keranjang kosong. Operasi transaksi dibatalkan.")
        conn.close()
        return

    # Kalkulasi Akumulasi Nilai Total Belanja
    total_belanja = sum(item['subtotal'] for item in keranjang)
    print(f"\nTotal Belanja Anda: Rp{total_belanja:,}")
    
    # 8. MODUL PEMBAYARAN & HITUNG KEMBALIAN
    while True:
        try:
            uang_bayar = int(input("Uang Bayar    : Rp"))
            if uang_bayar < total_belanja:
                print("[X] Uang kurang! Masukkan nominal pembayaran yang sesuai.")
                continue
            break
        except ValueError:
            print("[X] Silakan isi nominal pembayaran dengan valid!")
            
    kembalian = uang_bayar - total_belanja
    print(f"Kembalian     : Rp{kembalian:,}")
    
    # 9. UPDATE STOK OTOMATIS & REKAM DATA HISTORI
    tanggal_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Simpan data transaksi induk (Master)
    cursor.execute("INSERT INTO transaksi (tanggal, total_bayar) VALUES (?, ?)", (tanggal_sekarang, total_belanja))
    id_transaksi_baru = cursor.lastrowid
    
    # Simpan detail item transaksi & sinkronisasi pengurangan stok secara otomatis
    for item in keranjang:
        cursor.execute("INSERT INTO detail_transaksi (id_transaksi, id_produk, jumlah, subtotal) VALUES (?, ?, ?, ?)",
                       (id_transaksi_baru, item['id_produk'], item['jumlah'], item['subtotal']))
        cursor.execute("UPDATE produk SET stok = stok - ? WHERE id = ?", (item['jumlah'], item['id_produk']))
        
    conn.commit()
    conn.close()
    print("\n[✓] Transaksi Berhasil Disimpan ke Database SQLite!")
    
    # Output visual pratinjau struk di layar Terminal Console
    print("\n========== SMART RETAIL ==========")
    for item in keranjang:
        print(f"{item['nama']:<15} {item['jumlah']} x {item['harga']} = Rp{item['subtotal']:,}")
    print("----------------------------------")
    print(f"TOTAL BELANJA : Rp{total_belanja:,}")
    print(f"UANG BAYAR    : Rp{uang_bayar:,}")
    print(f"KEMBALIAN     : Rp{kembalian:,}")
    print("==================================")
    
    # Eksekusi fungsi bonus cetak berkas struk eksternal TXT
    cetak_struk_ke_file(id_transaksi_baru, tanggal_sekarang, keranjang, total_belanja, uang_bayar, kembalian)


# ==========================================
# 8. MODUL LAPORAN PENJUALAN & RIWAYAT
# ==========================================
def laporan_penjualan():
    """Menyajikan kompilasi analisis ringkasan omzet performa penjualan toko."""
    print("\n===== LAPORAN PENJUALAN SISTEM =====")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Mengambil hitungan data transaksi & jumlah nominal omzet masuk
    cursor.execute("SELECT COUNT(*), SUM(total_bayar) FROM transaksi")
    res = cursor.fetchone()
    total_tx = res[0] if res and res[0] else 0
    total_revenue = res[1] if res and res[1] else 0
    
    print(f"Jumlah Transaksi : {total_tx} kali")
    print(f"Total Penjualan   : Rp{total_revenue:,}")
    
    # Mengambil produk terlaris dengan kalkulasi sum penjualan terbanyak
    cursor.execute('''
        SELECT p.nama_produk, SUM(dt.jumlah) as total_terjual 
        FROM detail_transaksi dt
        JOIN produk p ON dt.id_produk = p.id
        GROUP BY dt.id_produk
        ORDER BY total_terjual DESC LIMIT 1
    ''')
    terlaris = cursor.fetchone()
    if terlaris:
        print(f"Produk Terlaris  : {terlaris[0]} (Terjual {terlaris[1]} pcs)")
    else:
        print("Produk Terlaris  : Belum ada rekaman data penjualan")
        
    # Pemetaan sistem informasi stok menipis (di bawah batas minimal 10 unit)
    print("\nProduk yang harus segera restock (Stok < 10):")
    cursor.execute("SELECT nama_produk, stok FROM produk WHERE stok < 10")
    restock_list = cursor.fetchall()
    if restock_list:
        for p in restock_list:
            print(f" - {p[0]} ({p[1]} pcs)")
    else:
        print(" [✓] Semua kondisi stok produk aman terintegrasi (di atas 10 pcs).")
    conn.close()

def riwayat_transaksi():
    """Menampilkan histori catatan log nota belanja transaksi."""
    print("\n===== RIWAYAT TRANSAKSI =====")
    print(f"{'ID TX':<6} | {'Tanggal & Waktu':<18} | {'Total Bayar':<12}")
    print("--------------------------------------------------")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, tanggal, total_bayar FROM transaksi ORDER BY id DESC")
    for row in cursor.fetchall():
        print(f"TX-{row[0]:<3} | {row[1]:<18} | Rp{row[2]:<10,}")
    print("--------------------------------------------------")
    conn.close()

# ==========================================
# 9. DRIVER CODE / MAIN PROGRAM CORE
# ==========================================
def main():
    """Fungsi utama pengontrol alur program dan validasi hak akses menu."""
    # Inisialisasi database dan tabel saat pertama kali dijalankan
    inisialisasi_database()
    user_aktif = None
    
    while True:
        # Pengecekan sesi login pengguna aktif
        if not user_aktif:
            user_aktif = login_sistem()
            if not user_aktif:
                input("\nTekan Enter untuk melakukan login ulang sistem...")
                continue
                
        # Struktur Interface Utama Aplikasi Smart-Retail
        print("\n===== SMART RETAIL =====")
        print("1. Kelola Produk")
        print("2. Transaksi Penjualan")
        print("3. Cari Produk")
        print("4. Laporan Penjualan")
        print("5. Logout")
        pilihan = input("Pilih Menu (1-5): ")
        
        # Opsi 1: Modul Kelola Produk (Eksklusif Admin)
        if pilihan == '1':
            if user_aktif['role'] == 'Admin':
                kelola_produk_menu()
            else:
                print("\n[X] HAK AKSES DITOLAK: Fitur Kelola Produk hanya untuk level Admin!")
                
        # Opsi 2: Modul Transaksi Penjualan (Akses: Admin & Kasir)
        elif pilihan == '2':
            if user_aktif['role'] in ['Admin', 'Kasir']:
                transaksi_penjualan()
            else:
                print("\n[X] Anda tidak mempunyai otoritas akses menu transaksi.")
                
        # Opsi 3: Modul Pencarian Produk (Akses: Semua Pengguna)
        elif pilihan == '3':
            cari_produk()
            
        # Opsi 4: Modul Laporan Penjualan & Riwayat (Eksklusif Admin)
        elif pilihan == '4':
            if user_aktif['role'] == 'Admin':
                while True:
                    print("\n-- Menu Opsi Laporan --")
                    print("1. Ringkasan Laporan Statistik Penjualan")
                    print("2. Lihat Riwayat Log Semua Transaksi")
                    print("3. Kembali Ke Menu Utama")
                    sub_lap = input("Pilih Opsi (1-3): ")
                    
                    if sub_lap == '1': 
                        laporan_penjualan()
                    elif sub_lap == '2': 
                        riwayat_transaksi()
                    elif sub_lap == '3': 
                        break
                    else:
                        print("[X] Pilihan sub-menu salah, silakan ulangi.")
            else:
                print("\n[X] HAK AKSES DITOLAK: Menu Laporan Penjualan eksklusif hanya untuk Admin!")
                
        # Opsi 5: Sistem Logout / Keluar Sesi Akun
        elif pilihan == '5':
            print(f"\n[-] Akun {user_aktif['username']} telah berhasil logout dari sistem.")
            user_aktif = None
            
        # Validasi jika input menu utama di luar angka 1-5
        else:
            print("[X] Input pilihan menu salah, silakan ulangi kembali!")

if __name__ == "__main__":
    main()

