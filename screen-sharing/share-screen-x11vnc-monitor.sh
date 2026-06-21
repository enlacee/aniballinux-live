#!/bin/bash

x11vnc -clip 1920x1080+1600+0 \
-viewonly \
-cursor most \
-pointer_mode 1 \
-nocursorshape \
-noxfixes \
-scale_cursor 3
