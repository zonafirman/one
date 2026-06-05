_one_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="search info install list remove system extract update fetch upgrade help doctor clean speedtest ping ports backup restore docker logs"

    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    if [ $COMP_CWORD -eq 2 ]; then
        case "${prev}" in
            search) COMPREPLY=( $(compgen -W "-f" -- ${cur}) ) ; return 0 ;;
            install) COMPREPLY=( $(compgen -W "-l" -- ${cur}) ) ; return 0 ;;
            remove) COMPREPLY=( $(compgen -W "-d" -- ${cur}) ) ; return 0 ;;
            clean) COMPREPLY=( $(compgen -W "--all" -- ${cur}) ) ; return 0 ;;
            restore) COMPREPLY=( $(compgen -f -- ${cur}) ) ; return 0 ;;
            *) ;;
        esac
    fi
}
complete -F _one_completion one