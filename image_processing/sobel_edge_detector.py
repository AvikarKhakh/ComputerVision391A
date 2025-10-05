import argparse
from pathlib import Path
import numpy as np
import cv2
import sys

# allow `from calculate_gradient import calculate_gradient`
sys.path.append(str(Path(__file__).parent))
from calculate_gradient import calculate_gradient  # returns (mag, ang_deg)

def sobel_edge_detector(img: np.ndarray, threshold: float) -> np.ndarray:
    # img is grayscale, uint8
    mag, _ = calculate_gradient(img)  # float32
    mag8 = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    edges = (mag8 >= threshold).astype(np.uint8) * 255
    return edges # binary edge map, uint8

def main():
    # parse command line arguments
    ap = argparse.ArgumentParser(description="Sobel edge detector (binary threshold on magnitude)")
    ap.add_argument("--input", required=True, help="path to grayscale image")
    ap.add_argument("--output", required=True, help="where to save the binary edge map (PNG/JPG)")
    ap.add_argument("--threshold", type=float, default=60.0,
                    help="threshold on normalized magnitude [0..255] (default: 60)")
    args = ap.parse_args()

    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"Could not read image: {args.input}")

    # process
    out = sobel_edge_detector(img, args.threshold)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.output, out)
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
