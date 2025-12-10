#!/bin/bash
# Build script for Minesweeper GUI
# Assumes PyInstaller is installed

echo "Building Minesweeper Executable..."
pyinstaller --onefile --windowed --name minesweeper minesweeper_gui.py

echo "Build complete. Executable should be in dist/minesweeper"
