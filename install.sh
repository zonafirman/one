#!/bin/bash

# ====================================================================
#  Mantra Installer Universal One-CLI - Rosé Pine Edition 🌸
# ====================================================================

# 1. Tentukan Direktori Sumber dan Target (Universal Berbasis $HOME)
REPO_DIR="$HOME/one"  
CORE_DIR="$REPO_DIR/core"

echo "===================================================================="
echo " 🚀 Memulai Instalasi / Sinkronisasi Core One-CLI Universal"
echo "===================================================================="

# 2. Pastikan struktur folder inti sudah siap
if [ ! -d "$CORE_DIR" ]; then
    echo "📂 Membuat direktori sistem di $CORE_DIR..."
    mkdir -p "$CORE_DIR"
fi

# 3. Proses Penyalinan Modul Python & Shell secara Presisi
echo "📦 Menyalin jeroan kode, modul manajer, dan tema estetik..."

# Modul dasar sistem
cp "$REPO_DIR/core/package_manager.py" "$CORE_DIR/" 2>/dev/null
cp "$REPO_DIR/core/help_manager.py" "$CORE_DIR/" 2>/dev/null
cp "$REPO_DIR/core/file_manager.py" "$CORE_DIR/" 2>/dev/null

# 🔥 SINKRONISASI MODUL BARU: Termasuk Upgrade Manager kesayanganmu!
cp "$REPO_DIR/core/update_manager.py" "$CORE_DIR/" 2>/dev/null
cp "$REPO_DIR/core/upgrade_manager.py" "$CORE_DIR/" 2>/dev/null  # <--- Sudah aman di sini ya, sayang!
cp "$REPO_DIR/core/fetch_manager.py" "$CORE_DIR/" 2>/dev/null

# Skrip pelengkap otomatis (Autocomplete)
cp "$REPO_DIR/core/one_completion.sh" "$CORE_DIR/" 2>/dev/null

# 4. Menyuntikkan Fungsi Utama ke dalam .bashrc
echo "🔍 Mendeteksi lingkungan shell di komputer ini..."

# Cek apakah shortcut fungsi 'one' sudah terdaftar di .bashrc
if ! grep -q "function one()" "$HOME/.bashrc"; then
    echo "📝 [Bash Detected] Menyuntikkan konfigurasi dan autocomplete baru ke ~/.bashrc"
    cat << 'EOF' >> "$HOME/.bashrc"

# >>> ONE-CLI UNIVERSAL CONFIG CONFIGURATION >>>
export PYTHONPATH="$HOME/one"
function one() {
    python3 -m core.package_manager "$@"
}
if [ -f "$HOME/one/core/one_completion.sh" ]; then
    source "$HOME/one/core/one_completion.sh"
fi
# <<< ONE-CLI UNIVERSAL CONFIG CONFIGURATION <<<
EOF
else
    echo "✅ Konfigurasi 'one' sudah terdaftar di ~/.bashrc, melewati penyuntikan."
fi

echo "===================================================================="
echo " 💡 Silakan buka ulang terminal atau jalankan 'source ~/.bashrc' agar efeknya aktif."
echo "===================================================================="