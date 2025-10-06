# ComputerVision391A — Image Processing Assignment
Computer Science Selected Topics - Computer Vision

## Overview
This assignment implements and analyzes three classic image processing tasks on a low-contrast X-ray image:

1) Intensity transformations  
2) Non-linear denoising and gradients  
3) Simple Sobel-based edge detection (compared with Canny).

---

## Exercise 1: Intensity Transformations & Histogram Equalization

### Description
Enhanced a low-contrast X-ray using two global methods:

## Key Concepts
* **Contrast Stretch**: linearly spreads pixel values from `[r_min, r_max]` to `[0, 255]` (used percentiles: `r_min = p2 = 5`, `r_max = p98 = 233`).
* **Histogram Equalization**: redistributes brightness using the CDF to use more of the available range.

* Linear remap: `y = clip( (x - r_min) * 255 / (r_max - r_min), 0, 255 )`  
* Histogram counts and normalized distribution (256 bins)  
* Equalization LUT from cumulative distribution

### Analysis
Stretching widened the brightness range and made bones/edges clearer with little extra noise. Equalization brightened dark areas more but also added grain. For this X-ray, contrast stretch looked the most natural; equalization was stronger but noisier.

## Reflection
I learned how much the choice of `r_min`/`r_max`, especially using percentages, changes the final look of the image. Reading the histogram made it easier to explain why stretch versus equalize behaves very differently. Overall, I saw that equalization can help boost contrast but also it can iincrease noise if not careful.

### Exercise 1 Results
<img width="6129" height="2534" alt="image" src="https://github.com/user-attachments/assets/2635d980-7625-4699-aeda-69786423d3e3" />
<img width="1800" height="600" alt="image" src="https://github.com/user-attachments/assets/f51356cb-1f48-41b7-a782-b6574ab50c50" />

---

## Exercise 2: Non-Linear Filtering & Gradient Magnitude

### Description
Added 5% salt-and-pepper noise, removed it with a 3×3 median filter, and computed the Sobel gradient magnitude before and after.

### Key Concepts
* **Median filter**: replaces each pixel with the median in an odd-sized window (reflect padding).
* **Sobel gradients**: `gx = Sx * img`, `gy = Sy * img`, magnitude `sqrt(gx^2 + gy^2)`.

### Analysis
* Mean **−84.5%**, 90th **−93.6%**, 99th **−82.6%** after median filtering; the max stayed similar.  
* Interpretation: the median filter suppresses impulse-noise edges while keeping strong boundaries, producing a much cleaner gradient map.

## Reflection 
During this exercise I saw firsthand that median filtering is the correct tool for salt-and-pepper noise because it removes spikes without blurring the real edges too much. Checking the simple stats (mean/p90/p99) through the CLI helped me justify the visual improvement in the images. I also learned that denoising before computing gradients gives much cleaner edge evidence in the image as well.

### Exercise 2 Results
<img width="1400" height="434" alt="image" src="https://github.com/user-attachments/assets/289b10eb-0847-4ee2-8216-1a46903aef75" />

---

## Exercise 3: Simple Sobel-Based Edge Detector

### Description
Built a small edge-detection pipeline and compared three outputs on the median-filtered image:

1. **Sobel + Threshold** on normalized magnitude (picked `threshold = 30` by trial and error).  
2. **Directional Edges**: keep edges angled roughly 45° (40–50°) and ignore weak edges (`magth = 20`).  
3. **Canny** (`low/high = 50/150`, `L2gradient=True`) for thin, continuous contours via non-max suppression + hysteresis.

### Key Concepts
* `calculate_gradient(img)` returns magnitude and angle (degrees) folded to `[0, 180)`.  
* Orientation-selective maps (helps isolate rib-like structures like in this image).  
* Canny usually gives the most continuous outlines when preceded by denoising.

### Analysis
* **Sobel (threshold = 30)**: clean edges; sensitive to threshold choice.  
* **Directional (40–50 degrees)**: intentionally sparse; highlights oblique structures near ~45°.  
* **Canny (50/150)**: most continuous and visually clear edges here, thanks to non-maximum suppression + hysteresis; benefits from the median prefilter.

## Reflection 
In this exercise, tuning the Sobel threshold showed me how very sensitive simple edge maps can be. The directional filter was useful to pull out edges at approximately a 45° on purpose, while Canny gave the thinnest, most connected contours on the image. Prefiltering with the median clearly helped all three edge results in the final image.

### Exercise 3 – Results
<img width="3600" height="1504" alt="image" src="https://github.com/user-attachments/assets/ab9311f1-a2f7-4a6e-84a2-f0fa034ca4ae" />

## Conclusion
Across these exercises I learned how contrast adjustment, denoising, and edge extraction fit together in a small pipeline of working with an image. Parameter choices (percentiles, window size, thresholds) make a big difference in your results, and simple metrics/plots help support/backup those choices. Overall, I saw that the steps you do before edge detection matter a lot. Better preprocessing gave cleaner edges and visuals in the image and those were much easier to understand.