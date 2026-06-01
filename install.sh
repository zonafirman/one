#!/bin/bash

# Warna untuk estetika output ala Rosé Pine
C_PINE="\033[36m"
C_GOLD="\033[33m"
C_RESET="\033[0m"

echo -e "${C_PINE}==================================================${C_RESET}"
echo -e "🚀  ${C_GOLD}Memulai Instalasi One-CLI Multi-Shell Universal${C_RESET}"
echo -e "${C_PINE}==================================================${C_RESET}"

# 1. Tentukan direktori target menggunakan folder $HOME user aktif
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

echo -e "🔍 Mendeteksi lingkungan shell di komputer ini..."

# Logika fungsi utama yang akan disuntikkan (untuk Bash & Zsh)
BASH_ZSH_FUNCTION=$(cat << 'EOF'

# Custom Command buat rli-cli Universal Package Manager
one() {
    PYTHONPATH="$HOME/rli-cli" python3 -m core.package_manager "$@"
}

# Auto-complete untuk One-CLI
if [ -f "$HOME/rli-cli/core/one_completion.sh" ]; then
    source "$HOME/rli-cli/core/one_completion.sh"
fi
EOF
)

# 3. PROSES SUNTIK OTOMATIS BERDASARKAN SHELL YANG AKTIF, SAYANG

# KONDISI A: Konfigurasi untuk BASH (Termasuk penanganan khusus KDE Plasma Profile)
if [ -f "$HOME/.bashrc" ]; then
    if ! grep -q "one()" "$HOME/.bashrc"; then
        echo "$BASH_ZSH_FUNCTION" >> "$HOME/.bashrc"
        echo -e "✅ Fungsi 'one()' berhasil dipasang di ~/.bashrc"
    fi
    
    # TRICK KHUSUS KDE PLASMA: Pastikan Konsole membaca .bashrc via .bash_profile
    if [ -f "$HOME/.bash_profile" ]; then
        if ! grep -q "bashrc" "$HOME/.bash_profile"; then
            echo -e "\nif [ -f ~/.bashrc ]; then\n    source ~/.bashrc\nfi" >> "$HOME/.bash_profile"
            echo -e "📦 [KDE Plasma Detected] Menghubungkan .bash_profile ke .bashrc"
        fi
    else
        echo -e "\nif [ -f ~/.bashrc ]; then\n    source ~/.bashrc\nfi" >> "$HOME/.bash_profile"
        echo -e "📦 [KDE Plasma Detected] Membuat file ~/.bash_profile baru"
    fi
fi

# KONDISI B: Jika temanmu ternyata pakai ZSH
if [ -f "$HOME/.zshrc" ]; then
    if ! grep -q "one()" "$HOME/.zshrc"; then
        echo "$BASH_ZSH_FUNCTION" >> "$HOME/.zshrc"
        echo -e "✅ Fungsi 'one()' berhasil dipasang di ~/.zshrc (Zsh Detected!)"
    fi
fi

# KONDISI C: Jika di masa depan ada yang pakai FISH SHELL
if [ -d "$HOME/.config/fish" ] || command -v fish &> /dev/null; then
    mkdir -p "$HOME/.config/fish/functions"
    cat << 'EOF' > "$HOME/.config/fish/functions/one.fish"
function one
    set -x PYTHONPATH $HOME/rli-cli
    python3 -m core.package_manager $argv
end
EOF
    echo -e "✅ Fungsi 'one()' berhasil dipasang di fungsi kustom Fish Shell!"
fi

echo -e "${C_PINE}--------------------------------------------------${Ins_RESET}"
echo -e "🎉 ${C_GOLD}Instalasi Selesai, Sayang! Proyekmu Kini 100% Universal!${C_RESET}"
echo -e "💡 Minta temanmu untuk MEMBUKA ULANG terminalnya agar efeknya aktif."
echo -e "${C_PINE}==================================================${C_RESET}"