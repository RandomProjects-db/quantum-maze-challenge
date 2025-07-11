#!/usr/bin/env python3
"""
Quantum Notation Display System
Shows authentic quantum state equations as fading overlays with proper LaTeX rendering
"""

import pygame
import math
import random
from typing import Optional, Tuple

# Try to import LaTeX renderer, fallback to text if not available
try:
    from latex_renderer import get_equation_surface, QUANTUM_EQUATIONS
    LATEX_AVAILABLE = True
    print("✅ LaTeX rendering available - equations will display with proper mathematical notation")
except ImportError as e:
    LATEX_AVAILABLE = False
    print(f"⚠️ LaTeX rendering not available ({e}) - falling back to text rendering")

class QuantumNotationDisplay:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts for quantum notation
        self.equation_font = pygame.font.Font(None, 48)
        self.symbol_font = pygame.font.Font(None, 36)
        self.subscript_font = pygame.font.Font(None, 28)
        
        # Colors
        self.quantum_blue = (100, 200, 255)
        self.quantum_green = (100, 255, 150)
        self.quantum_purple = (200, 100, 255)
        self.quantum_gold = (255, 215, 0)
        
        # Active notifications
        self.active_notifications = []
        
        # Bell states (entanglement)
        self.bell_states = [
            {
                'name': 'Φ⁺',
                'equation': '|Φ⁺⟩ = 1/√2 (|00⟩ + |11⟩)',
                'description': 'Bell State: Maximally Entangled',
                'color': self.quantum_blue
            },
            {
                'name': 'Φ⁻',
                'equation': '|Φ⁻⟩ = 1/√2 (|00⟩ - |11⟩)',
                'description': 'Bell State: Anti-correlated',
                'color': self.quantum_purple
            },
            {
                'name': 'Ψ⁺',
                'equation': '|Ψ⁺⟩ = 1/√2 (|01⟩ + |10⟩)',
                'description': 'Bell State: Triplet State',
                'color': self.quantum_green
            },
            {
                'name': 'Ψ⁻',
                'equation': '|Ψ⁻⟩ = 1/√2 (|01⟩ - |10⟩)',
                'description': 'Bell State: Singlet State',
                'color': self.quantum_gold
            }
        ]
        
        # Superposition states
        self.superposition_states = [
            {
                'name': '|+⟩',
                'equation': '|+⟩ = H|0⟩ = 1/√2 (|0⟩ + |1⟩)',
                'description': 'Superposition: Plus State',
                'color': self.quantum_green
            },
            {
                'name': '|-⟩',
                'equation': '|-⟩ = H|1⟩ = 1/√2 (|0⟩ - |1⟩)',
                'description': 'Superposition: Minus State',
                'color': self.quantum_blue
            }
        ]
    
    def show_entanglement_notification(self):
        """Display a random Bell state equation"""
        if LATEX_AVAILABLE:
            bell_keys = ['bell_phi_plus', 'bell_phi_minus', 'bell_psi_plus', 'bell_psi_minus']
            bell_key = random.choice(bell_keys)
            eq_data = QUANTUM_EQUATIONS[bell_key]
            self._create_latex_notification(
                bell_key,
                eq_data['description'],
                eq_data['color'],
                duration=2.5,
                effect_type='entanglement'
            )
        else:
            # Fallback to text rendering
            bell_state = random.choice(self.bell_states)
            self._create_notification(
                bell_state['equation'],
                bell_state['description'],
                bell_state['color'],
                duration=2.5,
                effect_type='entanglement'
            )
    
    def show_superposition_notification(self):
        """Display a random superposition state equation"""
        if LATEX_AVAILABLE:
            superposition_keys = ['superposition_plus', 'superposition_minus']
            superposition_key = random.choice(superposition_keys)
            eq_data = QUANTUM_EQUATIONS[superposition_key]
            self._create_latex_notification(
                superposition_key,
                eq_data['description'],
                eq_data['color'],
                duration=2.5,
                effect_type='superposition'
            )
        else:
            # Fallback to text rendering
            superposition_state = random.choice(self.superposition_states)
            self._create_notification(
                superposition_state['equation'],
                superposition_state['description'],
                superposition_state['color'],
                duration=2.5,
                effect_type='superposition'
            )
    
    def show_measurement_notification(self):
        """Display wave function collapse equation"""
        if LATEX_AVAILABLE:
            measurement_keys = ['measurement_collapse', 'measurement_probability']
            measurement_key = random.choice(measurement_keys)
            eq_data = QUANTUM_EQUATIONS[measurement_key]
            self._create_latex_notification(
                measurement_key,
                eq_data['description'],
                eq_data['color'],
                duration=1.8,
                effect_type='measurement'
            )
        else:
            # Fallback to text rendering
            equations = [
                {
                    'equation': '⟨ψ|M|ψ⟩ → |0⟩ or |1⟩',
                    'description': 'Wave Function Collapse',
                    'color': self.quantum_gold
                },
                {
                    'equation': 'P(|0⟩) = |α|², P(|1⟩) = |β|²',
                    'description': 'Measurement Probabilities',
                    'color': self.quantum_purple
                }
            ]
            
            measurement = random.choice(equations)
            self._create_notification(
                measurement['equation'],
                measurement['description'],
                measurement['color'],
                duration=1.8,
                effect_type='measurement'
            )
    
    def show_tunneling_notification(self):
        """Display quantum tunneling equation"""
        if LATEX_AVAILABLE:
            tunneling_keys = ['tunneling_probability', 'tunneling_wavefunction']
            tunneling_key = random.choice(tunneling_keys)
            eq_data = QUANTUM_EQUATIONS[tunneling_key]
            self._create_latex_notification(
                tunneling_key,
                eq_data['description'],
                eq_data['color'],
                duration=1.5,
                effect_type='tunneling'
            )
        else:
            # Fallback to text rendering
            equations = [
                {
                    'equation': 'T = |t|² = 4k₁k₂/(k₁+k₂)²',
                    'description': 'Quantum Tunneling Probability',
                    'color': self.quantum_blue
                },
                {
                    'equation': 'ψ(x) = Ae^(ikx) + Be^(-ikx)',
                    'description': 'Tunneling Wave Function',
                    'color': self.quantum_green
                }
            ]
            
            tunneling = random.choice(equations)
            self._create_notification(
                tunneling['equation'],
                tunneling['description'],
                tunneling['color'],
                duration=1.5,
                effect_type='tunneling'
            )
    
    def show_quantum_gate_notification(self):
        """Display a random quantum gate or operation equation for single qubit collection"""
        if LATEX_AVAILABLE:
            gate_keys = [
                'hadamard_gate', 'pauli_x_gate', 'pauli_z_gate', 'cnot_gate',
                'uncertainty_principle', 'no_cloning_theorem', 'born_rule', 'quantum_interference'
            ]
            gate_key = random.choice(gate_keys)
            eq_data = QUANTUM_EQUATIONS[gate_key]
            self._create_latex_notification(
                gate_key,
                eq_data['description'],
                eq_data['color'],
                duration=2.0,  # Slightly shorter for single qubit collection
                effect_type='quantum_gate'
            )
        else:
            # Fallback to text rendering
            gate_equations = [
                {
                    'equation': 'H|0⟩ = 1/√2(|0⟩ + |1⟩)',
                    'description': 'Hadamard Gate: Creates Superposition',
                    'color': self.quantum_green
                },
                {
                    'equation': 'X|0⟩ = |1⟩, X|1⟩ = |0⟩',
                    'description': 'Pauli-X Gate: Bit Flip Operation',
                    'color': self.quantum_blue
                },
                {
                    'equation': 'Δx Δp ≥ ℏ/2',
                    'description': 'Heisenberg Uncertainty Principle',
                    'color': self.quantum_blue
                },
                {
                    'equation': 'P(x) = |ψ(x)|²',
                    'description': 'Born Rule: Measurement Probability',
                    'color': self.quantum_purple
                }
            ]
            
            gate = random.choice(gate_equations)
            self._create_notification(
                gate['equation'],
                gate['description'],
                gate['color'],
                duration=2.0,
                effect_type='quantum_gate'
            )
    
    def show_quantum_wisdom(self):
        """Display inspirational quantum physics quotes for immersion"""
        wisdom_quotes = [
            {
                'text': '"Reality is not local."',
                'description': 'Quantum Non-locality',
                'color': self.quantum_blue
            },
            {
                'text': '"The observer defines the outcome."',
                'description': 'Measurement Problem',
                'color': self.quantum_purple
            },
            {
                'text': '"Particles know when they\'re being watched."',
                'description': 'Observer Effect',
                'color': self.quantum_gold
            },
            {
                'text': '"Entanglement defies classical logic."',
                'description': 'Spooky Action at a Distance',
                'color': self.quantum_green
            },
            {
                'text': '"Uncertainty is a feature, not a bug."',
                'description': 'Heisenberg Principle',
                'color': self.quantum_blue
            },
            {
                'text': '"In the quantum realm, probability is law."',
                'description': 'Quantum Mechanics',
                'color': self.quantum_purple
            }
        ]
        
        wisdom = random.choice(wisdom_quotes)
        self._create_notification(
            wisdom['text'],
            wisdom['description'],
            wisdom['color'],
            duration=3.0,  # Longer for contemplation
            effect_type='quantum_wisdom'
        )
    
    def _create_notification(self, equation: str, description: str, color: Tuple[int, int, int], 
                           duration: float, effect_type: str):
        """Create a new quantum notation notification"""
        # Calculate stacking position based on existing notifications
        stack_offset = len(self.active_notifications) * 80  # 80 pixels between stacked notifications
        
        notification = {
            'equation': equation,
            'description': description,
            'color': color,
            'duration': duration,
            'timer': duration,
            'effect_type': effect_type,
            'alpha': 255,
            'scale': 0.1,  # Start small and grow
            'y_offset': 0,  # For floating animation
            'stack_position': stack_offset,  # Vertical stacking offset
            'glow_phase': 0
        }
        
        self.active_notifications.append(notification)
    
    def _create_latex_notification(self, equation_key: str, description: str, color: Tuple[int, int, int], 
                                 duration: float, effect_type: str):
        """Create a new quantum notation notification with LaTeX rendering"""
        # Calculate stacking position based on existing notifications
        stack_offset = len(self.active_notifications) * 80  # 80 pixels between stacked notifications
        
        notification = {
            'equation_key': equation_key,  # For LaTeX rendering
            'equation': None,  # Will be rendered as surface
            'description': description,
            'color': color,
            'duration': duration,
            'timer': duration,
            'effect_type': effect_type,
            'alpha': 255,
            'scale': 0.1,  # Start small and grow
            'y_offset': 0,  # For floating animation
            'stack_position': stack_offset,  # Vertical stacking offset
            'glow_phase': 0,
            'is_latex': True  # Flag to indicate LaTeX rendering
        }
        
        self.active_notifications.append(notification)
    
    def update(self, dt: float):
        """Update all active notifications"""
        for notification in self.active_notifications[:]:  # Copy list to avoid modification issues
            notification['timer'] -= dt
            notification['glow_phase'] += dt * 4
            
            # Animation phases
            progress = 1.0 - (notification['timer'] / notification['duration'])
            
            if progress < 0.15:  # Fade in and scale up (longer fade in for better stacking)
                notification['alpha'] = int(255 * (progress / 0.15))
                notification['scale'] = 0.1 + 0.9 * (progress / 0.15)
            elif progress > 0.85:  # Fade out (longer stable time)
                fade_progress = (progress - 0.85) / 0.15
                notification['alpha'] = int(255 * (1.0 - fade_progress))
            else:  # Stable display
                notification['alpha'] = 255
                notification['scale'] = 1.0
            
            # Floating animation
            notification['y_offset'] = math.sin(notification['glow_phase']) * 3
            
            # Remove expired notifications
            if notification['timer'] <= 0:
                self.active_notifications.remove(notification)
        
        # Update stack positions for smooth repositioning
        self._update_stack_positions(dt)
    
    def _update_stack_positions(self, dt: float):
        """Update stack positions for smooth repositioning when notifications expire"""
        target_positions = {}
        
        # Calculate target positions for each notification
        for i, notification in enumerate(self.active_notifications):
            target_y = i * 80  # 80 pixels between notifications
            target_positions[id(notification)] = target_y
        
        # Smoothly move notifications to their target positions
        for notification in self.active_notifications:
            target_y = target_positions[id(notification)]
            current_y = notification.get('stack_position', 0)
            
            # Smooth interpolation to target position
            if abs(target_y - current_y) > 1:
                notification['stack_position'] = current_y + (target_y - current_y) * dt * 8
            else:
                notification['stack_position'] = target_y
    
    def draw(self, screen):
        """Draw all active quantum notation overlays"""
        for notification in self.active_notifications:
            self._draw_notification(screen, notification)
    
    def _draw_notification(self, screen, notification):
        """Draw a single quantum notation overlay"""
        if notification['alpha'] <= 0:
            return
        
        # Calculate position (center of screen with stacking)
        center_x = self.screen_width // 2
        base_center_y = self.screen_height // 2
        
        # Apply stacking offset and floating animation
        center_y = (base_center_y - 100 +  # Start higher to accommodate stacking
                   notification.get('stack_position', 0) + 
                   notification['y_offset'])
        
        # Don't draw if too far down the screen
        if center_y > self.screen_height - 50:
            return
        
        if notification.get('is_latex', False) and LATEX_AVAILABLE:
            # LaTeX rendering
            try:
                equation_surface, _, _ = get_equation_surface(notification['equation_key'], 32)
                description_surface = self.symbol_font.render(notification['description'], True, notification['color'])
                
                # Apply alpha and scaling
                if notification['alpha'] < 255:
                    equation_surface.set_alpha(notification['alpha'])
                    description_surface.set_alpha(notification['alpha'])
                
                # Scale surfaces
                if notification['scale'] != 1.0:
                    eq_width = int(equation_surface.get_width() * notification['scale'])
                    eq_height = int(equation_surface.get_height() * notification['scale'])
                    desc_width = int(description_surface.get_width() * notification['scale'])
                    desc_height = int(description_surface.get_height() * notification['scale'])
                    
                    if eq_width > 0 and eq_height > 0:
                        equation_surface = pygame.transform.scale(equation_surface, (eq_width, eq_height))
                    if desc_width > 0 and desc_height > 0:
                        description_surface = pygame.transform.scale(description_surface, (desc_width, desc_height))
                
                # Position calculations - DEFINE THESE FIRST
                eq_rect = equation_surface.get_rect(center=(center_x, center_y - 10))
                desc_rect = description_surface.get_rect(center=(center_x, center_y + 40))
                
                # Create glow effect for LaTeX equations
                glow_intensity = (math.sin(notification['glow_phase']) + 1) * 0.3 + 0.4
                glow_alpha = int(notification['alpha'] * 0.6 * glow_intensity)
                
                # Create multiple glow layers for enhanced effect
                glow_offsets = [(-3, -3), (-3, 0), (-3, 3), (0, -3), (0, 3), (3, -3), (3, 0), (3, 3)]
                
                # Draw glow layers
                for dx, dy in glow_offsets:
                    glow_eq_surface = equation_surface.copy()
                    glow_desc_surface = description_surface.copy()
                    glow_eq_surface.set_alpha(glow_alpha)
                    glow_desc_surface.set_alpha(glow_alpha)
                    
                    screen.blit(glow_eq_surface, (eq_rect.x + dx, eq_rect.y + dy))
                    screen.blit(glow_desc_surface, (desc_rect.x + dx, desc_rect.y + dy))
                
                # Draw main LaTeX equation and description with quantum shimmer
                self._draw_with_quantum_shimmer(screen, equation_surface, eq_rect, notification)
                self._draw_with_quantum_shimmer(screen, description_surface, desc_rect, notification)
                
                # Draw quantum effect particles around the LaTeX equation
                self._draw_enhanced_quantum_particles(screen, center_x, center_y, notification)
                
                # Add energy pulse effect around LaTeX equations
                self._draw_energy_pulse(screen, center_x, center_y, notification)
                
                # Special effect for entanglement (Bell states)
                if notification['effect_type'] == 'entanglement':
                    self._draw_entanglement_resonance(screen, center_x, center_y, notification)
                
            except Exception as e:
                print(f"LaTeX rendering error: {e}")
                # Fallback to text rendering
                self._draw_text_notification(screen, notification, center_x, center_y)
        else:
            # Text rendering (fallback or when LaTeX not available)
            self._draw_text_notification(screen, notification, center_x, center_y)
    
    def _draw_text_notification(self, screen, notification, center_x: int, center_y: int):
        """Draw notification using text rendering (fallback method)"""
        # Create surfaces with alpha
        equation_surface = self.equation_font.render(notification['equation'], True, notification['color'])
        description_surface = self.symbol_font.render(notification['description'], True, notification['color'])
        
        # Apply alpha and scaling
        if notification['alpha'] < 255:
            equation_surface.set_alpha(notification['alpha'])
            description_surface.set_alpha(notification['alpha'])
        
        # Scale surfaces
        if notification['scale'] != 1.0:
            eq_width = int(equation_surface.get_width() * notification['scale'])
            eq_height = int(equation_surface.get_height() * notification['scale'])
            desc_width = int(description_surface.get_width() * notification['scale'])
            desc_height = int(description_surface.get_height() * notification['scale'])
            
            if eq_width > 0 and eq_height > 0:
                equation_surface = pygame.transform.scale(equation_surface, (eq_width, eq_height))
            if desc_width > 0 and desc_height > 0:
                description_surface = pygame.transform.scale(description_surface, (desc_width, desc_height))
        
        # Draw glow effect
        glow_intensity = (math.sin(notification['glow_phase']) + 1) * 0.3 + 0.4
        glow_color = tuple(int(c * glow_intensity) for c in notification['color'])
        
        # Create glow surfaces (slightly larger)
        glow_eq = self.equation_font.render(notification['equation'], True, glow_color)
        glow_desc = self.symbol_font.render(notification['description'], True, glow_color)
        
        if notification['alpha'] < 255:
            glow_eq.set_alpha(int(notification['alpha'] * 0.5))
            glow_desc.set_alpha(int(notification['alpha'] * 0.5))
        
        # Position calculations
        eq_rect = equation_surface.get_rect(center=(center_x, center_y - 20))
        desc_rect = description_surface.get_rect(center=(center_x, center_y + 25))
        
        # Draw glow (offset by 2 pixels in each direction)
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx != 0 or dy != 0:  # Don't draw at center
                    screen.blit(glow_eq, (eq_rect.x + dx, eq_rect.y + dy))
                    screen.blit(glow_desc, (desc_rect.x + dx, desc_rect.y + dy))
        
        # Draw main text with quantum shimmer
        self._draw_with_quantum_shimmer(screen, equation_surface, eq_rect, notification)
        self._draw_with_quantum_shimmer(screen, description_surface, desc_rect, notification)
        
        # Draw enhanced quantum effect particles around the text
        self._draw_enhanced_quantum_particles(screen, center_x, center_y, notification)
        
        # Add energy pulse effect
        self._draw_energy_pulse(screen, center_x, center_y, notification)
        
        # Special effect for entanglement (Bell states)
        if notification['effect_type'] == 'entanglement':
            self._draw_entanglement_resonance(screen, center_x, center_y, notification)
    
    def _draw_enhanced_quantum_particles(self, screen, center_x: int, center_y: int, notification):
        """Draw enhanced quantum particles around LaTeX equations"""
        if notification['alpha'] < 100:  # Don't draw particles when fading
            return
        
        # More particles for different effect types
        particle_counts = {
            'entanglement': 12,  # More particles for entanglement
            'superposition': 8,
            'measurement': 6,
            'tunneling': 10
        }
        
        particle_count = particle_counts.get(notification['effect_type'], 8)
        
        for i in range(particle_count):
            # Multiple orbital layers for enhanced effect
            for layer in range(2):
                angle = (notification['glow_phase'] * (2 + layer * 0.5) + i * (2 * math.pi / particle_count))
                base_radius = 90 + layer * 30
                radius = base_radius + math.sin(notification['glow_phase'] * 3 + i + layer) * 25
                
                particle_x = center_x + math.cos(angle) * radius
                particle_y = center_y + math.sin(angle) * radius
                
                # Particle size varies with layer and animation
                size = (3 - layer) + math.sin(notification['glow_phase'] * 4 + i) * 1.5
                
                # Enhanced particle colors with quantum effect
                base_color = notification['color']
                intensity = 0.8 + 0.2 * math.sin(notification['glow_phase'] * 2 + i)
                particle_color = tuple(int(c * intensity) for c in base_color)
                
                # Particle alpha based on notification alpha and layer
                particle_alpha = min(255, int(notification['alpha'] * (0.9 - layer * 0.2)))
                
                # Create particle surface with enhanced glow
                particle_size = int(size * 2)
                if particle_size > 0:
                    particle_surface = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
                    
                    # Draw particle with glow effect
                    glow_color = (*particle_color, int(particle_alpha * 0.3))
                    main_color = (*particle_color, particle_alpha)
                    
                    # Outer glow
                    pygame.draw.circle(particle_surface, glow_color, 
                                     (particle_size, particle_size), particle_size)
                    # Inner bright core
                    pygame.draw.circle(particle_surface, main_color, 
                                     (particle_size, particle_size), max(1, particle_size // 2))
                    
                    screen.blit(particle_surface, (int(particle_x - particle_size), int(particle_y - particle_size)))
    
    def _draw_energy_pulse(self, screen, center_x: int, center_y: int, notification):
        """Draw energy pulse effect around LaTeX equations"""
        if notification['alpha'] < 50:
            return
        
        # Pulsing energy rings
        pulse_phase = notification['glow_phase'] * 2
        
        for ring in range(3):
            ring_radius = 60 + ring * 40 + math.sin(pulse_phase + ring) * 20
            ring_alpha = int(notification['alpha'] * 0.3 * (1 - ring * 0.2))
            
            if ring_alpha > 10:
                # Create ring surface
                ring_surface = pygame.Surface((int(ring_radius * 2 + 10), int(ring_radius * 2 + 10)), pygame.SRCALPHA)
                ring_color = (*notification['color'], ring_alpha)
                
                # Draw pulsing ring
                pygame.draw.circle(ring_surface, ring_color, 
                                 (int(ring_radius + 5), int(ring_radius + 5)), 
                                 int(ring_radius), 2)
                
                ring_rect = ring_surface.get_rect(center=(center_x, center_y))
                screen.blit(ring_surface, ring_rect)
        
        # Add quantum field distortion effect
        self._draw_quantum_field_distortion(screen, center_x, center_y, notification)
    
    def _draw_quantum_field_distortion(self, screen, center_x: int, center_y: int, notification):
        """Draw quantum field distortion effect"""
        if notification['alpha'] < 80:
            return
        
        # Quantum field lines
        field_lines = 6
        for i in range(field_lines):
            angle = (i * 2 * math.pi / field_lines) + notification['glow_phase'] * 0.5
            
            # Field line parameters
            line_length = 40 + math.sin(notification['glow_phase'] * 3 + i) * 15
            line_alpha = int(notification['alpha'] * 0.4)
            
            if line_alpha > 20:
                start_x = center_x + math.cos(angle) * 50
                start_y = center_y + math.sin(angle) * 50
                end_x = center_x + math.cos(angle) * (50 + line_length)
                end_y = center_y + math.sin(angle) * (50 + line_length)
                
                # Create field line surface for alpha blending
                field_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
                field_color = (*notification['color'], line_alpha)
                
                # Draw field line with thickness variation
                thickness = 2 + int(math.sin(notification['glow_phase'] * 4 + i))
                
                # Convert to surface-relative coordinates
                surf_start = (int(start_x - center_x + 100), int(start_y - center_y + 100))
                surf_end = (int(end_x - center_x + 100), int(end_y - center_y + 100))
                
                pygame.draw.line(field_surface, field_color, surf_start, surf_end, thickness)
                
                field_rect = field_surface.get_rect(center=(center_x, center_y))
                screen.blit(field_surface, field_rect)
    
    def _draw_with_quantum_shimmer(self, screen, surface, rect, notification):
        """Draw surface with quantum shimmer effect"""
        # Draw main surface
        screen.blit(surface, rect)
        
        # Add quantum shimmer overlay
        shimmer_intensity = (math.sin(notification['glow_phase'] * 6) + 1) * 0.1 + 0.05
        shimmer_alpha = int(notification['alpha'] * shimmer_intensity)
        
        if shimmer_alpha > 10:
            # Create shimmer surface
            shimmer_surface = surface.copy()
            shimmer_surface.set_alpha(shimmer_alpha)
            
            # Apply color tint for quantum effect
            shimmer_color = notification['color']
            tint_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            tint_surface.fill((*shimmer_color, shimmer_alpha))
            shimmer_surface.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_ADD)
            
            # Draw shimmer with slight offset for depth
            shimmer_offset = int(math.sin(notification['glow_phase'] * 8) * 2)
            shimmer_rect = rect.copy()
            shimmer_rect.x += shimmer_offset
            screen.blit(shimmer_surface, shimmer_rect)
    
    def _draw_entanglement_resonance(self, screen, center_x: int, center_y: int, notification):
        """Draw special entanglement resonance effect for Bell states"""
        if notification['alpha'] < 60:
            return
        
        # Entanglement connection lines (representing quantum correlation)
        resonance_phase = notification['glow_phase'] * 3
        
        # Draw quantum correlation lines
        for i in range(4):  # 4 lines for the 4 Bell states
            angle = (i * math.pi / 2) + resonance_phase * 0.3
            
            # Connection points
            distance = 80 + math.sin(resonance_phase + i) * 20
            x1 = center_x + math.cos(angle) * distance
            y1 = center_y + math.sin(angle) * distance
            x2 = center_x + math.cos(angle + math.pi) * distance
            y2 = center_y + math.sin(angle + math.pi) * distance
            
            # Line properties
            line_alpha = int(notification['alpha'] * 0.5 * (0.5 + 0.5 * math.sin(resonance_phase * 2 + i)))
            line_thickness = 2 + int(math.sin(resonance_phase * 4 + i))
            
            if line_alpha > 20:
                # Create line surface for proper alpha blending
                line_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
                line_color = (*notification['color'], line_alpha)
                
                # Convert to surface coordinates
                surf_x1 = int(x1 - center_x + 150)
                surf_y1 = int(y1 - center_y + 150)
                surf_x2 = int(x2 - center_x + 150)
                surf_y2 = int(y2 - center_y + 150)
                
                # Draw entanglement connection with quantum fluctuation
                pygame.draw.line(line_surface, line_color, 
                               (surf_x1, surf_y1), (surf_x2, surf_y2), line_thickness)
                
                # Add quantum nodes at connection points
                node_size = 3 + int(math.sin(resonance_phase * 5 + i))
                pygame.draw.circle(line_surface, line_color, (surf_x1, surf_y1), node_size)
                pygame.draw.circle(line_surface, line_color, (surf_x2, surf_y2), node_size)
                
                line_rect = line_surface.get_rect(center=(center_x, center_y))
                screen.blit(line_surface, line_rect)
        
        # Add quantum entanglement spiral
        spiral_points = []
        for t in range(0, 360, 10):
            spiral_angle = math.radians(t) + resonance_phase
            spiral_radius = 30 + t * 0.1 + math.sin(resonance_phase * 2 + t * 0.1) * 10
            
            if spiral_radius < 100:  # Keep spiral contained
                spiral_x = center_x + math.cos(spiral_angle) * spiral_radius
                spiral_y = center_y + math.sin(spiral_angle) * spiral_radius
                spiral_points.append((int(spiral_x), int(spiral_y)))
        
        # Draw spiral if we have enough points
        if len(spiral_points) > 3:
            spiral_alpha = int(notification['alpha'] * 0.4)
            if spiral_alpha > 15:
                spiral_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
                spiral_color = (*notification['color'], spiral_alpha)
                
                # Convert points to surface coordinates
                surf_points = [(x - center_x + 150, y - center_y + 150) for x, y in spiral_points]
                
                # Draw spiral lines
                for i in range(len(surf_points) - 1):
                    pygame.draw.line(spiral_surface, spiral_color, surf_points[i], surf_points[i + 1], 2)
                
                spiral_rect = spiral_surface.get_rect(center=(center_x, center_y))
                screen.blit(spiral_surface, spiral_rect)
    
    def clear_all_notifications(self):
        """Clear all active notifications"""
        self.active_notifications.clear()
    
    def has_active_notifications(self) -> bool:
        """Check if there are any active notifications"""
        return len(self.active_notifications) > 0
