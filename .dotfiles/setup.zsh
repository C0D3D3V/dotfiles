#!/usr/bin/env zsh
cd "$HOME" || exit

cfg_dir="$HOME/.cfg"

function cfg {
  /usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME $@
}

if [ -d "$cfg_dir" ] && [ "$(ls -A "$cfg_dir" 2>/dev/null | wc -l)" -gt 0 ]; then
  echo "Dotfiles are already installed. Instead, they are updated with the following command: \`cfg pull\`" >&2
  cfg pull
else
  git clone --recursive --jobs 8 --bare https://github.com/C0D3D3V/dotfiles.git "$cfg_dir"


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
  cfg config include.path "~/.dotfiles/dotfiles-git-config"
fi

if [ -d "$HOME/.vim_runtime" ] && [ "$(ls -A "$HOME/.vim_runtime" 2>/dev/null | wc -l)" -gt 0 ]; then
  echo "Vim configuration is already installed. Instead, it is now updated with the following command \`git -C  ~/.vim_runtime pull\`" >&2
  git -C  ~/.vim_runtime pull
else
  git clone --depth=1 https://github.com/amix/vimrc.git ~/.vim_runtime
  sh ~/.vim_runtime/install_awesome_vimrc.sh
fi