"""
===============================================================================
LAYER 4: VISUAL MANDALA GENERATOR
===============================================================================
Translates Smith Chart impedance reflection telemetry (Z = (1+Γ)/(1-Γ)) 
into dynamic Julia Set fractal coordinate offsets and ASCII terminal output.
Designed for execution on mobile ARM / Pydroid 3 runtimes.
===============================================================================
"""

import math
import cmath
import time

class SmithTelemetryMapper:
    """Calculates directional spiral telemetry and reflection coefficients."""
    
    @staticmethod
    def calculate_impedance(gamma: complex) -> complex:
        """Computes normalized complex impedance Z = (1 + Γ) / (1 - Γ)."""
        if gamma == complex(1, 0):
            return complex(float('inf'), float('inf'))
        return (1 + gamma) / (1 - gamma)

    @staticmethod
    def calculate_reclaimed_wave(gamma: complex, step: int, coherence: float = 0.985) -> float:
        """
        Reclaims boundary escape energy (Tesla stub inversion logic).
        Constructive superposition yield: W_peak = W0 + (eta * W_reclaimed)
        """
        gamma_mag = abs(gamma)
        gamma_phase = cmath.phase(gamma)
        
        # Stub-inversion condition
        reclaimed_factor = (1.0 / gamma_mag) if gamma_mag > 1.0 else (1.0 - gamma_mag)
        w_reclaimed = reclaimed_factor * math.sin((step * 0.5) + gamma_phase)
        
        w0 = math.sin(step * 0.2)
        w_peak = w0 + (coherence * w_reclaimed)
        return w_peak


class VisualMandalaEngine:
    """Renders dynamic fractal mandala frames driven by incoming telemetry."""
    
    def __init__(self, width: int = 44, height: int = 22):
        self.width = width
        self.height = height
        self.target_coherence = 0.985
        # ASCII density palette ranging from low to high density
        self.palette = " .:-=+*#%@"

    def render_frame(self, gamma: complex, w_peak: float) -> str:
        """
        Maps telemetry parameters directly onto the complex Julia plane:
        - Gamma magnitude & phase modulate the constant seed 'C'
        - Reclaimed W_peak dynamic scales the frame zoom
        """
        gamma_mag = abs(gamma)
        gamma_phase = cmath.phase(gamma)

        # Dynamic C parameter mapping: C = C0 + delta(Γ)
        c_re = -0.70 + (0.12 * gamma_mag * math.cos(gamma_phase))
        c_im = 0.27015 + (0.12 * gamma_mag * math.sin(gamma_phase))
        c_param = complex(c_re, c_im)

        # Zoom modulation driven by constructive peak resonance
        zoom = 1.0 + (0.25 * abs(w_peak))
        
        lines = []
        max_iter = 15

        for y in range(self.height):
            line = []
            # Normalize display grid coordinates to complex plane [-1.5, 1.5]
            zy = ((y / self.height) * 3.0 - 1.5) / zoom
            for x in range(self.width):
                zx = ((x / self.width) * 3.0 - 1.5) / zoom
                z = complex(zx, zy)
                
                # Standard Julia iteration loop: Z_(n+1) = Z_n^2 + C
                iters = 0
                while abs(z) <= 2.0 and iters < max_iter:
                    z = (z * z) + c_param
                    iters += 1
                
                # Character lookup based on iteration escape count
                char_idx = int((iters / max_iter) * (len(self.palette) - 1))
                line.append(self.palette[char_idx])
            lines.append("".join(line))
            
        return "\n".join(lines)


def run_directional_spiral_simulation(steps: int = 12):
    """
    Executes a 12-step directional spiral telemetry loop from Step 01 (|Γ|=0.9)
    down to Step 12 Resonance Lock (|Γ|=0.0, SWR=1.0).
    """
    engine = VisualMandalaEngine()
    mapper = SmithTelemetryMapper()

    print("=" * 50)
    print(" MANDALA SYNTHESIZER: LAYER 4 EXECUTION RUNTIME")
    print("=" * 50)

    for i in range(1, steps + 1):
        # Clockwise inward spiral vector modulation
        progress = (i - 1) / float(steps - 1)
        radius = 0.90 * (1.0 - progress)
        angle = -1.0 * ((i - 1) * (2.0 * math.pi / 3.0))
        gamma = cmath.rect(radius, angle)
        
        # Calculate impedance & wave peak
        z_imp = mapper.calculate_impedance(gamma)
        w_peak = mapper.calculate_reclaimed_wave(gamma, i)
        
        # SWR calculation
        swr = (1.0 + abs(gamma)) / (1.0 - abs(gamma)) if abs(gamma) < 1.0 else float('inf')

        # Render output frame
        frame = engine.render_frame(gamma, w_peak)

        # Display Step Header and Visual Frame
        print(f"\n--- STEP {i:02d}/{steps:02d} | |Γ|={abs(gamma):.2f} @ {math.degrees(angle)%360:3.0f}° | SWR={swr:.2f} ---")
        print(f"Impedance Z = {z_imp.real:.2f} + {z_imp.imag:.2f}j | W_peak = {w_peak:.3f}")
        print("-" * 50)
        print(frame)
        
        time.sleep(0.05)


if __name__ == "__main__":
    run_directional_spiral_simulation(steps=12)
