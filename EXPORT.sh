export NAME="$1"
export LANG="$2"

python3 create_tex.py "$1" "$2"

if [[ $? == 1 ]]; then
    echo "exit..."
    exit
fi
