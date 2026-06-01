_one_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Pilihan perintah utama dari one-cli kamu
    opts="search install list remove system extract help"

    # Tab tingkat pertama (setelah kata 'one')
    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    # Tab tingkat kedua (setelah argumen atau perintah utama)
    if [ $COMP_CWORD -eq 2 ]; then
        case "${prev}" in
            search)
                COMPREPLY=( $(compgen -W "-f" -- ${cur}) )
                return 0
                ;;
            install)
                COMPREPLY=( $(compgen -W "-l" -- ${cur}) )
                return 0
                ;;
            remove)
                COMPREPLY=( $(compgen -W "-d" -- ${cur}) )
                return 0
                ;;
            *)
                ;;
        esac
    fi

    # TAB TINGKAT KETIGA: Fitur sakti baru khusus setelah argumen pilihan, sayang!
    if [ $COMP_CWORD -eq 3 ]; then
        local grand_prev="${COMP_WORDS[COMP_CWORD-2]}"
        
        # Jika perintahnya 'one remove -d', biarkan Bash menyarankan file/folder lokal
        if [ "${grand_prev}" = "remove" ] && [ "${prev}" = "-d" ]; then
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
        fi
    fi
}

complete -F _one_completion one