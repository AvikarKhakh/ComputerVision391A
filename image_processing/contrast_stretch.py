import argparse
from pathlib import Path
import numpy as np
import cv2

def contrast_stretch(img: np.ndarray, r_min: float, r_max: float) -> np.ndarray:
    """Map intensities in [r_min, r_max] linearly to [0, 255]."""
    if r_min >= r_max:
        raise ValueError("r_min must be < r_max")
    x = img.astype(np.float32)
    y = (x - r_min) * (255.0 / (r_max - r_min))
    y = np.clip(y, 0, 255).astype(np.uint8)
    return y

def main():
    ap = argparse.ArgumentParser(description="Linear contrast stretch")
    ap.add_argument("--input", required=True, help="path to grayscale image")
    ap.add_argument("--output", required=True, help="where to save the result")
    ap.add_argument("--rmin", type=float, required=True, help="lower input intensity")
    ap.add_argument("--rmax", type=float, required=True, help="upper input intensity")
    args = ap.parse_args()

    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"Could not read image: {args.input}")

    out = contrast_stretch(img, args.rmin, args.rmax)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.output, out)
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
