#!/usr/bin/env zsh
cd "$HOME" || exit

if command -v wpg-install.sh >/dev/null; then
  echo "Installing wpgtk themes and icons"
  wpg-install.sh -gi
else
  echo "ERROR: command wpg-install.sh not found"
  echo "Please install wpgtk and run the command wpg-install -gi"
fi

# Some wallpapers: https://wallpaperaccess.com/minimalism-4k
# To build your own theme also see:
# https://github.com/deviantfero/wpgtk-colorschemes
# https://github.com/deviantfero/wpgtk-templates
# https://github.com/deviantfero/wpgtk/wiki/Templates

download_wallpaper() {
  local url="$1"
  local wallpaper="$2"

  local wallpaper_path="$HOME/.config/wallpapers"
  mkdir -p "$wallpaper_path"

  echo "Downloading wallpaper to $wallpaper_path/$wallpaper"
  curl -L "$url" --output "$wallpaper_path/$wallpaper"

  if command -v wpg >/dev/null; then
    echo "Add wallpaper to wpg"
    wpg -a "$wallpaper_path/$wallpaper"
  else
    echo "Run wpg to generate the config from the template files"
  fi
}

download_wallpaper https://wallpaperaccess.com/full/2109997.jpg pyramid.jpg
download_wallpaper https://wallpaperaccess.com/full/10750888.jpg period.jpg
download_wallpaper https://wallpaperaccess.com/full/3205251.jpg space.jpg
download_wallpaper https://wallpaperaccess.com/full/1582719.jpg panda.jpg


 
if command -v wpg >/dev/null; then
  echo "Set wallpaper"
  wpg -s pyramid.jpg
fi

if command -v betterlockscreen >/dev/null; then
  echo "Set lockscreen wallpaper"
  betterlockscreen -u ~/.config/wallpapers/space.jpg
fi


echo "Run lxappearance to set the GTK and icon theme"
