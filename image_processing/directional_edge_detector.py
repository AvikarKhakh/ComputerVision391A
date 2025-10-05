import argparse
from pathlib import Path
import numpy as np
import cv2
import sys

# allow: from calculate_gradient import calculate_gradient
sys.path.append(str(Path(__file__).parent))
from calculate_gradient import calculate_gradient   # returns (mag, ang_deg)

def directional_edge_detector(img: np.ndarray, direction_range: tuple[float, float], mag_threshold: float = 0.0) -> np.ndarray:
    mag, ang_deg = calculate_gradient(img)  # mag is float32, ang in degrees [0,180)
    mag8 = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    lo, hi = direction_range
    # angle mask
    ang_mask = (ang_deg >= lo) & (ang_deg <= hi)
    # optional magnitude gating
    if mag_threshold > 0:
        mag_mask = mag8 >= mag_threshold
        mask = ang_mask & mag_mask
    else:
        mask = ang_mask

    out = np.where(mask, 255, 0).astype(np.uint8)
    return out

def main():
    # parse command line arguments
    ap = argparse.ArgumentParser(description="Directional edge detector (by Sobel angle)")
    ap.add_argument("--input", required=True, help="path to grayscale image")
    ap.add_argument("--output", required=True, help="where to save the binary directional map")
    ap.add_argument("--min-deg", type=float, required=True, help="min angle (degrees, 0..180)")
    ap.add_argument("--max-deg", type=float, required=True, help="max angle (degrees, 0..180)")
    ap.add_argument("--magth", type=float, default=0.0,
                    help="optional magnitude threshold on normalized mag [0..255] (default: 0 — disabled)")
    args = ap.parse_args()

    # validate angle range
    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise SystemExit(f"Could not read image: {args.input}")

    out = directional_edge_detector(img, (args.min_deg, args.max_deg), args.magth)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.output, out)
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
