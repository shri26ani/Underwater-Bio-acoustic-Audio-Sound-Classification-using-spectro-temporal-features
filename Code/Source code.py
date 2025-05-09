# -*- coding: utf-8 -*-
"""Testing

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-eQTjakL3HT65T78_Z6LHIFfL-caUsam
"""

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from sklearn.svm import SVC
from scipy.fftpack import fft

# Load the WAV file
audio_file = '/content/drive/MyDrive/MTP_Audio_Dataset/Dataset/Dolphin/Bottlenose Dolphin/56006001.wav'  # Replace with actual filename
y, sr = librosa.load(audio_file, sr=None)

# Compute FFT for amplitude vs frequency plot
n = len(y)
yf = np.abs(fft(y)[:n // 2])  # Take positive frequencies only
xf = np.linspace(0, sr / 2, len(yf))  # Frequency axis

# Plot 1: Amplitude vs Frequency (FFT Spectrum)
plt.figure(figsize=(12, 5))
plt.plot(xf, yf, color='blue')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('Amplitude vs Frequency Spectrum')
plt.show()

# Compute MFCCs
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# Plot 2: Amplitude vs Frequency with MFCC filter banks
plt.figure(figsize=(12, 5))
plt.plot(xf, yf, color='blue', alpha=0.5)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('Amplitude vs Frequency with MFCC Filter Banks')

# Overlay MFCC filter banks
mel_filters = librosa.filters.mel(sr=sr, n_fft=n, n_mels=13)
mel_freqs = librosa.mel_frequencies(n_mels=13, fmin=0, fmax=sr / 2)
for i, freq in enumerate(mel_freqs):
    plt.axvline(x=freq, color='red', linestyle='--', alpha=0.6, label='MFCC Filter' if i == 0 else "")

plt.legend()
plt.show()

# SVM Classification Setup (Placeholder, Replace with actual labeled dataset)
X_features = mfccs.T  # Feature matrix (MFCCs)
y_labels = np.random.randint(0, 2, X_features.shape[0])  # Random labels for illustration
clf = SVC(kernel='linear')
clf.fit(X_features, y_labels)
print("SVM Model Trained with MFCC Features")

import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import pandas as pd  # For displaying MFCC feature table

# Load the audio file
file_path = "/content/drive/MyDrive/MTP_Audio_Dataset/Dataset/Dolphin/Bottlenose Dolphin/56006001.wav"  # Change to your actual file path
y, sr = librosa.load(file_path, sr=None)  # Load at original sampling rate

# ------------------ Step 1: Compute Frequency Spectrum ------------------
N = 4096  # FFT size
Y = np.abs(np.fft.rfft(y, N))  # Compute FFT
frequencies = np.fft.rfftfreq(N, 1 / sr)  # Frequency bins

# ------------------ Step 2: Compute Mel Filter Bank -----------------
n_mfcc = 13  # Number of MFCC coefficients (Keep consistent with feature extraction)
mel_freqs = librosa.mel_frequencies(n_mfcc, fmin=20, fmax=sr//2)  # Extracted frequency range

# ------------------ Step 3: Compute MFCC Features ------------------
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

# Compute feature vectors (mean of MFCCs)
mfcc_means = np.mean(mfccs, axis=1)

# Normalize for visualization
normalized_features = (mfcc_means - np.min(mfcc_means)) / (np.max(mfcc_means) - np.min(mfcc_means))
scaled_features = normalized_features * np.max(Y)  # Scale to FFT amplitude

# ------------------ Step 4: Display Extracted MFCC Features ------------------
mfcc_table = pd.DataFrame({
    "MFCC Coefficient": range(1, n_mfcc + 1),
    "Mean MFCC Value": mfcc_means,
    "Corresponding Frequency (Hz)": mel_freqs
})
print("\nExtracted MFCC Feature Vectors:")
print(mfcc_table)

# ------------------ Step 5: Plot Amplitude vs Frequency with MFCC Features ------------------
plt.figure(figsize=(12, 6))
plt.plot(frequencies, Y, color='b', label="FFT Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Amplitude vs Frequency Spectrum with MFCC Features")
plt.grid()
plt.xlim(0, sr // 2)  # Limit x-axis to Nyquist frequency

# Overlay vertical lines for Mel Frequency Bins
for freq in mel_freqs:
    plt.axvline(x=freq, color='r', linestyle='--', alpha=0.6, label="Mel Filter Range" if freq == mel_freqs[0] else "")

# Overlay MFCC feature points (Ensure x and y have the same length)
plt.scatter(mel_freqs, scaled_features, color='black', marker='o', label="MFCC Feature Points")

plt.legend()
plt.show()

# Print the MFCC frequency range used
print(f"\nMFCC Frequency Range: {mel_freqs[0]:.2f} Hz to {mel_freqs[-1]:.2f} Hz")

import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load the audio file
file_path = "/content/drive/MyDrive/MTP_Audio_Dataset/Dataset/Dolphin/Bottlenose Dolphin/56006001.wav"  # Change to actual file path
y, sr = librosa.load(file_path, sr=None)  # Load at original sampling rate

# ------------------ Step 1: Compute MFCC Features ------------------
n_mfcc = 13  # Number of MFCC coefficients
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)

# Normalize MFCC features (zero mean, unit variance)
scaler = StandardScaler()
mfccs_scaled = scaler.fit_transform(mfccs.T)  # Transpose to shape (samples, features)

# ------------------ Step 2: Apply PCA ------------------
pca = PCA(n_components=n_mfcc)  # Apply PCA
mfccs_pca = pca.fit_transform(mfccs_scaled)  # Transform MFCC features

# Explained variance ratio
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

# ------------------ Step 3: Select Optimal Number of Components ------------------
# Find the number of components needed to explain 95% variance
optimal_components = np.argmax(cumulative_variance >= 0.95) + 1

# Print PCA results
print(f"\nOptimal Number of PCA Components to Retain 95% Variance: {optimal_components}")
print(f"Explained Variance of First {optimal_components} Components: {cumulative_variance[optimal_components-1]:.4f}")

# Get corresponding frequencies for MFCCs
mel_freqs = librosa.mel_frequencies(n_mfcc, fmin=20, fmax=sr//2)

# ------------------ Step 4: Plot Explained Variance vs. PCA Components ------------------
plt.figure(figsize=(8, 5))
plt.bar(range(1, n_mfcc + 1), explained_variance * 100, color='b', alpha=0.7)
plt.plot(range(1, n_mfcc + 1), cumulative_variance * 100, marker='o', linestyle='--', color='r', label="Cumulative Variance")
plt.axhline(y=95, color='g', linestyle='--', label="95% Variance Threshold")
plt.xlabel("PCA Components")
plt.ylabel("Explained Variance (%)")
plt.title("PCA Explained Variance of MFCC Features")
plt.legend()
plt.grid()
plt.show()

# ------------------ Step 5: Plot Important PCA Features vs. Frequency ------------------
plt.figure(figsize=(10, 5))
plt.bar(mel_freqs, pca.components_[0]**2, width=50, color='b', alpha=0.7)  # First principal component
plt.xlabel("Frequency (Hz)")
plt.ylabel("Principal Component Contribution")
plt.title("Importance of Frequencies in First PCA Component")
plt.grid()
plt.show()

# ------------------ Step 6: Print Most Relevant MFCC Features ------------------
top_pca_features = np.argsort(pca.components_[0]**2)[::-1][:5]  # Top 5 contributing features

print("\nTop 5 Most Important MFCC Features After PCA:")
for i, idx in enumerate(top_pca_features):
    print(f"Feature {idx+1}: Frequency {mel_freqs[idx]:.2f} Hz, Contribution {pca.components_[0][idx]**2:.4f}")