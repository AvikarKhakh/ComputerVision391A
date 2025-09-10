# Exercise 2: Thin lens & f-numbers

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# image folder path (same as in Exercise 1)
IMAGES_DIR = Path(__file__).parent / "images"
IMAGES_DIR.mkdir(exist_ok=True)  # make sure folder exists

def thin_lens_zi(f_mm: float, zo_mm: float) -> float:
    # Thin lens formula: 1/f = 1/Zo + 1/Zi
    if zo_mm <= f_mm:
        raise ValueError("Zo must be > f (object beyond focal length).")
    # Zi = (f * Zo) / (Zo - f)
    return (f_mm * zo_mm) / (zo_mm - f_mm)

def zi_curve_for_f(f_mm: float):
    # Generate zo values from slightly > f to 10,000 * f
    zo = np.logspace(np.log10(1.1 * f_mm), np.log10(1e4 * f_mm), num=2000)
    zi = (f_mm * zo) / (zo - f_mm)  # vectorized thin lens
    return zo, zi

def plot_both(f_list, f_numbers):
    fig, axes = plt.subplots(1, 2, figsize=(14,6)) # 1 row, 2 columns

    # Left: zi vs zo
    ax = axes[0]
    # Plot zi vs zo for each f
    for f in f_list:
        zo, zi = zi_curve_for_f(f)
        ax.loglog(zo, zi, label=f"f={f} mm")
        ax.axvline(f, linestyle="--", linewidth=1)
    ax.set_xlabel("Object Distance Zo (mm)") # x-axis label
    ax.set_ylabel("Image Distance Zi (mm)") # y-axis label
    ax.set_ylim(1, 3000) # y-axis limits
    ax.set_title("Thin Lens Law") # plot title
    
    # Allows plot to be read more easily
    ax.grid(True, which="major", linestyle='-', linewidth=0.7)
    ax.grid(True, which="minor", linestyle=':', linewidth=0.4)
    
    ax.legend()

    # Right: aperture diameter vs f
    ax = axes[1]
    f_vals = np.linspace(min(f_list), 600, 200)
    # Plot D vs f for each f-number
    for N in f_numbers:
        D = f_vals / N
        ax.plot(f_vals, D, label=f"f/{N}")
    ax.set_xlabel("Focal Length f (mm)") # x-axis label
    ax.set_ylabel("Aperture Diameter D (mm)") # y-axis label
    ax.set_title("Aperture vs Focal Length") # plot title
    ax.grid(True)
    ax.legend()

    # Mark real lenses as points on the lines
    lenses = [
        (24, 1.4),
        (50, 1.8),
        (70, 2.8),
        (200, 2.8),
        (400, 2.8),
        (600, 4.0),
    ]
    # for loop to plot and annotate each lens
    for f_mm, N in lenses:
        D = f_mm / N
        ax.scatter([f_mm], [D], s=20, color="black", zorder=5)

    plt.tight_layout()
    
    # Save the figure in images folder for README
    out_path = IMAGES_DIR / "exercise2_plots.png"
    plt.savefig(out_path, dpi=200, bbox_inches="tight")

    plt.show()

def print_lens_apertures():
    # D = f / N
    lenses = [
        ("24mm f/1.4", 24.0, 1.4),
        ("50mm f/1.8", 50.0, 1.8),
        ("70mm f/2.8", 70.0, 2.8),
        ("200mm f/2.8", 200.0, 2.8),
        ("400mm f/2.8", 400.0, 2.8),
        ("600mm f/4.0", 600.0, 4.0),
    ]
    # Calculate and print aperture diameters
    print("\nAperture diameters (D = f / N):")
    # for loop to print each lens and its aperture diameter
    for name, f, N in lenses:
        D = f / N
        print(f"  {name:<14} -> D = {D:.1f} mm")

def main():
    # Focal lengths and f-numbers to plot
    f_list = [3.0, 9.0, 50.0, 200.0]
    # f-numbers for aperture diameter lines
    plot_both(f_list, [1.4, 1.8, 2.8, 4.0]) 
    # Print aperture diameters for common lenses
    print_lens_apertures()                  

# Execute main function
if __name__ == "__main__":
    main()