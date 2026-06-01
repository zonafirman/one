# 🚀 One-CLI (rli-cli Universal Package & File Manager)

Aplikasi berbasis Terminal (CLI) super asisten yang dirancang menggunakan Python dan Shell Script untuk mempermudah manajemen paket, monitoring sistem, ekstraksi arsip, hingga penghapusan berkas lokal secara kilat di Ubuntu GNOME.

---

## ✨ Fitur Utama

* **Smart Search (`one search`)**: Mencari paket aplikasi repositori atau menyisir file lokal menggunakan flag `-f`.
* **Smart Installer (`one install`)**: Instalasi aplikasi otomatis atau pasang berkas lokal `.deb` via flag `-l`.
* **Universal Extractor (`one extract`)**: Membongkar segala format kompresi berkas (`.zip`, `.tar.gz`, `.rar`) tanpa pusing argumen bawaan.
* **System Monitor (`one system`)**: Pemantauan performa CPU, RAM, dan top proses secara real-time yang estetik.
* **Smart Remove (`one remove`)**: Menghapus paket aplikasi, mematikan service, atau **menghapus file/folder lokal secara total via flag `-d` (Kebal Permission/Auto-Sudo)**.
* **Smart Autocomplete**: Dukungan penuh tombol **Tab** untuk pelengkap argumen otomatis di terminal.

---

## 🛠️ Panduan Perintah Lengkap

Berikut adalah tabel rujukan cepat pemakaian perintah `one`, sayang:

| Perintah Utama | Argumen / Flag | Fungsi Perintah | Contoh Pemakaian |
| :--- | :--- | :--- | :--- |
| **`search`** | *Tanpa Flag* | Mencari aplikasi di repositori internet | `one search vlc` |
| | **`-f`** | Mencari file atau folder lokal di komputer | `one search -f tugas_kuliah` |
| **`install`** | *Tanpa Flag* | Mengunduh & pasang aplikasi dari internet | `one install neofetch` |
| | **`-l`** | Memasang file paket mentah lokal `.deb` | `one install -l ./discord.deb` |
| **`remove`** | *Tanpa Flag* | Menghapus aplikasi sistem / service internet | `one remove nginx` |
| | **`-d`** | **Menghapus file satuan ATAU folder beserta isinya** | `one remove -d folder_sampah` |
| **`extract`** | *Jalur Berkas* | Mengekstrak otomatis arsip kompresi apa saja | `one extract data.tar.gz` |
| **`system`** | *Tanpa Flag* | Menampilkan monitor performa komputer | `one system` |
| **`help`** | *Tanpa Flag* | Membuka lembar panduan navigasi internal | `one help` |

---

## ⚙️ Cara Instalasi Medis

1. Pastikan kamu berada di dalam direktori proyek utama, lalu berikan izin eksekusi pada skrip installer:
   ```bash
   chmod +x install.sh