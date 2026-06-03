# 🚀 One-CLI (Universal Package, Network & System Assistant)

Aplikasi berbasis Terminal (CLI) super asisten yang dirancang menggunakan Python dan Shell Script untuk mengotomatisasi manajemen paket, penyegaran repositori, ekstraksi arsip lintas format, pengujian latensi serta kecepatan internet, hingga penarikan spesifikasi sistem yang interaktif dan estetik ala palet warna **Rosé Pine** di Linux (Ubuntu GNOME & KDE Plasma).

---

## ✨ Fitur Utama

* **Smart Search (`one search`)**: Mencari paket aplikasi repositori internet atau menyisir berkas lokal via flag `-f`.
* **Smart Installer (`one install`)**: Instalasi aplikasi otomatis dari internet atau pasang berkas mentah `.deb` lokal via flag `-l`.
* **Smart Remove (`one remove`)**: Menghapus paket aplikasi sistem, menonaktifkan service, atau menghapus file/folder lokal secara total via flag `-d` (Kebal Permission/Auto-Sudo).
* **Universal Extractor (`one extract`)**: Membongkar segala format kompresi berkas (`.zip`, `.tar.gz`, `.rar`) tanpa pusing argumen bawaan.
* **Premium System Monitor (`one system`)**: Pemantauan performa CPU, RAM, kapasitas DISK, dan daftar proses berjalan secara real-time yang interaktif (TUI) dengan desain berbingkai premium dan fitur *zebra-striping* warna Rosé Pine.
* **Network Ping Tester (`one ping`)**: Menguji latensi koneksi jaringan secara berkala ke server global dengan tampilan grafik mini yang bersih.
* **Smart Internet Speedtest (`one speedtest`)**: Mengukur kecepatan unduh (*download*) dan unggah (*upload*) internet secara akurat langsung dari kernel terminal dengan antarmuka yang ramah.
* **Repo Synchronizer (`one update`)**: Menyegarkan indeks paket repositori sistem (`apt update`) secara instan dengan satu perintah.
* **Beautiful Fetch (`one fetch`)**: Menampilkan ringkasan spesifikasi komputer dan logo minimalis kustom dengan tema warna Rosé Pine yang teduh.
* **Smart Autocomplete**: Dukungan penuh tombol **Tab** untuk pelengkap argumen otomatis di terminal secara multi-level.

---

## 📊 Daftar Perintah Lengkap (List Commands)

Berikut adalah tabel rujukan cepat pemakaian perintah `one` untuk mempermudah navigasi kamu, sayang:

| Perintah Utama | Argumen / Flag | Fungsi Perintah | Contoh Pemakaian |
| :--- | :--- | :--- | :--- |
| **`search`** | *Tanpa Flag* | Mencari aplikasi di repositori internet | `one search vlc` |
| | **`-f`** | Mencari berkas atau folder lokal di komputer | `one search -f data_kuliah` |
| **`install`** | *Tanpa Flag* | Mengunduh & pasang aplikasi dari internet | `one install neofetch` |
| | **`-l`** | Memasang file paket mentah lokal `.deb` | `one install -l ./discord.deb` |
| **`remove`** | *Tanpa Flag* | Menghapus aplikasi sistem dari komputer | `one remove nginx` |
| | **`-d`** | Menghapus file satuan ATAU folder padat beserta isinya | `one remove -d folder_sampah` |
| **`extract`** | *Jalur Berkas* | Mengekstrak otomatis arsip kompresi apa saja | `one extract data.tar.gz` |
| **`system`** | *Tanpa Flag* | Menampilkan monitor performa komputer real-time interaktif (Q untuk keluar) | `one system` |
| **`ping`** | *Tanpa Flag* | Melakukan tes latensi jaringan ke server DNS utama | `one ping` |
| **`speedtest`** | *Tanpa Flag* | Menguji kecepatan unduh & unggah internet secara *real-time* | `one speedtest` |
| **`update`** | *Tanpa Flag* | Menyegarkan daftar paket repositori sistem (`apt update`) | `one update` |
| **`fetch`** | *Tanpa Flag* | Menampilkan spesifikasi sistem estetik ala Rosé Pine | `one fetch` |
| **`help`** | *Tanpa Flag* | Membuka lembar panduan navigasi internal program | `one help` |

---

