#!/usr/bin/env python3
"""
LaTeX Equation Renderer for Quantum Notation
Uses matplotlib to render proper mathematical equations
"""

import pygame
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import mathtext
import numpy as np
import io
from PIL import Image
import os
from typing import Tuple, Optional

class LaTeXRenderer:
    def __init__(self):
        # Configure matplotlib for LaTeX rendering
        plt.rcParams['text.usetex'] = False  # Use mathtext instead of full LaTeX for compatibility
        plt.rcParams['font.size'] = 20
        plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern font
        
        # Cache for rendered equations
        self.equation_cache = {}
        
        # Ensure cache directory exists
        self.cache_dir = "equation_cache"
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def render_equation_to_surface(self, latex_equation: str, color: Tuple[int, int, int] = (255, 255, 255), 
                                 font_size: int = 24) -> pygame.Surface:
        """Render a LaTeX equation to a pygame surface"""
        
        # Create cache key
        cache_key = f"{latex_equation}_{color}_{font_size}"
        
        # Check cache first
        if cache_key in self.equation_cache:
            return self.equation_cache[cache_key]
        
        try:
            # Create figure with transparent background
            fig, ax = plt.subplots(figsize=(8, 2), facecolor='none')
            ax.set_facecolor('none')
            
            # Remove axes
            ax.axis('off')
            
            # Render the equation
            text_color = tuple(c/255.0 for c in color)  # Convert to matplotlib color format
            ax.text(0.5, 0.5, f'${latex_equation}$', 
                   horizontalalignment='center', 
                   verticalalignment='center',
                   fontsize=font_size,
                   color=text_color,
                   transform=ax.transAxes)
            
            # Save to bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', 
                       facecolor='none', edgecolor='none', 
                       transparent=True, dpi=150)
            buf.seek(0)
            
            # Load with PIL and convert to pygame surface
            pil_image = Image.open(buf)
            
            # Convert PIL image to pygame surface
            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()
            
            pygame_surface = pygame.image.fromstring(data, size, mode)
            
            # Convert to per-pixel alpha for transparency
            pygame_surface = pygame_surface.convert_alpha()
            
            plt.close(fig)
            buf.close()
            
            # Cache the result
            self.equation_cache[cache_key] = pygame_surface
            
            return pygame_surface
            
        except Exception as e:
            print(f"LaTeX rendering failed for '{latex_equation}': {e}")
            # Fallback to text rendering
            return self._fallback_text_render(latex_equation, color, font_size)
    
    def _fallback_text_render(self, text: str, color: Tuple[int, int, int], font_size: int) -> pygame.Surface:
        """Fallback text rendering if LaTeX fails"""
        font = pygame.font.Font(None, font_size)
        surface = font.render(text, True, color)
        return surface
    
    def clear_cache(self):
        """Clear the equation cache"""
        self.equation_cache.clear()

# Global renderer instance
latex_renderer = LaTeXRenderer()

