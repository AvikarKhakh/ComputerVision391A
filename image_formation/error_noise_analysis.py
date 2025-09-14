# Exercise 4: Noise & Error Analysis

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

# Globals / params
signal_freq   = 5.0     
duration      = 2.0     
sampling_freq = 8.0     
num_bits      = 3
min_signal    = -1.0
max_signal    =  1.0

# Noise params
noise_mean = 0.0
noise_std  = 0.1        # relative to signal magnitude

def mse(a, b):
    # mean squared error
    a = np.asarray(a); b = np.asarray(b)
    return float(np.mean((a - b) ** 2))

def rmse(a, b):
    # root mean squared error
    return float(np.sqrt(mse(a, b)))

def psnr(a, b, peak=1.0):
    # peak signal to noise ratio
    m = mse(a, b)
    # avoid div by zero
    if m == 0:
        return float("inf")
    return 10.0 * np.log10((peak ** 2) / m)

def original_signal(t):
    return np.sin(2*np.pi*signal_freq*t)

def add_gaussian_noise(signal, mean=noise_mean, std=noise_std):
    # scale noise relative to signal magnitude
    mag = np.max(signal) - np.min(signal)
    noise = np.random.normal(mean, std * mag, size=signal.shape) # Gaussian noise
    return signal + noise

def quantize(vals, bits, vmin, vmax):
    # uniform mid-tread quantization
    n = 2 ** bits
    q_idx = np.rint((vals - vmin) / (vmax - vmin) * (n - 1)).astype(int) # quantization indices
    q_idx = np.clip(q_idx, 0, n - 1) # ensure in range
    q_vals = vmin + q_idx * (vmax - vmin) / (n - 1) # quantized values

    return q_vals, q_idx

def plot_all_one_view(samp_freq_hz: float, bits: int = num_bits):

    # continuous reference
    t_cont = np.linspace(0, duration, 1000, endpoint=False)
    s_cont = original_signal(t_cont)
    s_cont_noisy = np.clip(add_gaussian_noise(s_cont), min_signal, max_signal)

    # sampling (clean), add noise to samples, then quantize
    n = int(samp_freq_hz * duration)
    t_s = np.linspace(0, duration, n, endpoint=False)
    s_s = original_signal(t_s)                                   # clean samples
    s_noisy = np.clip(add_gaussian_noise(s_s), min_signal, max_signal)
    q_vals, _ = quantize(s_noisy, bits, min_signal, max_signal)  # quantized samples

    # figure layout
    fig = plt.figure(figsize=(15, 4))
    fig.suptitle(f"Noise & Error with {samp_freq_hz:.1f}Hz (signal {signal_freq}Hz)", fontweight="bold")
    gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.25)

    # 1 - clean vs noisy (continuous)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t_cont, s_cont, label="Clean")
    ax1.plot(t_cont, s_cont_noisy, label="Noisy", alpha=0.9)
    ax1.set_xlim(0, duration); ax1.set_ylim(-1.2, 1.2)
    ax1.set_xlabel("time (s)"); ax1.set_ylabel("Amplitude")
    ax1.set_title("Continuous (clean vs noisy)")
    ax1.grid(True); ax1.legend()

    # 2 - noisy samples
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t_cont, s_cont, label="Continuous")
    ax2.stem(t_s, s_noisy, linefmt="C1-", markerfmt="C1o", basefmt=" ", label="Noisy Samples")
    ax2.set_xlim(0, duration); ax2.set_ylim(-1.2, 1.2)
    ax2.set_xlabel("time (s)")
    ax2.set_title(f"Sampling at {samp_freq_hz:.1f}Hz (noisy)")
    ax2.grid(True); ax2.legend()

    # 3 - quantized staircase
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.plot(t_cont, s_cont, alpha=0.35, label="Continuous")
    ax3.step(t_s, q_vals, where="post", linestyle="--", label=f"Quantized ({bits} Bits)")
    ax3.stem(t_s, s_noisy, linefmt="C1-", markerfmt="C1o", basefmt=" ", label="Noisy Samples")
    ax3.set_xlim(0, duration); ax3.set_ylim(-1.2, 1.2)
    ax3.set_xlabel("time (s)")
    ax3.set_title("Quantization of Noisy Samples")
    ax3.grid(True); ax3.legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # save image
    img_dir = Path(__file__).parent / "images"
    img_dir.mkdir(exist_ok=True)
    out = img_dir / f"exercise4_all_{int(samp_freq_hz)}Hz_{bits}bits.png"
    fig.savefig(out, dpi=200)


    # metrics vs clean sampled signal
    print("\nMetrics @ {:.1f} Hz".format(samp_freq_hz))
    # continuous noisy vs clean
    print("Noisy  vs clean:  MSE={:.5f}  RMSE={:.5f}  PSNR={:.2f} dB" .format(mse(s_noisy, s_s), rmse(s_noisy, s_s), psnr(s_noisy, s_s, peak=max_signal)))
    # quantized vs clean
    print("Quant vs clean:   MSE={:.5f}  RMSE={:.5f}  PSNR={:.2f} dB" .format(mse(q_vals, s_s), rmse(q_vals, s_s), psnr(q_vals, s_s, peak=max_signal)))

    plt.show()

# replace your main() with:
def main():
    plot_all_one_view(sampling_freq, num_bits)

if __name__ == "__main__":
    main()
