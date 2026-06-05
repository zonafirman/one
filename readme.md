# 🚀 One-CLI Enterprise Edition

Asisten Terminal (CLI) serbaguna yang dirancang dengan Python untuk mengotomatisasi manajemen paket, sistem, dan jaringan secara profesional.

---

## ✨ Fitur Unggulan

*   **Unified Package Management**: Cari, instal, dan periksa paket dari APT, Flatpak, dan Snap secara bersamaan.
*   **System Diagnostics & Monitoring**: Dashboard TUI interaktif (`system`), diagnosa kesehatan (`doctor`), dan pembersihan sistem (`clean`).
*   **Network & Security Tools**: Audit keamanan dasar (`security`), monitor port (`ports`), dan manajemen layanan (`service`).
*   **Command History**: Lacak semua perintah yang dijalankan melalui `one` untuk audit dan pengulangan (`history`).
*   **File & Directory Utilities**: Ekstraksi arsip (`extract`), penghapusan aman (`file`), dan visualisasi pohon direktori (`tree`).
*   **Backup & Restore**: Cadangkan dan pulihkan daftar aplikasi yang terinstal dengan mudah.

---

## 📊 Referensi Perintah

| Perintah Utama | Argumen / Flag | Fungsi Perintah | Contoh Pemakaian |
| :--- | :--- | :--- | :--- |
| **`search`** | *Tanpa Flag* | Mencari paket di APT, Flatpak, & Snap secara simultan | `one search vlc` |
| | **`-f`** | Mencari file atau folder lokal secara cerdas | `one search -f tugas_kuliah` |
| **`info`** | *Nama Paket* | Mengintip informasi detail spesifikasi paket aplikasi | `one info spotify` |
| **`install`** | *Tanpa Flag* | Menu interaktif pasang aplikasi pilihan terdekat | `one install neovim` |
| | **`-l`** | Memasang file paket mentah `.deb` lokal | `one install -l ./discord.deb` |
| **`remove`** | *Tanpa Flag* | Menghapus aplikasi atau menonaktifkan *systemd service* | `one remove nginx` |
| | **`-d`** | Hapus file/folder permanen secara total (Auto-Sudo) | `one remove -d cache_lama` |
| **`extract`** | *Jalur Berkas* | Bongkar berkas kompresi (`.zip`, `.tar.gz`, `.rar`, `.7z`) | `one extract source.zip` |
| **`system`** | *Tanpa Flag* | Dashboard monitor performa komputer interaktif (TUI) | `one system` |
| **`doctor`** | *Tanpa Flag* | Diagnosa kesehatan hardware, thermal, RAM, dan disk | `one doctor` |
| **`clean`** | *Tanpa Flag* | Pembersihan standar cache gambar dan paket sistem | `one clean` |
| | **`--all`** | Pembersihan menyeluruh termasuk pembatasan ukuran log | `one clean --all` |
| **`ping`** | *Tanpa Flag* | Uji latensi koneksi internet real-time dengan kode warna | `one ping` |
| **`speedtest`** | *Tanpa Flag* | Ukur kecepatan unduh & unggah internet langsung | `one speedtest` |
| **`update`** | *Tanpa Flag* | Segarkan indeks repositori sistem (`apt update`) | `one update` |
| **`fetch`** | *Tanpa Flag* | Tampilkan ringkasan spesifikasi sistem | `one fetch` |
| **`upgrade`** | *Tanpa Flag* | Sinkronisasi otomatis menarik pembaruan kode Git terbaru | `one upgrade` |
| **`help`** | *Tanpa Flag* | Buka lembar panduan navigasi internal program | `one help` |
| **`backup`** | *Tanpa Flag* | Ekspor daftar paket terinstal ke `.json` | `one backup` |
| **`restore`** | *File Json* | Instal masal dari file backup | `one restore data.json` |
| **`ports`** | *Tanpa Flag* | Lihat port jaringan yang terbuka | `one ports` |
| **`security`** | *Tanpa Flag* | Jalankan audit keamanan dasar pada sistem | `one security` |
| **`service`** | *Aksi + Nama* | Kelola layanan systemd (start, stop, status) | `one service start nginx` |
| **`ip`** | *Tanpa Flag* | Tampilkan informasi identitas IP Lokal & Publik | `one ip` |
| **`kill`** | *Nama / Port* | Matikan proses berdasarkan nama atau Port | `one kill 8080` |
| **`history`** | *Tanpa Flag* | Tampilkan riwayat perintah yang dijalankan | `one history` |
| **`tree`** | *[Path]* | Tampilkan struktur direktori dalam format pohon | `one tree /var/log` |
---

## 🛠️ Panduan Instalasi & Pembaruan

### Langkah Pasang Baru
1. Pastikan folder proyek berada di direktori `~/one`.
2. Masuk ke folder dan berikan izin eksekusi pada skrip:
   ```bash
   cd ~/one && chmod +x install.sh