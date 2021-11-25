#!/bin/bash

echo "What File do you wish to use as a background?"

read wallpaperfile

echo "What Backend do you want wal to use?
   Backends:
 - colorthief
 - haishoku
 - colorz
 - wal
"

read backend

wal -i $wallpaperfile --backend $backend

plasma-theme -c ~/.local/share/color-schemes/pywal-kde.colors

echo "Please Restart Konsole to see changes apply there and change file manager icons accordingly"
