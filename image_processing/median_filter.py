import argparse
from pathlib import Path
import numpy as np
import cv2

def median_filter(img: np.ndarray, size: int = 3) -> np.ndarray:
    if size < 1 or size % 2 == 0:
        raise ValueError("size must be an odd integer >= 1") # enforce odd size

    if img.ndim == 3: 
        # run per-channel, then merge back
        chans = cv2.split(img)
        filt = [median_filter(c, size) for c in chans]
        return cv2.merge(filt)

    # ensure uint8 input for simplicity
    x = img.astype(np.uint8) if img.dtype != np.uint8 else img
    k = size
    r = k // 2

    # pad the input image to handle borders
    padded = cv2.copyMakeBorder(x, r, r, r, r, borderType=cv2.BORDER_REFLECT)
    H, W = x.shape
    out = np.empty_like(x)

    # straightforward sliding-window implementation (clear & student-friendly)
    for y in range(H):
        for z in range(W):
            win = padded[y:y+k, z:z+k]
            out[y, z] = np.median(win)

    return out

def main():
    # example usage:
    ap = argparse.ArgumentParser(description="Median filter (non-linear)")
    ap.add_argument("--input", required=True, help="path to input image (will be read as grayscale)")
    ap.add_argument("--output", required=True, help="where to save the filtered image")
    ap.add_argument("--size", type=int, default=3, help="odd window size (default: 3)")
    args = ap.parse_args()

    # read image as grayscale
    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"Could not read image: {args.input}")

    # apply median filter
    out = median_filter(img, args.size)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.output, out)
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
