import argparse
from pathlib import Path
import numpy as np
import cv2

def equalize_histogram(img: np.ndarray) -> np.ndarray:
    if img.dtype != np.uint8: # convert to uint8 if needed
        x = img.astype(np.uint8)
    else:
        x = img

    hist, _ = np.histogram(x.ravel(), bins=256, range=(0, 256))
    cdf = hist.cumsum().astype(np.float64)
    # mask zeros to avoid flat regions dividing by 0
    cdf_min = cdf[cdf > 0].min() if np.any(cdf > 0) else 0.0
    cdf_norm = (cdf - cdf_min) / (cdf[-1] - cdf_min) if cdf[-1] > cdf_min else np.zeros_like(cdf)
    lut = np.clip(np.round(255 * cdf_norm), 0, 255).astype(np.uint8)

    return lut[x]

def main():
    # parse command line arguments
    ap = argparse.ArgumentParser(description="Histogram equalization (grayscale)")
    ap.add_argument("--input", required=True, help="path to grayscale image")
    ap.add_argument("--output", required=True, help="where to save the equalized image")
    args = ap.parse_args()

    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE) # uint8
    if img is None:
        raise SystemExit(f"Could not read image: {args.input}") # error

    # process
    out = equalize_histogram(img)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.output, out)
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
