# Aniballinux Stream Suite Makefile

.PHONY: help overlay stream brave install

help:
	@echo "Aniballinux Stream Suite"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  start      - Launch EVERYTHING (Overlay, Stream, Brave) at once"
	@echo "  overlay    - Start the mouse overlayer tool (auto-installs if needed)"
	@echo "  stream     - Start the screen sharing suite"
	@echo "  brave      - Launch the streaming environment"

start:
	@echo "Launching Aniballinux Stream Suite... 🚀"
	@$(MAKE) overlay &
	@$(MAKE) stream &
	@$(MAKE) brave &

overlay:
	@if [ ! -d "mouse-overlayer/venv" ]; then \
		echo "Creating virtual environment and installing dependencies..."; \
		cd mouse-overlayer && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt; \
	fi
	@echo "Starting Mouse Overlayer..."
	cd mouse-overlayer && ./venv/bin/python mouse_overlay.py

stream:
	@echo "Starting Screen Sharing..."
	cd screen-sharing && bash share-screen-x11vnc.sh

brave:
	@echo "Launching Brave Live Environment..."
	cd browser-automation && bash open-brave.sh
