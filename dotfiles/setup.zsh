#!/usr/bin/env zsh
cd "$HOME" || exit

cfg_dir="$HOME/.cfg"
if [ -d "$cfg_dir" ] && [ "$(ls -A "$cfg_dir" 2>/dev/null | wc -l)" -gt 0 ]; then
  echo "dotfiles are already installed, use \`cfg pull\` to update" >&2
  exit 1
fi

git clone --recursive --jobs 8 --bare https://github.com/C0D3D3V/dotfiles.git "$cfg_dir"

function cfg {
   /usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME $@
}

# backup
BACKUP_DIR=".dotfiles-backup"
mkdir -p "$BACKUP_DIR"
if cfg checkout &>/dev/null; then
  echo "Checked out dotfiles."
else
  cfg checkout 2>&1 | awk -F '\t' '/\t/ {print $2}' >"$BACKUP_DIR/BACKUP_FILE_LIST"
  echo "Backing up $(wc -l <$BACKUP_DIR/BACKUP_FILE_LIST) pre-existing dot files."
  xargs -I{} dirname $BACKUP_DIR/{} <"$BACKUP_DIR/BACKUP_FILE_LIST" | xargs -I{} mkdir -p {}
  xargs -I{} mv {} $BACKUP_DIR/{} <"$BACKUP_DIR/BACKUP_FILE_LIST"
fi

cfg checkout
cfg config status.showUntrackedFiles no
cfg submodule update --init --recursive --jobs 8
