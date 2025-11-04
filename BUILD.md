# Build Instructions

## Building from Source

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional)

### Setup

1. Clone or download the repository
```bash
git clone https://github.com/youpaki/video-sorter-youtube-uploader.git
cd video-sorter-youtube-uploader
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python main.py
```

## Creating Standalone Executable

### Windows

Run the build script:
```cmd
build.bat
```

The executable will be created in `dist/VideoSorterYouTubeUploader.exe`

### macOS / Linux

Run the build script:
```bash
chmod +x build.sh
./build.sh
```

The executable will be created in `dist/VideoSorterYouTubeUploader`

### Manual Build

If the scripts don't work, you can build manually:

```bash
pip install pyinstaller
pyinstaller build.spec
```

## Build Configuration

The build is configured in `build.spec`:
- Single-file executable (all dependencies bundled)
- No console window (GUI mode)
- Includes all required modules and dependencies
- Optimized with UPX compression

## Distribution

To distribute the application:

1. Create a ZIP archive of the executable
2. Include README.md and LICENSE
3. Test on a clean system without Python installed

## Troubleshooting

### "Module not found" errors during build
Reinstall all dependencies:
```bash
pip install --upgrade -r requirements.txt
```

### Build fails on Windows
Ensure Visual C++ Redistributable is installed

### Build fails on macOS
Install Xcode command line tools:
```bash
xcode-select --install
```

### Large executable size
This is normal. The executable includes:
- Python interpreter
- All dependencies (OpenCV, Selenium, etc.)
- Standard library modules

Expected size: 80-100 MB

## Testing the Build

After building, test the executable on a system without Python:

1. Copy the executable to a test machine
2. Verify Chrome is installed
3. Run the executable
4. Test all features (scan, analyze, upload)
