# Citra Digital - Mini Image Editor

A desktop image processing application built with Python. Implements common digital image processing algorithms from scratch using pixel-level operations.

## Features

### Adjustments
- **Image Negative** — Invert pixel values
- **Brightness** — Adjust brightness with slider (-255 to 255)
- **Power Law (Gamma)** — Gamma correction (0.1 to 5.0)
- **Log Transform** — Logarithmic intensity mapping

### Transform
- **Rotate** — Clockwise / Counter-clockwise rotation
- **Flip** — Horizontal / Vertical flip
- **Scale** — Resize by scale factor (0.1x to 4.0x)
- **Resample** — Resize to specific width × height

### Blending
- **Image Blending** — Alpha blend two images together

### Filtering
- **Median Filter** — Noise reduction (3×3, 5×5, 7×7 kernel)
- **Mean Filter** — Averaging filter
- **Gaussian Filter** — Weighted blur with Gaussian kernel

### Edge Detection
- **Sobel** — Gradient-based edge detection
- **Prewitt** — Uniform gradient edge detection
- **Robert Cross** — Diagonal gradient edge detection
- **Compass** — Directional edge detection (N, NE, E, SE, S, SW, W, NW, ALL)

## Tech Stack

- **Python 3**
- **Pillow (PIL)** — Image I/O and color space conversion
- **FreeSimpleGUI** — Desktop GUI framework

## Getting Started

```bash
python -m venv venv
source venv/bin/activate
pip install Pillow FreeSimpleGUI
python img_viewer.py
```

## Project Structure

```
├── img_viewer.py        # GUI application
├── processing_list.py   # Image processing algorithms
└── README.md
```
