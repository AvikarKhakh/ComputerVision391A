# ComputerVision391A
Computer Science Selected Topics - Computer Vision Course

## Overview
This repository contains the implementation and analysis of various exercises from the Computer Vision course (CV391-A). Each exercise explores a fundamental concept in computer vision, including geometric transformations, lens aperture parameters, and noise/error analysis. The goal is to develop a deeper understanding of image processing and computer vision techniques through hands-on coding and experimentation.

---------------

## Exercise 1: Affine Transformation
### Description
In this exercise, I explored affine transformations, which are  mappings that keep points, straight lines, and planes. The transformation involves scaling, rotating, and translating an image based on three control points. I choose three points on the original 
image and found those exact points on the transformed image to try and replicate the transformation as accurately as possible.

### Key Concepts
- **Affine Transformation Matrix**: Computed using three pairs of corresponding points between the original and target images to try and replicate the transformation.
- **OpenCV Functions**: Used `cv.getAffineTransform` to calculate the transformation matrix and `cv.warpAffine` to apply the transformation to the image.

### Reflection
This exercise demonstrated the importance of understanding how geometric transformations work in image processing. By visualizing the transformation results, I gained insight into how specific points influence the output image. Debugging issues like overlapping borders in the new image I was trying to form helped me learn the importance of setting appropriate parameters within the code.

## Access Output
image_formation/images/exercise1_all_images.png

---------------

## Exercise 2: Lens Aperture Parameters
### Description
This exercise focused on simulating the effects of lens aperture parameters, such as focal length and f-number, on image formation. The goal was to understand how these parameters influence the depth of field and light exposure. 

### Key Concepts
- **Focal Length (f)**: Determines the magnification and field of view.
- **F-number (N)**: Controls the aperture size and depth of field.
- **Simulation**: Used mathematical models to simulate the effects of changing these parameters.

### Reflection
This exercise gave me insight into the physics behind camera optics and how they can impact image quality. 
I found it interesting to see how small changes in aperture size could significantly affect the sharpness of objects at 
different distances. This knowledge is crucial for designing camera systems and understanding real-world photography. 
In the output plots, I show the different ideal aperture diamter measurements for the respective focal lengths through 
marking black dots on the liens. 

## Access Output
image_formation/images/exercise2_plots.png

---------------

## Exercise 3: Sampling and Quantization
### Description
In this exercise, I explored the concepts of sampling and quantization, which are fundamental to converting continuous signals 
into digital images. I analyzed how sampling frequency and bit depth can affect the quality of the reconstructed signal.

### Key Concepts
- **Sampling Frequency**: Determines how often the signal is sampled over time.
- **Quantization**: Maps continuous frequency values to discrete levels based on the number of bits.

### Reflection
This exercise gave me a better understanding of the trade-offs between resolution, storage, and quality in digital imaging. 
It was  interesting to observe how insufficient sampling frequency could lead to aliasing, making the importance of the 
Nyquist-Shannon theorem clear. I included two plots in my output, one with the original sampling at 8.0 Hz and then on the 
right side shows the 3-bit quantization plot. 

### Conclusion Questions from Assignment
1. Reasonable sampling frequency: 
    - At least 2× the signal frequency (Nyquist rule).
    - But going a bit higher (like 3–4×) makes the signal look better.
2. How to minimize error:
    - Use more samples (higher sampling frequency).
    - Use more bits (finer quantization)

## Access Output
image_formation/images/exercise3_8Hz_3bits.png

---------------

## Exercise 4: Noise and Error Analysis
### Description
The final exercise involved analyzing the effects of noise on signals and quantifying the error during sampling and quantization. 
I added Gaussian noise to signals and calculated metrics such as Mean Squared Error, Root Mean Squared Error, and 
Peak Signal Noise Ratio to evaluate the quality of the processed signals. Additionally, sampled, quantize, and 
plotted the noise signal similarly to exercise three.

### Key Concepts
- **Gaussian Noise**: Simulated random noise to mimic real-world imperfections in the model.
- **Error Metrics**:
  - **MSE (Mean Squared Error)**: Measures the average squared difference between the original and processed signals.
  - **RMSE (Root Mean Squared Error)**: Provides a more interpretable measure of error.
  - **PSNR (Peak Signal-to-Noise Ratio)**: Evaluates the quality of the signal relative to its peak value.

### Reflection
This exercise emphasized the importance of error analysis within image processing. By visualizing the noisy and quantized signals, 
I gained a better understanding of how noise impacts signal fidelity. The use of metrics like PSNR provided a quantitative way to 
compare different techniques in image processing. I decided to plot everything in one view with three different plots that build 
off of one another to show first the continous clean vs noisy, then sampling at 8.0 Hz (noisy), and lastly the quantization of the 
noisy samples.

## Example Console Output (varies)
METRICS @ 8.0 Hz
Noisy  vs clean:  MSE=0.04356  RMSE=0.20872  PSNR=13.61 dB
Quant vs clean:   MSE=0.04135  RMSE=0.20336  PSNR=13.83 dB

## Access Output
image_formation/images/exercise4_all_8Hz_3bits.png

---------------

## Conclusion
Through these exercises, I was able to explore the foundational concepts of computer vision and image processing. 
Each exercise provided valuable insights into the mathematical and physical aspects that are in modern computer vision systems. 
This repository serves as a foundational resource regarding Computer Vision for understanding and applying these concepts in close 
to real-world scenarios.

---------------