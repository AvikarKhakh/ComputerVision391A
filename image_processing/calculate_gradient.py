import argparse
from pathlib import Path
import numpy as np
import cv2

# 3×3 Sobel kernels (Sx, Sy)
_SX = np.array([[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]], dtype=np.float32)
_SY = np.array([[ 1,  2,  1],
                [ 0,  0,  0],
                [-1, -2, -1]], dtype=np.float32)

def calculate_gradient(img: np.ndarray):
    # img: grayscale image, uint8 or float32
    x = img.astype(np.float32)
    gx = cv2.filter2D(x, ddepth=cv2.CV_32F, kernel=_SX, borderType=cv2.BORDER_REFLECT)
    gy = cv2.filter2D(x, ddepth=cv2.CV_32F, kernel=_SY, borderType=cv2.BORDER_REFLECT)
    mag = np.sqrt(gx * gx + gy * gy).astype(np.float32)
    return mag  # float32, NOT scaled

def main():
    # example usage:
    ap = argparse.ArgumentParser(description="Compute gradient magnitude using Sobel")
    ap.add_argument("--input", required=True, help="path to grayscale image")
    ap.add_argument("--output", required=True, help="where to save 8-bit magnitude image")
    args = ap.parse_args()

    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"Could not read image: {args.input}")

    mag = calculate_gradient(img)

    # scale to 8-bit for saving (0–255)
    mag8 = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.output, mag8)
    print(f"Saved gradient magnitude: {args.output}")

if __name__ == "__main__":
    main()
