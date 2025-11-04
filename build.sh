#!/bin/bash

echo "===================================="
echo "Building macOS/Linux Executable"
echo "===================================="
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

echo "Building executable..."
pyinstaller build.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "===================================="
    echo "Build completed successfully!"
    echo "===================================="
    echo ""
    echo "Executable location: dist/VideoSorterYouTubeUploader"
    echo ""
else
    echo ""
    echo "Build failed!"
    exit 1
fi
