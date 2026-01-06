#!/bin/bash
export DISPLAY=":0.0"

PMUPDATES="$(checkupdates | wc -l)"
AURUPDATES="$(yay -Qua | wc -l)"
notify-send  -h string:bgcolor:#000000 -h string:fgcolor:#d8ff44 "Verfügbare Aktualisierungen:"  "Pacman: $PMUPDATES  AUR: $AURUPDATES" 

exit