#!/bin/bash

#x11vnc -clip 960x1080+1440+0 -cursor most -pointer_mode 1 -nocursorshape -noxfixes -scale_cursor 3

x11vnc \
-clip 960x1080+1600+0 \
-viewonly \
-cursor arrow \
-overlay \
-pointer_mode 1 \
-nocursorshape \
-noxfixes \
-scale_cursor 2
