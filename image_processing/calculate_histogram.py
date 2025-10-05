import argparse
from pathlib import Path
import numpy as np
import cv2

def calculate_histogram(img: np.ndarray, bins: int = 256):
    if bins <= 0:
        raise ValueError("bins must be positive")
    # Use [0,256) so that intensity 255 is included in the last bin.
    counts, _ = np.histogram(img.ravel(), bins=bins, range=(0, 256))
    counts = counts.astype(np.int64)
    total = counts.sum()
    dist = counts / total if total > 0 else np.zeros_like(counts, dtype=np.float64)
    return counts, dist

def main():
    ap = argparse.ArgumentParser(description="Calculate grayscale histogram")
    ap.add_argument("--input", required=True, help="path to grayscale image")
    ap.add_argument("--bins", type=int, default=256, help="number of bins (default: 256)")
    ap.add_argument("--save", help="optional: path to save counts as .npy")
    args = ap.parse_args()

    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"Could not read image: {args.input}")

    counts, dist = calculate_histogram(img, args.bins)

    # Print a tiny summary
    print(f"bins={args.bins}, total_pixels={counts.sum()}, min_count={counts.min()}, max_count={counts.max()}")

    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        np.save(args.save, counts)
        print(f"Saved counts to {args.save}.npy")

if __name__ == "__main__":
    main()
