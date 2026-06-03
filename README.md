# AssetHub Investment Tracker

> 📈 CLI Application · Python 3.7+  
> *Monitor & Manage your Investment Portfolio Efficiently*

---

| Menu Fitur | Kategori Aset | Batas Login | Dependencies |
|:----------:|:-------------:|:-----------:|:------------:|
| 11         | 8             | 3×          | 2            |

---

## 01 · Fitur Utama

### 📁 Portfolio Management

| Fitur | Deskripsi |
|-------|-----------|
| **View Portfolio** | Tampilkan semua aset beserta Market Value, Avg Cost, dan Unrealized P/L secara real-time. |
| **Add Asset** | Tambah aset baru dengan validasi format Asset ID unik (ASTxxx). |
| **Update Asset** | Edit quantity, harga beli, harga pasar, atau status — satu field atau sekaligus. |
| **Delete Asset** | Hapus aset dari portofolio dengan langkah konfirmasi sebelum eksekusi. |

### 💸 Transaksi

| Fitur | Deskripsi |
|-------|-----------|
| **Buy / Sell** | Transaksi BUY menghitung ulang weighted average price secara otomatis. SELL mengurangi posisi dan mencatat hasil jual. |
| **Transaction History** | Riwayat lengkap semua transaksi BUY & SELL dengan ringkasan total nilai per tipe. |

### 📊 Analytics

| Fitur | Deskripsi |
|-------|-----------|
| **Performance Summary** | Dashboard analitik: total nilai, ROI, aset terbaik & terburuk, breakdown per kategori. |
| **Search Asset** | Cari aset berdasarkan ID. |
| **Filter by Category** | Filter portofolio berdasarkan kategori aset. |
| **Sort Portfolio** | Urutkan berdasarkan Market Value / P/L ascending & descending. |

---

## 02 · Sistem Login

🔒 **PIN Akses (Default: `1234`)**

- Input tersembunyi dengan masking karakter `*`
- Maksimal **3 kali percobaan** — jika salah 3 kali, program otomatis berhenti
- Untuk mengubah PIN, edit variabel `PIN_AKSES` di bagian atas file `assethub.py`

---

## 03 · Instalasi

**Install Dependencies**
```bash
pip install tabulate pwinput
```

**Jalankan Aplikasi**
```bash
python Caps1_Assethub_Maulana_Imam_Rifai.py
```

> 📦 `tabulate` — render tabel di terminal · `pwinput` — masking input PIN

---

## 04 · Menu Utama

```
══════════════════════════════════════════════════════════════════════
           AssetHub Investment Tracker
     Monitor & Manage your Investment Portfolio Efficiently
══════════════════════════════════════════════════════════════════════

  PORTFOLIO MANAGEMENT          ANALYTICS
  ─────────────────────         ─────────────────────
  [1]  View Portfolio           [7]  Performance Summary
  [2]  Add Asset                [8]  Search Asset
  [3]  Update Asset             [9]  Filter by Category
  [4]  Delete Asset             [10] Sort Portfolio

  TRANSACTION                   SYSTEM
  ─────────────────────         ─────────────────────
  [5]  Buy / Sell Asset         [11] Exit
  [6]  Transaction History

──────────────────────────────────────────────────────────────────────

  Select Menu [1-11] : _
```

---

## 05 · Kategori Aset

| Kategori |
|----------|
| ₿ Crypto |
| 🥇 Commodity |
| 🇮🇩 Indonesia Stock |
| 🇺🇸 US Stock |
| 🏠 Real Estate |
| 📊 Mutual Fund |
| 💵 Cash |
| 📦 Others |

---

## 06 · Sample Portfolio Bawaan

| Asset ID | Nama Aset | Kategori | Unrealized P/L |
|----------|-----------|----------|----------------|
| AST001 | Bitcoin | Crypto | +Rp 40.000.000 |
| AST002 | Gold | Commodity | +Rp 750.000 |
| AST003 | BBCA | Indonesia Stock | +Rp 80.000 |
| AST004 | NVIDIA | US Stock | +Rp 3.450.000 |

> ⚠️ **Data tidak tersimpan permanen.** Seluruh portofolio dan riwayat transaksi bersifat **in-memory** — akan hilang saat program ditutup. Semua nilai menggunakan mata uang **Rupiah (Rp)**.

---

## 07 · Struktur Data Aset

| Field | Tipe | Keterangan |
|-------|------|------------|
| `asset_id` | String | ID unik format ASTxxx |
| `asset_name` | String | Nama aset |
| `category` | String | Kategori dari 8 pilihan yang tersedia |
| `quantity` | Float | Jumlah unit yang dimiliki |
| `buy_price` | Float | Harga rata-rata beli per unit (Rp) |
| `market_price` | Float | Harga pasar saat ini per unit (Rp) |
| `status` | String | Active / Inactive |
| `purchase_date` | String | Format YYYY-MM-DD |

---

## 08 · Konfigurasi

| Konstanta | Default | Keterangan |
|-----------|---------|------------|
| `APP_NAME` | AssetHub Investment Tracker | Nama aplikasi di header |
| `PIN_AKSES` | `1234` | PIN login — ganti sesuai kebutuhan |
| `LEBAR` | 70 | Lebar tampilan terminal (karakter) |

---

*AssetHub · Python CLI · tabulate · pwinput*
