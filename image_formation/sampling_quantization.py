# Exercise 3: Sampling & Quantization

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# set up paths
IMG_DIR = Path(__file__).parent / "images"
IMG_DIR.mkdir(exist_ok=True)  # make sure folder exists

# Globals
signal_freq   = 5.0    # Hz
duration      = 2.0    # s
sampling_freq = 8.0    # Hz
num_bits      = 3      # 3-bit -> 8 levels
min_signal    = -1.0
max_signal    =  1.0

def original_signal(t):
    # s(t) = sin(2π f t)
    return np.sin(2 * np.pi * signal_freq * t)

def quantize(vals, bits, vmin, vmax):
    # map to [0, n-1], round, clip, then back to amplitude levels
    n = 2 ** bits
    # indices
    q_idx = np.rint((vals - vmin) / (vmax - vmin) * (n - 1)).astype(int)
    q_idx = np.clip(q_idx, 0, n - 1)
    q_vals = vmin + q_idx * (vmax - vmin) / (n - 1)
    
    return q_vals, q_idx

def make_panels_for(samp_freq_hz: float, bits: int = num_bits):
    # continuous
    t_cont = np.linspace(0, duration, 1000, endpoint=False)
    s_cont = original_signal(t_cont)

    # sampled
    n = int(samp_freq_hz * duration)
    t_s = np.linspace(0, duration, n, endpoint=False)
    s_s = original_signal(t_s)

    # quantize
    q_vals, _ = quantize(s_s, bits, min_signal, max_signal)

    # one figure with 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(f"Sampling at {samp_freq_hz:.1f} Hz (signal {signal_freq} Hz)")

    # left samples
    ax = axes[0]
    ax.plot(t_cont, s_cont, label="continuous")
    ax.stem(t_s, s_s, linefmt="C1-", markerfmt="C1o", basefmt=" ", label="samples")
    ax.set_xlim(0, duration); ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Amplitude")
    ax.set_title(f"Sampling at {samp_freq_hz:.1f} Hz")
    ax.grid(True); ax.legend()

    # right quantized staircase
    ax = axes[1]
    ax.plot(t_cont, s_cont, alpha=0.35, label="continuous")
    ax.step(t_s, q_vals, where="post", linestyle="--", label=f"Quantized ({bits} bits)")
    ax.stem(t_s, s_s, linefmt="C1-", markerfmt="C1o", basefmt=" ", label="samples")
    ax.set_xlim(0, duration); ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Amplitude")
    ax.set_title(f"Quantization ({bits} bits)")
    ax.grid(True); ax.legend()

    plt.tight_layout()

    # save figure
    out_path = IMG_DIR / f"exercise3_{int(samp_freq_hz)}Hz_{bits}bits.png"
    fig.savefig(out_path, dpi=200)
    
    plt.show()

def main():
    make_panels_for(8.0, num_bits)   # reproduce your current result

    # Write up conclusions below
    print("\nExercise 3 Conclusions")

    print("1. Reasonable sampling frequency:")
    print("   - At least 2× the signal frequency (Nyquist rule).")
    print("   - But going a bit higher (like 3–4×) makes the signal look better.\n")

    print("2. How to minimize error:")
    print("   - Use more samples (higher sampling frequency).")
    print("   - Use more bits (finer quantization)\n")

if __name__ == "__main__":
    main()