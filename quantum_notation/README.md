# 🌌 Quantum Notation Images

This folder contains the quantum state equation images used in the game's educational overlays.

## 📐 Required Images

### Superposition States
- **superposition_plus.png**: |+⟩ = H|0⟩ = 1/√2 (|0⟩ + |1⟩)
- **superposition_minus.png**: |-⟩ = H|1⟩ = 1/√2 (|0⟩ - |1⟩)

### Bell States (Entanglement)
- **bell_phi_plus.png**: |Φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)
- **bell_phi_minus.png**: |Φ⁻⟩ = 1/√2 (|00⟩ - |11⟩)
- **bell_psi_plus.png**: |Ψ⁺⟩ = 1/√2 (|01⟩ + |10⟩)
- **bell_psi_minus.png**: |Ψ⁻⟩ = 1/√2 (|01⟩ - |10⟩)

### Measurement States
- **measurement_collapse.png**: ⟨ψ|M|ψ⟩ → |0⟩ or |1⟩
- **measurement_probability.png**: P(|0⟩) = |α|², P(|1⟩) = |β|²

### Tunneling States
- **tunneling_probability.png**: T = |t|² = 4k₁k₂/(k₁+k₂)²
- **tunneling_wavefunction.png**: ψ(x) = Ae^(ikx) + Be^(-ikx)

## 🎨 Image Specifications

- **Format**: PNG with transparent background
- **Size**: 400x100 pixels (recommended)
- **Style**: Clean, mathematical notation on transparent background
- **Colors**: White or light blue text for visibility on dark game background

## 🔄 Current Status

Currently using **text-based rendering** with pygame fonts. 

**Option 1**: Keep text-based (works great, no additional files needed)
**Option 2**: Replace with PNG images for more professional mathematical notation

## 📝 LaTeX Source (for creating images)

If you want to create the PNG images from LaTeX:

### Superposition
```latex
|+\rangle = H|0\rangle = \frac{1}{\sqrt{2}} \left( |0\rangle + |1\rangle \right)
|-\rangle = H|1\rangle = \frac{1}{\sqrt{2}} \left( |0\rangle - |1\rangle \right)
```

### Bell States
```latex
|\Phi^+\rangle = \frac{1}{\sqrt{2}} \left( |00\rangle + |11\rangle \right)
|\Phi^-\rangle = \frac{1}{\sqrt{2}} \left( |00\rangle - |11\rangle \right)
|\Psi^+\rangle = \frac{1}{\sqrt{2}} \left( |01\rangle + |10\rangle \right)
|\Psi^-\rangle = \frac{1}{\sqrt{2}} \left( |01\rangle - |10\rangle \right)
```

## 🚀 Implementation

The quantum notation system is already implemented and working with text rendering. Adding images is optional for enhanced visual appeal.

**Current implementation**: ✅ Working with beautiful text rendering
**Image enhancement**: 🔄 Optional upgrade for even more professional look
