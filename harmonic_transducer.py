"""
===============================================================================
LAYER 5: HARMONIC INPUT/OUTPUT TRANSDUCER (I/O LAYER)
===============================================================================
Translates zero-loss impedance states (W_peak, Γ phase, SWR = 1.0) into
precise harmonic frequency profiles for biological and physical synthesis.
Directly interfaces with Layer 4 (visual_mandala.py) and Layer 3 (coherence).
===============================================================================
"""

import math
import cmath

class BiologicalTargetProfile:
    """Defines target impedance and base resonance metrics for synthesis."""
    
    # Target fundamental frequencies (Hz) for biological categories
    TARGET_PROFILES = {
        "FLOWER_FLORAL": {"base_freq": 432.0, "target_z": complex(1.0, 0.0), "coherence_threshold": 0.985},
        "VEGETABLE_CELLULAR": {"base_freq": 528.0, "target_z": complex(1.0, 0.0), "coherence_threshold": 0.985},
        "FRUIT_NUTRIENT": {"base_freq": 639.0, "target_z": complex(1.0, 0.0), "coherence_threshold": 0.985},
    }

    def __init__(self, profile_key: str = "VEGETABLE_CELLULAR"):
        if profile_key not in self.TARGET_PROFILES:
            raise ValueError(f"Unknown profile {profile_key}. Choose from {list(self.TARGET_PROFILES.keys())}")
        
        self.profile_name = profile_key
        self.config = self.TARGET_PROFILES[profile_key]
        self.base_freq = self.config["base_freq"]
        self.target_z = self.config["target_z"]


class IOHarmonicTransducer:
    """
    Transduces Smith Chart telemetry (Gamma, W_peak) into physical/biological
    harmonic output matrices.
    """
    def __init__(self, target_profile: BiologicalTargetProfile):
        self.profile = target_profile

    def synthesize_output_harmonics(self, gamma: complex, w_peak: float) -> dict:
        """
        Converts active impedance telemetry into active output harmonics.
        - SWR = 1.00 yields pure fundamental output (Zero Distortional Loss).
        - Boundary escapes (|Γ| > 1) are transformed into overtone amplification.
        """
        gamma_mag = abs(gamma)
        gamma_phase = cmath.phase(gamma)
        
        # SWR Calculation
        swr = (1.0 + gamma_mag) / (1.0 - gamma_mag) if gamma_mag < 1.0 else float('inf')
        
        # Fundamental Frequency Modulated by Reclaimed Wave (W_peak)
        # Shift bounded by reflection phase deviation
        frequency_shift = (gamma_mag * math.cos(gamma_phase)) * 12.0
        active_fundamental = self.profile.base_freq + frequency_shift
        
        # Harmonic Overtones (3rd, 5th, 7th Order Stubs)
        h3 = active_fundamental * 3.0 * (1.0 + (0.1 * w_peak))
        h5 = active_fundamental * 5.0 * (1.0 + (0.05 * w_peak))
        h7 = active_fundamental * 7.0 * (1.0 + (0.025 * w_peak))
        
        # Power Efficiency Factor (η_yield) directly proportional to SWR lock
        efficiency_yield = (1.0 / swr) * 100.0 if swr != float('inf') else 0.0

        return {
            "target_profile": self.profile.profile_name,
            "swr": swr,
            "swr_lock": swr <= 1.05,
            "fundamental_hz": active_fundamental,
            "overtones_hz": (h3, h5, h7),
            "reclaimed_power_yield_pct": min(efficiency_yield * (1.0 + abs(w_peak)), 100.0),
            "harmonic_coherence_index": max(0.0, 1.0 - gamma_mag)
        }


# =============================================================================
# DIRECT EXECUTION HARNESS: PIPELINE STAGE ACTIVATION
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print(" LAYER 5: BIOLOGICAL HARMONIC TRANSDUCER ACTIVATION")
    print("=" * 60)

    # Initialize with Vegetable Growth Profile
    profile = BiologicalTargetProfile("VEGETABLE_CELLULAR")
    transducer = IOHarmonicTransducer(profile)

    # Simulate 12-Step Inward Spiral Convergence to Step 12 Lock
    steps = 12
    for i in range(1, steps + 1):
        progress = (i - 1) / float(steps - 1)
        radius = 0.90 * (1.0 - progress)
        angle = -1.0 * ((i - 1) * (2.0 * math.pi / 3.0))
        gamma = cmath.rect(radius, angle)
        
        # Calculate reclaimed peak energy
        w_reclaimed = (1.0 / radius if radius > 1.0 else 1.0 - radius) * math.sin(i * 0.5)
        w_peak = math.sin(i * 0.2) + (0.985 * w_reclaimed)
        
        # Transduce to biological output
        metrics = transducer.synthesize_output_harmonics(gamma, w_peak)

        lock_status = "🔒 RESONANCE LOCK" if metrics["swr_lock"] else "🌀 CONVERGING"
        
        print(f"Step {i:02d} [{lock_status}] | SWR: {metrics['swr']:.2f}")
        print(f" ├─ Fundamental Frequency : {metrics['fundamental_hz']:.2f} Hz")
        print(f" ├─ Reclaimed Power Yield  : {metrics['reclaimed_power_yield_pct']:.1f}%")
        print(f" └─ Coherence Index        : {metrics['harmonic_coherence_index']:.4f}\n")