# Quantum equation definitions with proper LaTeX
QUANTUM_EQUATIONS = {
    'bell_phi_plus': {
        'latex': r'|\Phi^+\rangle = \frac{1}{\sqrt{2}} \left( |00\rangle + |11\rangle \right)',
        'description': 'Bell State: Maximally Entangled',
        'color': (100, 200, 255)
    },
    'bell_phi_minus': {
        'latex': r'|\Phi^-\rangle = \frac{1}{\sqrt{2}} \left( |00\rangle - |11\rangle \right)',
        'description': 'Bell State: Anti-correlated',
        'color': (200, 100, 255)
    },
    'bell_psi_plus': {
        'latex': r'|\Psi^+\rangle = \frac{1}{\sqrt{2}} \left( |01\rangle + |10\rangle \right)',
        'description': 'Bell State: Triplet State',
        'color': (100, 255, 150)
    },
    'bell_psi_minus': {
        'latex': r'|\Psi^-\rangle = \frac{1}{\sqrt{2}} \left( |01\rangle - |10\rangle \right)',
        'description': 'Bell State: Singlet State',
        'color': (255, 215, 0)
    },
    'superposition_plus': {
        'latex': r'|+\rangle = H|0\rangle = \frac{1}{\sqrt{2}} \left( |0\rangle + |1\rangle \right)',
        'description': 'Superposition: Plus State',
        'color': (100, 255, 150)
    },
    'superposition_minus': {
        'latex': r'|-\rangle = H|1\rangle = \frac{1}{\sqrt{2}} \left( |0\rangle - |1\rangle \right)',
        'description': 'Superposition: Minus State',
        'color': (100, 200, 255)
    },
    'measurement_collapse': {
        'latex': r'\langle\psi|M|\psi\rangle \rightarrow |0\rangle \text{ or } |1\rangle',
        'description': 'Wave Function Collapse',
        'color': (255, 215, 0)
    },
    'measurement_probability': {
        'latex': r'P(|0\rangle) = |\alpha|^2, \quad P(|1\rangle) = |\beta|^2',
        'description': 'Measurement Probabilities',
        'color': (200, 100, 255)
    },
    'tunneling_probability': {
        'latex': r'T = |t|^2 = \frac{4k_1k_2}{(k_1+k_2)^2}',
        'description': 'Quantum Tunneling Probability',
        'color': (100, 200, 255)
    },
    'tunneling_wavefunction': {
        'latex': r'\psi(x) = Ae^{ik_1x} + Be^{-ik_1x}',
        'description': 'Tunneling Wave Function',
        'color': (100, 255, 150)
    },
    
    # Quantum Gates (for single qubit collection)
    'hadamard_gate': {
        'latex': r'H|0\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)',
        'description': 'Hadamard Gate: Creates Superposition',
        'color': (100, 255, 150)
    },
    'pauli_x_gate': {
        'latex': r'X|0\rangle = |1\rangle, \quad X|1\rangle = |0\rangle',
        'description': 'Pauli-X Gate: Bit Flip Operation',
        'color': (100, 200, 255)
    },
    'pauli_z_gate': {
        'latex': r'Z|+\rangle = |-\rangle, \quad Z|-\rangle = |+\rangle',
        'description': 'Pauli-Z Gate: Phase Flip',
        'color': (255, 215, 0)
    },
    'cnot_gate': {
        'latex': r'CNOT|00\rangle = |00\rangle, \quad CNOT|10\rangle = |11\rangle',
        'description': 'CNOT Gate: Entangling Operation',
        'color': (100, 200, 255)
    },
    
    # Quantum Concepts
    'uncertainty_principle': {
        'latex': r'\Delta x \Delta p \geq \frac{\hbar}{2}',
        'description': 'Heisenberg Uncertainty Principle',
        'color': (100, 200, 255)
    },
    'no_cloning_theorem': {
        'latex': r'\nexists U: U|\psi\rangle|0\rangle = |\psi\rangle|\psi\rangle',
        'description': 'No-Cloning Theorem: Cannot Copy Unknown States',
        'color': (200, 100, 255)
    },
    'born_rule': {
        'latex': r'P(x) = |\psi(x)|^2',
        'description': 'Born Rule: Measurement Probability',
        'color': (200, 100, 255)
    },
    'quantum_interference': {
        'latex': r'|\psi\rangle = |0\rangle - |1\rangle \Rightarrow |\langle 0|\psi\rangle|^2 = 0',
        'description': 'Quantum Interference: Destructive Cancellation',
        'color': (100, 255, 150)
    }
}

def get_equation_surface(equation_key: str, font_size: int = 32) -> Tuple[pygame.Surface, str, Tuple[int, int, int]]:
    """Get a rendered equation surface by key"""
    if equation_key not in QUANTUM_EQUATIONS:
        raise ValueError(f"Unknown equation key: {equation_key}")
    
    eq_data = QUANTUM_EQUATIONS[equation_key]
    surface = latex_renderer.render_equation_to_surface(
        eq_data['latex'], 
        eq_data['color'], 
        font_size
    )
    
    return surface, eq_data['description'], eq_data['color']

def test_latex_rendering():
    """Test function to verify LaTeX rendering works"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("LaTeX Equation Test")
    
    clock = pygame.time.Clock()
    running = True
    
    # Test equations
    test_equations = ['bell_phi_plus', 'superposition_plus', 'measurement_collapse']
    current_eq = 0
    
    print("LaTeX Equation Test - Press SPACE to cycle through equations, ESC to exit")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    current_eq = (current_eq + 1) % len(test_equations)
        
        screen.fill((0, 0, 0))
        
        # Render current equation
        try:
            eq_key = test_equations[current_eq]
            surface, description, color = get_equation_surface(eq_key, 36)
            
            # Center the equation
            rect = surface.get_rect(center=(400, 250))
            screen.blit(surface, rect)
            
            # Show description
            font = pygame.font.Font(None, 24)
            desc_surface = font.render(description, True, color)
            desc_rect = desc_surface.get_rect(center=(400, 350))
            screen.blit(desc_surface, desc_rect)
            
            # Instructions
            inst_surface = font.render("SPACE: Next equation, ESC: Exit", True, (255, 255, 255))
            inst_rect = inst_surface.get_rect(center=(400, 500))
            screen.blit(inst_surface, inst_rect)
            
        except Exception as e:
            # Show error
            font = pygame.font.Font(None, 36)
            error_surface = font.render(f"Rendering Error: {str(e)}", True, (255, 100, 100))
            error_rect = error_surface.get_rect(center=(400, 300))
            screen.blit(error_surface, error_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_latex_rendering()
