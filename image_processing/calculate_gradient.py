import argparse
from pathlib import Path
import numpy as np
import cv2

# 3×3 Sobel kernels
_SX = np.array([[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]], dtype=np.float32)
_SY = np.array([[ 1,  2,  1],
                [ 0,  0,  0],
                [-1, -2, -1]], dtype=np.float32)

# compute gradient magnitude and angle using Sobel operator
def calculate_gradient(img: np.ndarray): # img is grayscale, uint8
    x = img.astype(np.float32)
    # compute gradients
    gx = cv2.filter2D(x, ddepth=cv2.CV_32F, kernel=_SX, borderType=cv2.BORDER_REFLECT)
    gy = cv2.filter2D(x, ddepth=cv2.CV_32F, kernel=_SY, borderType=cv2.BORDER_REFLECT)

    mag = cv2.magnitude(gx, gy)  # float32
    ang = cv2.phase(gx, gy, angleInDegrees=True)  # [0, 360)
    # fold to [0,180): direction is unsigned
    ang_deg = np.minimum(ang, 360.0 - ang)

    return mag, ang_deg

def main():
    # parse command line arguments
    ap = argparse.ArgumentParser(description="Sobel gradient magnitude + angle")
    ap.add_argument("--input", required=True, help="path to grayscale image")
    ap.add_argument("--out-mag", required=True, help="where to save 8-bit magnitude image")
    ap.add_argument("--out-angle", help="optional: save angle visualization (0..180° → 0..255)")
    args = ap.parse_args()

    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE) # uint8
    if img is None:
        raise SystemExit(f"Could not read image: {args.input}")

    # compute gradient
    mag, ang_deg = calculate_gradient(img) # float32

    # save magnitude (scaled to 8-bit)
    mag8 = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    Path(args.out-mag).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(args.out_mag, mag8)
    print(f"Saved magnitude: {args.out_mag}")

    # optional: save angle visualization
    if args.out_angle:
        ang8 = (ang_deg * (255.0 / 180.0)).clip(0, 255).astype(np.uint8)
        Path(args.out_mag).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(args.out_angle, ang8)
        print(f"Saved angle viz: {args.out_angle}")

if __name__ == "__main__":
    main()
