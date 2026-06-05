#!/bin/bash
# ====================================================================
#  One-CLI Pro Edition - System Installer
# ====================================================================

REPO_DIR="$HOME/one"  
CORE_DIR="$REPO_DIR/core"

echo "[INFO] Starting One-CLI Pro installation..."

if [ ! -d "$CORE_DIR" ]; then
    mkdir -p "$CORE_DIR"
fi

echo "[INFO] Copying core modules..."
cp "$REPO_DIR"/core/*.py "$CORE_DIR/" 2>/dev/null
cp "$REPO_DIR/core/one_completion.sh" "$CORE_DIR/" 2>/dev/null

detect_and_inject() {
    local shell_rc=$1
    if [ -f "$shell_rc" ]; then
        if ! grep -q "function one()" "$shell_rc"; then
            echo "[INFO] Injecting configurations into $shell_rc"
            cat << 'EOF' >> "$shell_rc"

# >>> ONE-CLI PRO CONFIGURATION >>>
export PYTHONPATH="$HOME/one"
function one() {
    python3 -m core.package_manager "$@"
}
if [ -f "$HOME/one/core/one_completion.sh" ]; then
    source "$HOME/one/core/one_completion.sh"
fi
# <<< ONE-CLI PRO CONFIGURATION <<<
EOF
        else
            echo "[OK] Configuration already exists in $shell_rc."
        fi
    fi
}

detect_and_inject "$HOME/.bashrc"
detect_and_inject "$HOME/.zshrc"

echo "[SUCCESS] Installation complete. Run 'source ~/.bashrc' to apply."