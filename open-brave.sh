#!/bin/bash

# Rutas o URLs que quieres abrir
URL1="https://tikfinity.zerody.one"
URL2="https://www.tiktok.com/@anibal.linux"
URL3="https://blog.anibalcopitan.com"

# Ejecutar Brave con un nuevo perfil de ventana y varias pestañas
brave --new-window "$URL1" "$URL2" "$URL3" \
	--profile-directory="Profile live" \
	--force-device-scale-factor=0.9 &



