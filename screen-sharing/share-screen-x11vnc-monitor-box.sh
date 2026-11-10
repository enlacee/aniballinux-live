#!/bin/bash

# Comparte solo una "caja" (porcion) del monitor externo.
# Uso: ./share-screen-x11vnc-monitor-box.sh [ANCHO] [ALTO] [OFFSET_X] [OFFSET_Y]
#   por defecto: mitad izquierda del monitor, 960x1025 desde la esquina superior izquierda
BOX_W=${1:-960}
BOX_H=${2:-1025}
OFF_X=${3:-0}   # desplazamiento relativo al monitor externo
OFF_Y=${4:-0}

# geometria real del monitor externo (el que no es primary), ej: 1920x1080+1600+0
GEOMETRY=$(xrandr | grep ' connected' | grep -v primary | grep -oE '[0-9]+x[0-9]+\+[0-9]+\+[0-9]+' | head -1)

if [ -z "$GEOMETRY" ]; then
    echo "No se encontro un monitor externo conectado" >&2
    exit 1
fi

# separar WxH+X+Y
IFS='x+' read -r MON_W MON_H MON_X MON_Y <<< "$GEOMETRY"

# no salirse del monitor
[ $((OFF_X + BOX_W)) -gt "$MON_W" ] && BOX_W=$((MON_W - OFF_X))
[ $((OFF_Y + BOX_H)) -gt "$MON_H" ] && BOX_H=$((MON_H - OFF_Y))

CLIP="${BOX_W}x${BOX_H}+$((MON_X + OFF_X))+$((MON_Y + OFF_Y))"

echo "Monitor externo: $GEOMETRY"
echo "Compartiendo caja: $CLIP"

x11vnc -clip "$CLIP" \
-viewonly \
-cursor most \
-pointer_mode 1 \
-nocursorshape
