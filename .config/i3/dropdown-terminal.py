#!/usr/bin/env python

# This script starts a terminal and, mobes it to the top of the workspace with a width of 90%
# and remembers the height as percentage
# Works with multiple outputs with different resolution or scaling

from i3ipc import Connection

title = 'terminal-dropdown'
conn = Connection()

# check if dropdown terminal exists and toggle scratchpad, set height and width
terms = conn.get_tree().find_named(f'^{title}$')
for term in terms:
    term.command('scratchpad show')
    exit(0)

# open dropdown terminal, positioning etc is done in sway config
conn.command(f'exec --no-startup-id "kitty --title {title}"')
