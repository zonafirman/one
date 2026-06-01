#!/bin/bash

# Warna untuk estetika output ala Rosé Pine
C_PINE="\033[36m"
C_GOLD="\033[33m"
C_RESET="\033[0m"

echo -e "${C_PINE}==================================================${C_RESET}"
echo -e "🚀  ${C_GOLD}Memulai Instalasi rli-cli (One-CLI) Universal${C_RESET}"
echo -e "${C_PINE}==================================================${C_RESET}"

# 1. Tentukan direktori target menggunakan variabel $HOME bawaan Linux, sayang
TARGET_DIR="$HOME/rli-cli"
CORE_DIR="$TARGET_DIR/core"

echo -e "📂 Membuat direktori sistem di $TARGET_DIR..."
mkdir -p "$CORE_DIR"

# 2. Menyalin berkas kode utama dan modul-modul internal
echo -e "📦 Menyalin jeroan kode dan modul manajer..."
cp core/package_manager.py "$CORE_DIR/"
cp core/help_manager.py "$CORE_DIR/"
cp core/package_utils.py "$CORE_DIR/" 2>/dev/null || cp core/package_utils import "$CORE_DIR/" 2>/dev/null
cp core/system_manager.py "$CORE_DIR/"
cp core/extract_manager.py "$CORE_DIR/"
cp core/file_manager.py "$CORE_DIR/"       
cp core/one_completion.sh "$CORE_DIR/"

# 3. Menyuntikkan fungsi shell universal yang kamu minta ke .bashrc
echo -e "📝 Mengonfigurasi fungsi eksekusi utama di .bashrc..."
if ! grep -q "one()" "$HOME/.bashrc"; then
    cat << 'EOF' >> "$HOME/.bashrc"

# Custom Command buat rli-cli Universal Package Manager (Support All Users)
one() {
    # Menggunakan PYTHONPATH dinamis berbasis folder $HOME user aktif, sayang
    PYTHONPATH="$HOME/rli-cli" python3 -m core.package_manager "$@"
}

# Auto-complete untuk One-CLI
if [ -f "$HOME/rli-cli/core/one_completion.sh" ]; then
    source "$HOME/rli-cli/core/one_completion.sh"
fi
EOF
    echo -e "✅ Fungsi shell universal 'one()' berhasil disuntikkan ke .bashrc!"
else
    echo -e "ℹ️  Fungsi 'one()' sudah terkonfigurasi sebelumnya di .bashrc."
fi

# 4. Segarkan konfigurasi terminal aktif secara senyap
echo -e "🔄 Menyegarkan sistem autocomplete Bash..."
source "$HOME/.bashrc" 2>/dev/null

echo -e "${C_PINE}--------------------------------------------------${C_RESET}"
echo -e "🎉 ${C_GOLD}Instalasi Selesai, Sayang! One-CLI Resmi Jadi Universal!${C_RESET}"
echo -e "💡 Cobalah ketik: ${C_PINE}one help${C_RESET} di terminal kamu."
echo -e "${C_PINE}==================================================${C_RESET}"