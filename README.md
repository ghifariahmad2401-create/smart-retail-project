# Smart Retail Project

Aplikasi kasir dan manajemen toko berbasis Python (CLI) dengan database SQLite. Mendukung login dengan dua peran, yaitu admin dan kasir.

## Fitur
**Admin**
- Kelola produk (lihat, tambah, hapus)
- Lihat data transaksi
- Lihat data user
- Lihat stok

**Kasir**
- Lihat produk
- Transaksi penjualan (stok otomatis berkurang)
- Lihat stok

## Teknologi
- Python 3
- SQLite (modul bawaan `sqlite3`)

## Cara Menjalankan
1. Clone repo ini
2. Pastikan Python 3 sudah terpasang
3. Jalankan: `python main.py`

## Akun Contoh
| Username | Password | Role |
|----------|----------|-------|
| admin | admin123 | admin |
| kasir | kasir123 | kasir |

## Struktur File
- `main.py` : program utama
- `smart_retail.db` : database SQLite
- `requirements.txt` : daftar dependensi
- `reset_db.py` : mengatur ulang database ke data awal
