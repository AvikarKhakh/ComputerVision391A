#!/usr/bin/env python3
# Exercise 1: Affine Transformation

from pathlib import Path
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Paths
IMAGES_DIR = Path(__file__).parent / "images"
ORIG_PATH  = IMAGES_DIR / "original_image.jpg"
TARG_PATH  = IMAGES_DIR / "transformed_image.jpg"

def read_bgr(path: Path):
    img = cv.imread(str(path), cv.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not read: {path}")
    return img

def bgr_to_rgb(img_bgr):
    return cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)

def apply_affine(orig_bgr, src_pts, dst_pts):
    # Build affine transform from 3 pts
    M = cv.getAffineTransform(src_pts.astype(np.float32),
                              dst_pts.astype(np.float32))
    h, w = orig_bgr.shape[:2]
    warped = cv.warpAffine(orig_bgr, M, (w, h),
                           flags=cv.INTER_LINEAR,
                           borderMode=cv.BORDER_CONSTANT)  # Change to BORDER_CONSTANT
    return warped, M

def main():
    # Load images
    orig_bgr = read_bgr(ORIG_PATH)
    targ_bgr = read_bgr(TARG_PATH)

    # Hard-coded pts: order TL, TR, BL
    src_pts = np.float32([
        [0, 0],    # TL original
        [1200, 0],   # TR original
        [491, 491]    # BL original
    ])
    dst_pts = np.float32([
        [303, 61],  # TL target
        [890, 474],  # TR target
        [733, 723]   # BL target
    ])

    affine_bgr, M = apply_affine(orig_bgr, src_pts, dst_pts)
    print("Affine matrix:\n", M)

    # Convert for display
    orig_rgb   = bgr_to_rgb(orig_bgr)
    targ_rgb   = bgr_to_rgb(targ_bgr)
    affine_rgb = bgr_to_rgb(affine_bgr)

    # Show results
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(orig_rgb);   axes[0].set_title("Original"); axes[0].axis("off")
    axes[1].imshow(targ_rgb);   axes[1].set_title("Target");   axes[1].axis("off")
    axes[2].imshow(affine_rgb); axes[2].set_title("Affine");   axes[2].axis("off")
    plt.tight_layout(); plt.show()

if __name__ == "__main__":
    main()
