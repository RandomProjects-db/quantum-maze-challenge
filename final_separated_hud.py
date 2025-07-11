#!/usr/bin/env python3
"""
Final Separated HUD System
Absolute separation with clear visual boundaries
"""

import pygame
import math
import random
from typing import List, Optional

class FinalSeparatedHUD:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # ABSOLUTE separation configuration
        self.hud_height = 120  # HUD banner height
        self.separator_height = 8  # Very thick separator for clear division
        self.total_hud_space = self.hud_height + self.separator_height
        
        # Game area is COMPLETELY separate - no overlap possible
        self.game_area_height = screen_height - self.total_hud_space
        self.separator_y = self.game_area_height
        self.hud_start_y = self.separator_y + self.separator_height
        
        print(f"🎮 Game Area: 0 to {self.game_area_height} pixels")
        print(f"🔸 Separator: {self.separator_y} to {self.separator_y + self.separator_height} pixels")
        print(f"📊 HUD Area: {self.hud_start_y} to {screen_height} pixels")
        
        # Colors with high contrast for clear separation
        self.game_bg_color = (0, 0, 0)  # Pure black for game area
        self.separator_color = (255, 0, 255)  # Bright magenta separator - impossible to miss!
        self.hud_bg_color = (20, 20, 50)  # Dark blue for HUD
        self.text_color = (255, 255, 255)
        self.accent_color = (0, 255, 255)
        self.warning_color = (255, 100, 100)
        self.success_color = (100, 255, 150)
        self.timer_color = (255, 215, 0)
        self.fact_color = (180, 180, 255)
        
        # Fonts
        self.main_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 36)
        self.fact_font = pygame.font.Font(None, 18)
        
        # Animation variables
        self.pulse_phase = 0
        self.warning_flash = 0
        self.fact_change_timer = 0
        self.current_fact_index = 0
        
        # Short quantum facts for static display
        self.quantum_facts = [
            "🌀 Hadamard gates create superposition states",
            "🔗 Entangled qubits affect each other instantly",
            "⚛️ Qubits hold infinite possible states",
            "🚪 CNOT gates create quantum entanglement",
            "📡 Quantum teleportation transfers information",
            "🌊 Superposition enables quantum parallelism",
            "🚫 No-Cloning: Can't copy quantum states",
            "🔐 Shor's algorithm breaks encryption fast",
            "🔍 Grover's algorithm searches in √N time",
            "💨 Decoherence destroys quantum properties",
            "📏 Measurement collapses wave functions",
            "🔬 Qubits: photons, ions, circuits, diamonds",
            "🌐 Bloch Sphere visualizes qubit states",
            "🔄 Quantum gates are reversible operations",
            "🔔 Bell states are maximally entangled",
            "🏆 Quantum supremacy beats classical",
            "🤝 Quantum solves different problems",
            "❓ Uncertainty limits measurements",
            "👁️ Observation changes quantum systems",
            "🌊 Tunneling crosses impossible barriers"
        ]
        
        # Layout sections
        self.sections = {
            'score': {'x': 20, 'width': 100},
            'lives': {'x': 130, 'width': 80},
            'level': {'x': 220, 'width': 60},
            'qubits': {'x': 290, 'width': 100},
            'timers': {'x': 400, 'width': 180},
            'facts': {'x': 590, 'width': 390}
        }
    
    def get_game_area_height(self) -> int:
        """Return the height available for the game area"""
        return self.game_area_height
    
    def get_separator_y(self) -> int:
        """Return Y position of the separator"""
        return self.separator_y
    
    def update(self, dt: float):
        """Update HUD animations and fact rotation"""
        self.pulse_phase += dt * 3
        self.warning_flash += dt * 8
        
        # Update fact rotation
        self.fact_change_timer += dt
        if self.fact_change_timer >= 5.0:  # Change every 5 seconds
            self.fact_change_timer = 0
            self.current_fact_index = (self.current_fact_index + 1) % len(self.quantum_facts)
    
    def draw(self, screen, score: int, lives: int, level: int, qubits_collected: int, 
             total_qubits: int, entanglement_timer: float = 0, superposition_timer: float = 0,
             measurement_timer: float = 0):
        """Draw the absolutely separated HUD"""
        
        # FIRST: Fill game area with black (to show clear separation)
        pygame.draw.rect(screen, self.game_bg_color, 
                        (0, 0, self.screen_width, self.game_area_height))
        
        # SECOND: Draw VERY visible separator
        pygame.draw.rect(screen, self.separator_color, 
                        (0, self.separator_y, self.screen_width, self.separator_height))
        
        # THIRD: Draw HUD background (completely separate area)
        pygame.draw.rect(screen, self.hud_bg_color, 
                        (0, self.hud_start_y, self.screen_width, self.hud_height))
        
        # Add border around HUD for extra clarity
        pygame.draw.rect(screen, self.accent_color, 
                        (0, self.hud_start_y, self.screen_width, self.hud_height), 2)
        
        # Draw all HUD sections
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
        y = self.hud_start_y + 15
        
        label = self.small_font.render("SCORE", True, self.accent_color)
        screen.blit(label, (x, y))
        
        score_color = self.text_color
        if score > 1000:
            pulse = (math.sin(self.pulse_phase) + 1) * 0.2 + 0.8
            score_color = tuple(int(c * pulse) for c in self.success_color)
        
        score_text = self.main_font.render(f"{score:,}", True, score_color)
        screen.blit(score_text, (x, y + 25))
    
    def _draw_lives_section(self, screen, lives: int):
        """Draw lives display"""
        section = self.sections['lives']
        x = section['x']
        y = self.hud_start_y + 15
        
        label = self.small_font.render("LIVES", True, self.accent_color)
        screen.blit(label, (x, y))
        
        heart_x = x
        heart_y = y + 30
        
        for i in range(max(lives, 0)):
            heart_color = self.success_color
            if lives <= 1:
                flash = (math.sin(self.warning_flash) + 1) * 0.5
                heart_color = tuple(int(self.warning_color[j] * flash + self.success_color[j] * (1-flash)) 
                                  for j in range(3))
            
            heart_points = [
                (heart_x + 4, heart_y + 2),
                (heart_x + 8, heart_y + 6),
                (heart_x + 4, heart_y + 10),
                (heart_x, heart_y + 6)
            ]
            pygame.draw.polygon(screen, heart_color, heart_points)
            heart_x += 15
    
    def _draw_level_section(self, screen, level: int):
        """Draw level display"""
        section = self.sections['level']
        x = section['x']
        y = self.hud_start_y + 15
        
        label = self.small_font.render("LEVEL", True, self.accent_color)
        screen.blit(label, (x, y))
        
        level_text = self.main_font.render(str(level), True, self.text_color)
        screen.blit(level_text, (x, y + 25))
    
    def _draw_qubits_section(self, screen, collected: int, total: int):
        """Draw qubits progress"""
        section = self.sections['qubits']
        x = section['x']
        y = self.hud_start_y + 15
        
        label = self.small_font.render("QUBITS", True, self.accent_color)
        screen.blit(label, (x, y))
        
        progress_text = f"{collected}/{total}"
        progress_color = self.text_color
        
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
            bar_y = y + 55
            
            pygame.draw.rect(screen, (40, 40, 60), (bar_x, bar_y, bar_width, bar_height))
            
            fill_width = int((collected / total) * bar_width)
            if fill_width > 0:
                pygame.draw.rect(screen, progress_color, (bar_x, bar_y, fill_width, bar_height))
    
    def _draw_timers_section(self, screen, entanglement_timer: float, superposition_timer: float, 
                           measurement_timer: float):
        """Draw active power-up timers"""
        section = self.sections['timers']
        x = section['x']
        y = self.hud_start_y + 10
        
        timer_y = y
        
        if entanglement_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "ENTANGLE", entanglement_timer, 
                                  self.accent_color, 10.0)
            timer_y += 25
        
        if superposition_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "SUPERPOS", superposition_timer,
                                  self.success_color, 8.0)
            timer_y += 25
        
        if measurement_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "MEASURE", measurement_timer,
                                  self.timer_color, 5.0)
    
    def _draw_single_timer(self, screen, x: int, y: int, label: str, time_left: float, 
                          color: tuple, max_time: float):
        """Draw a single timer"""
        label_text = self.small_font.render(f"{label}: {time_left:.1f}s", True, color)
        screen.blit(label_text, (x, y))
        
        bar_width = 70
        bar_height = 6
        bar_x = x + 100
        bar_y = y + 4
        
        pygame.draw.rect(screen, (30, 30, 40), (bar_x, bar_y, bar_width, bar_height))
        
        progress = min(time_left / max_time, 1.0)
        fill_width = int(progress * bar_width)
        
        if progress > 0.5:
            fill_color = color
        elif progress > 0.2:
            blend = (0.5 - progress) / 0.3
            fill_color = tuple(int(color[i] * (1-blend) + self.warning_color[i] * blend) 
                             for i in range(3))
        else:
            flash = (math.sin(self.warning_flash) + 1) * 0.5
            fill_color = tuple(int(self.warning_color[i] * flash + color[i] * (1-flash)) 
                             for i in range(3))
        
        if fill_width > 0:
            pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height))
    
    def _draw_facts_section(self, screen):
        """Draw quantum facts"""
        section = self.sections['facts']
        x = section['x']
        y = self.hud_start_y + 15
        
        label = self.small_font.render("DID YOU KNOW?", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Current fact
        current_fact = self.quantum_facts[self.current_fact_index]
        
        # Word wrap
        words = current_fact.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_surface = self.fact_font.render(test_line, True, self.fact_color)
            
            if test_surface.get_width() <= section['width']:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        line_y = y + 30
        for line in lines[:3]:  # Max 3 lines
            line_surface = self.fact_font.render(line, True, self.fact_color)
            screen.blit(line_surface, (x, line_y))
            line_y += 20
        
        # Progress indicator
        progress = self.fact_change_timer / 5.0
        progress_width = int(section['width'] * progress)
        if progress_width > 0:
            pygame.draw.rect(screen, self.accent_color, 
                           (x, self.hud_start_y + 95, progress_width, 3))
    
    def draw_game_over_overlay(self, screen, final_score: int, stats_dict: dict):
        """Draw game over screen in game area only"""
        overlay = pygame.Surface((self.screen_width, self.game_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        game_over_text = self.large_font.render("QUANTUM GAME OVER", True, self.warning_color)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 - 100))
        screen.blit(game_over_text, game_over_rect)
        
        score_text = self.main_font.render(f"Final Score: {final_score:,}", True, self.text_color)
        score_rect = score_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 - 60))
        screen.blit(score_text, score_rect)
        
        y_offset = self.game_area_height//2 - 20
        for key, value in stats_dict.items():
            stat_text = self.small_font.render(f"{key}: {value}", True, self.accent_color)
            stat_rect = stat_text.get_rect(center=(self.screen_width//2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 25
        
        continue_text = self.small_font.render("Press SPACE to continue", True, self.success_color)
        continue_rect = continue_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 + 80))
        screen.blit(continue_text, continue_rect)
    
    def draw_pause_overlay(self, screen):
        """Draw pause overlay in game area only"""
        overlay = pygame.Surface((self.screen_width, self.game_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        
        pause_text = self.large_font.render("QUANTUM PAUSED", True, self.accent_color)
        pause_rect = pause_text.get_rect(center=(self.screen_width//2, self.game_area_height//2))
        screen.blit(pause_text, pause_rect)
        
        continue_text = self.small_font.render("Press ESC to resume", True, self.text_color)
        continue_rect = continue_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 + 40))
        screen.blit(continue_text, continue_rect)