## 📊 Daftar Perintah Lengkap (List Commands)

Berikut adalah tabel rujukan cepat pemakaian perintah `one` untuk mempermudah navigasi kamu, sayang:

| Perintah Utama | Argumen / Flag | Fungsi Perintah | Contoh Pemakaian |
| :--- | :--- | :--- | :--- |
| **`search`** | *Tanpa Flag* | Mencari aplikasi di repositori internet | `one search vlc` |
| | **`-f`** | Mencari berkas atau folder lokal di komputer | `one search -f data_kuliah` |
| **`install`** | *Tanpa Flag* | Mengunduh & pasang aplikasi dari internet | `one install neofetch` |
| | **`-l`** | Memasang file paket mentah lokal `.deb` | `one install -l ./discord.deb` |
| **`remove`** | *Tanpa Flag* | Menghapus aplikasi sistem dari komputer | `one remove nginx` |
| | **`-d`** | Menghapus file satuan ATAU folder padat beserta isinya | `one remove -d folder_sampah` |
| **`extract`** | *Jalur Berkas* | Mengekstrak otomatis arsip kompresi apa saja | `one extract data.tar.gz` |
| **`system`** | *Tanpa Flag* | Menampilkan monitor performa komputer secara real-time | `one system` |
| **`update`** | *Tanpa Flag* | Menyegarkan daftar paket repositori sistem (`apt update`) | `one update` |
| **`fetch`** | *Tanpa Flag* | Menampilkan spesifikasi sistem estetik ala Rosé Pine | `one fetch` |
| **`help`** | *Tanpa Flag* | Membuka lembar panduan navigasi internal program | `one help` |

---

## 🛠️ Tutorial Instalasi (Universal Guide)

Ikuti langkah-langkah di bawah ini untuk memasang One-CLI di komputer kamu atau temanmu. **Pastikan kamu mengeksekusinya sebagai user biasa (bukan sebagai root/sudo su)** agar konfigurasi jalur direktori terpasang dengan benar.

### Langkah 1: Persiapan Berkas
Pastikan seluruh file proyek sudah berada di dalam folder repositori bernama `one` di direktori home kamu (`~/one`).

### Langkah 2: Berikan Izin Eksekusi Installer
Buka terminal, masuk ke folder proyek, dan berikan izin eksekusi pada skrip `install.sh`:
```bash
cd ~/one
chmod +x install.sh
```
### Langkah 3: Jalankan Skrip Installer

Eksekusi skrip installer utama tanpa menggunakan embel-embel `sudo`:

```bash
./install.sh

```

*Skrip ini secara cerdas akan mendeteksi tipe shell lingkungan kamu (Bash, Zsh, atau Fish Shell) dan mengonfigurasi jembatan profil terminal secara otomatis (termasuk terminal Konsole pada KDE Plasma).*

### Langkah 4: Muat Ulang Konfigurasi Terminal

Agar fungsi tombol Tab (autocomplete) dan perintah `one` langsung aktif, muat ulang konfigurasi terminalmu saat ini atau cukup **buka tab terminal baru**:

```bash
source ~/.bashrc

```

*(Jika menggunakan Zsh, silakan jalankan perintah `source ~/.zshrc`)*

---

## 💡 Tips Cara Pembaruan Kode Manual

Jika di masa mendatang ada penambahan fitur atau pembaruan kode di repositori GitHub, pengguna cukup mengetikkan perintah berantai ini untuk melakukan sinkronisasi instan tanpa perlu menginstal ulang dari awal:

```bash
cd ~/one && git pull

```

---

## 📝 Catatan Hak Akses & Keamanan

* **Deteksi Hak Akses Otomatis**: Beberapa fitur seperti `one remove -d` (hapus file/folder) dan `one update` (apt update) membutuhkan hak akses Administrator. Aplikasi ini dirancang secara cerdas untuk mendeteksi hak akses berkas; jika dibutuhkan, eskalasi keamanan (`sudo`) akan dipicu secara otomatis tanpa mengganggu kestabilan folder home user biasa.
* **Portabilitas Tinggi**: Karena konfigurasi internal memanfaatkan `PYTHONPATH` dinamis yang berbasis variabel `$HOME`, folder proyek `one` ini bebas dipindahkan ke user mana pun di sistem operasi berbasis Debian/Ubuntu tanpa merusak dependensi kode.
