#!/usr/bin/env python3
"""
Separated Banner HUD System
Complete separation from game area with educational content
"""

import pygame
import math
import random
import time
from typing import List, Optional

class SeparatedHUD:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Banner Configuration
        self.banner_height = 120  # Taller banner for more content
        self.banner_y = screen_height - self.banner_height  # Bottom banner
        self.game_area_height = screen_height - self.banner_height
        
        # Separator line
        self.separator_height = 3
        self.separator_y = self.banner_y - self.separator_height
        
        # Colors
        self.banner_bg_color = (15, 15, 35, 240)  # Darker banner background
        self.separator_color = (100, 200, 255)  # Bright cyan separator
        self.text_color = (255, 255, 255)
        self.accent_color = (100, 200, 255)
        self.warning_color = (255, 100, 100)
        self.success_color = (100, 255, 150)
        self.timer_color = (255, 215, 0)
        self.fact_color = (200, 200, 255)  # Light purple for facts
        
        # Fonts
        self.main_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 22)
        self.large_font = pygame.font.Font(None, 40)
        self.fact_font = pygame.font.Font(None, 20)
        
        # Animation variables
        self.pulse_phase = 0
        self.warning_flash = 0
        self.fact_scroll_x = 0
        self.fact_change_timer = 0
        self.current_fact_index = 0
        
        # Educational facts
        self.quantum_facts = [
            "🌀 Hadamard gates place qubits into superposition, allowing them to be in both |0⟩ and |1⟩ states simultaneously",
            "🔗 Entangled qubits can influence each other instantaneously, no matter how far apart — Einstein's 'spooky action at a distance'",
            "⚛️ A single qubit holds an infinite range of possible states, not just 0 or 1 like classical bits",
            "🚪 The CNOT gate (Controlled-NOT) is crucial for creating entanglement between qubits",
            "📡 Quantum teleportation transfers information using entangled pairs, not actual particle movement",
            "🌊 Superposition allows quantum computers to evaluate many solutions at once, vastly outperforming classical computers",
            "🚫 The No-Cloning Theorem: It's impossible to make an exact copy of an unknown quantum state",
            "🔐 Shor's algorithm can factor large numbers exponentially faster, threatening traditional encryption",
            "🔍 Grover's algorithm searches unsorted databases in √N time — much faster than classical methods",
            "💨 Quantum decoherence is the main challenge — quantum systems lose their 'quantumness' due to environment interaction",
            "📏 Measurement causes wavefunction collapse — the state 'chooses' an outcome probabilistically",
            "🔬 Qubits can be made using photons, trapped ions, superconducting circuits, or diamond vacancies",
            "🌐 The Bloch Sphere visualizes a qubit's state on a sphere surface — not just 0 or 1!",
            "🔄 Quantum gates are reversible — unlike classical logic gates which lose information",
            "🔔 Bell states are maximally entangled two-qubit states, foundation for quantum protocols",
            "🏆 Quantum supremacy: when quantum computers perform tasks no classical computer can do feasibly",
            "🤝 Quantum computers don't replace classical ones — they solve different problem types",
            "❓ Uncertainty principle: You can't know exact position and momentum simultaneously",
            "👁️ Measuring a quantum system changes it — the observer determines outcomes",
            "🌊 Quantum tunneling lets particles pass through 'impossible' barriers — used in transistors and fusion",
            "📐 Learn linear algebra: vectors, matrices, tensor products are quantum computing foundations",
            "📝 Master Dirac notation: |ψ⟩, ⟨ψ|, and quantum state representation",
            "💻 Try IBM Quantum Experience to run real quantum computers online",
            "🛠️ Practice with Qiskit or Cirq simulators to build quantum circuits",
            "🎯 'If you think you understand quantum mechanics, you don't' — Richard Feynman",
            "🌌 'Everything real is made of things that cannot be regarded as real' — Niels Bohr",
            "✨ 'The universe is stranger than we can imagine' — J.B.S. Haldane",
            "🎲 Quantum randomness is truly random — not just unpredictable like classical chaos",
            "🔮 Quantum computers use probability amplitudes, not just probabilities",
            "🌈 Quantum interference can make wrong answers cancel out, leaving only correct ones"
        ]
        
        # Layout sections for banner
        self.sections = {
            'score': {'x': 20, 'width': 120},
            'lives': {'x': 150, 'width': 80},
            'level': {'x': 240, 'width': 80},
            'qubits': {'x': 330, 'width': 120},
            'timers': {'x': 460, 'width': 200},
            'facts': {'x': 670, 'width': 330}  # Right side for scrolling facts
        }
    
    def get_game_area_height(self) -> int:
        """Return the height available for the game area (excluding banner)"""
        return self.game_area_height
    
    def get_separator_y(self) -> int:
        """Return Y position of the separator line"""
        return self.separator_y
    
    def update(self, dt: float):
        """Update HUD animations and fact rotation"""
        self.pulse_phase += dt * 3
        self.warning_flash += dt * 8
        
        # Update fact rotation
        self.fact_change_timer += dt
        if self.fact_change_timer >= 8.0:  # Change fact every 8 seconds
            self.fact_change_timer = 0
            self.current_fact_index = (self.current_fact_index + 1) % len(self.quantum_facts)
            self.fact_scroll_x = 0  # Reset scroll position
        
        # Scroll fact text if it's too long
        current_fact = self.quantum_facts[self.current_fact_index]
        fact_surface = self.fact_font.render(current_fact, True, self.fact_color)
        if fact_surface.get_width() > self.sections['facts']['width']:
            self.fact_scroll_x += dt * 50  # Scroll speed
            if self.fact_scroll_x > fact_surface.get_width() + 50:
                self.fact_scroll_x = -self.sections['facts']['width']
    
    def draw(self, screen, score: int, lives: int, level: int, qubits_collected: int, 
             total_qubits: int, entanglement_timer: float = 0, superposition_timer: float = 0,
             measurement_timer: float = 0):
        """Draw the separated banner HUD"""
        
        # Draw separator line
        pygame.draw.rect(screen, self.separator_color, 
                        (0, self.separator_y, self.screen_width, self.separator_height))
        
        # Draw banner background
        banner_surface = pygame.Surface((self.screen_width, self.banner_height), pygame.SRCALPHA)
        pygame.draw.rect(banner_surface, self.banner_bg_color, 
                        (0, 0, self.screen_width, self.banner_height))
        
        # Add subtle gradient effect
        for i in range(self.banner_height):
            alpha = int(240 * (1 - i / self.banner_height * 0.3))
            color = (15, 15, 35, alpha)
            pygame.draw.line(banner_surface, color, (0, i), (self.screen_width, i))
        
        screen.blit(banner_surface, (0, self.banner_y))
        
        # Draw all sections
        self._draw_score_section(screen, score)
        self._draw_lives_section(screen, lives)
        self._draw_level_section(screen, level)
        self._draw_qubits_section(screen, qubits_collected, total_qubits)
        self._draw_timers_section(screen, entanglement_timer, superposition_timer, measurement_timer)
        self._draw_facts_section(screen)
    
    def _draw_score_section(self, screen, score: int):
        """Draw score display"""
        section = self.sections['score']
        x = section['x']
        y = self.banner_y + 15
        
        # Score label
        label = self.small_font.render("SCORE", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Score value with pulsing effect for high scores
        score_color = self.text_color
        if score > 1000:
            pulse = (math.sin(self.pulse_phase) + 1) * 0.2 + 0.8
            score_color = tuple(int(c * pulse) for c in self.success_color)
        
        score_text = self.main_font.render(f"{score:,}", True, score_color)
        screen.blit(score_text, (x, y + 25))
    
    def _draw_lives_section(self, screen, lives: int):
        """Draw lives display with heart symbols"""
        section = self.sections['lives']
        x = section['x']
        y = self.banner_y + 15
        
        # Lives label
        label = self.small_font.render("LIVES", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Heart symbols for lives
        heart_x = x
        heart_y = y + 30
        
        for i in range(max(lives, 0)):
            heart_color = self.success_color
            if lives <= 1:  # Warning color for low lives
                flash = (math.sin(self.warning_flash) + 1) * 0.5
                heart_color = tuple(int(self.warning_color[j] * flash + self.success_color[j] * (1-flash)) 
                                  for j in range(3))
            
            # Draw heart shape
            heart_points = [
                (heart_x + 6, heart_y + 2),
                (heart_x + 12, heart_y + 8),
                (heart_x + 6, heart_y + 14),
                (heart_x, heart_y + 8)
            ]
            pygame.draw.polygon(screen, heart_color, heart_points)
            heart_x += 18
    
    def _draw_level_section(self, screen, level: int):
        """Draw level display"""
        section = self.sections['level']
        x = section['x']
        y = self.banner_y + 15
        
        # Level label
        label = self.small_font.render("LEVEL", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Level value
        level_text = self.main_font.render(str(level), True, self.text_color)
        screen.blit(level_text, (x, y + 25))
    
    def _draw_qubits_section(self, screen, collected: int, total: int):
        """Draw qubits progress"""
        section = self.sections['qubits']
        x = section['x']
        y = self.banner_y + 15
        
        # Qubits label
        label = self.small_font.render("QUBITS", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Progress text
        progress_text = f"{collected}/{total}"
        progress_color = self.text_color
        
        # Change color based on progress
        if total > 0:
            progress_ratio = collected / total
            if progress_ratio >= 1.0:
                progress_color = self.success_color
            elif progress_ratio >= 0.8:
                progress_color = self.timer_color
        
        progress_surface = self.main_font.render(progress_text, True, progress_color)
        screen.blit(progress_surface, (x, y + 25))
        
        # Progress bar
        if total > 0:
            bar_width = 80
            bar_height = 8
            bar_x = x
            bar_y = y + 60
            
            # Background bar
            pygame.draw.rect(screen, (40, 40, 60), (bar_x, bar_y, bar_width, bar_height))
            
            # Progress fill
            fill_width = int((collected / total) * bar_width)
            if fill_width > 0:
                pygame.draw.rect(screen, progress_color, (bar_x, bar_y, fill_width, bar_height))
    
    def _draw_timers_section(self, screen, entanglement_timer: float, superposition_timer: float, 
                           measurement_timer: float):
        """Draw active power-up timers"""
        section = self.sections['timers']
        x = section['x']
        y = self.banner_y + 10
        
        timer_y = y
        
        # Entanglement Timer
        if entanglement_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "ENTANGLE", entanglement_timer, 
                                  self.accent_color, 10.0)
            timer_y += 25
        
        # Superposition Timer
        if superposition_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "SUPERPOS", superposition_timer,
                                  self.success_color, 8.0)
            timer_y += 25
        
        # Measurement Timer
        if measurement_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "MEASURE", measurement_timer,
                                  self.timer_color, 5.0)
    
    def _draw_single_timer(self, screen, x: int, y: int, label: str, time_left: float, 
                          color: tuple, max_time: float):
        """Draw a single timer with progress bar"""
        # Timer label and time
        label_text = self.small_font.render(f"{label}: {time_left:.1f}s", True, color)
        screen.blit(label_text, (x, y))
        
        # Timer progress bar
        bar_width = 80
        bar_height = 6
        bar_x = x + 110
        bar_y = y + 4
        
        # Background
        pygame.draw.rect(screen, (30, 30, 40), (bar_x, bar_y, bar_width, bar_height))
        
        # Progress fill
        progress = min(time_left / max_time, 1.0)
        fill_width = int(progress * bar_width)
        
        # Color changes as timer runs out
        if progress > 0.5:
            fill_color = color
        elif progress > 0.2:
            # Blend to warning color
            blend = (0.5 - progress) / 0.3
            fill_color = tuple(int(color[i] * (1-blend) + self.warning_color[i] * blend) 
                             for i in range(3))
        else:
            # Flash warning
            flash = (math.sin(self.warning_flash) + 1) * 0.5
            fill_color = tuple(int(self.warning_color[i] * flash + color[i] * (1-flash)) 
                             for i in range(3))
        
        if fill_width > 0:
            pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height))
    
    def _draw_facts_section(self, screen, ):
        """Draw rotating quantum facts"""
        section = self.sections['facts']
        x = section['x']
        y = self.banner_y + 15
        
        # Facts label
        label = self.small_font.render("DID YOU KNOW?", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Current fact with scrolling
        current_fact = self.quantum_facts[self.current_fact_index]
        fact_surface = self.fact_font.render(current_fact, True, self.fact_color)
        
        # Create clipping area for scrolling text
        clip_rect = pygame.Rect(x, y + 25, section['width'], 60)
        screen.set_clip(clip_rect)
        
        # Draw scrolling text
        text_x = x - int(self.fact_scroll_x)
        screen.blit(fact_surface, (text_x, y + 30))
        
        # If text is scrolling, also draw it again for seamless loop
        if self.fact_scroll_x > 0:
            screen.blit(fact_surface, (text_x + fact_surface.get_width() + 50, y + 30))
        
        # Remove clipping
        screen.set_clip(None)
        
        # Progress indicator for fact rotation
        progress = self.fact_change_timer / 8.0
        progress_width = int(section['width'] * progress)
        if progress_width > 0:
            pygame.draw.rect(screen, self.accent_color, 
                           (x, y + 95, progress_width, 2))
    
    def draw_game_over_overlay(self, screen, final_score: int, stats_dict: dict):
        """Draw game over screen in the game area only"""
        # Semi-transparent overlay over game area only
        overlay = pygame.Surface((self.screen_width, self.game_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.large_font.render("QUANTUM GAME OVER", True, self.warning_color)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 - 100))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.main_font.render(f"Final Score: {final_score:,}", True, self.text_color)
        score_rect = score_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 - 60))
        screen.blit(score_text, score_rect)
        
        # Stats
        y_offset = self.game_area_height//2 - 20
        for key, value in stats_dict.items():
            stat_text = self.small_font.render(f"{key}: {value}", True, self.accent_color)
            stat_rect = stat_text.get_rect(center=(self.screen_width//2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 25
        
        # Continue instruction
        continue_text = self.small_font.render("Press SPACE to continue", True, self.success_color)
        continue_rect = continue_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 + 80))
        screen.blit(continue_text, continue_rect)
    
    def draw_pause_overlay(self, screen):
        """Draw pause overlay in the game area only"""
        # Semi-transparent overlay over game area only
        overlay = pygame.Surface((self.screen_width, self.game_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.large_font.render("QUANTUM PAUSED", True, self.accent_color)
        pause_rect = pause_text.get_rect(center=(self.screen_width//2, self.game_area_height//2))
        screen.blit(pause_text, pause_rect)
        
        # Continue instruction
        continue_text = self.small_font.render("Press ESC to resume", True, self.text_color)
        continue_rect = continue_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 + 40))
        screen.blit(continue_text, continue_rect)
