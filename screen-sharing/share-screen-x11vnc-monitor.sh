#!/bin/bash

# geometria real del monitor externo (el que no es primary), ej: 1280x1024+1600+0
GEOMETRY=$(xrandr | grep ' connected' | grep -v primary | grep -oE '[0-9]+x[0-9]+\+[0-9]+\+[0-9]+' | head -1)

if [ -z "$GEOMETRY" ]; then
    echo "No se encontro un monitor externo conectado" >&2
    exit 1
fi

echo "Compartiendo monitor: $GEOMETRY"

x11vnc -clip "$GEOMETRY" \
-viewonly \
-cursor most \
-pointer_mode 1 \
-nocursorshape
