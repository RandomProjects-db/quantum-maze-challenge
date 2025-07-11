#!/usr/bin/env python3
"""
Enhanced HUD System with Dedicated Status Area
Clean interface that doesn't interfere with quantum equation displays
"""

import pygame
import math
from typing import List, Optional

class EnhancedHUD:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # HUD Layout Configuration
        self.hud_height = 80  # Dedicated HUD area height
        self.hud_y = screen_height - self.hud_height  # Bottom of screen
        self.game_area_height = screen_height - self.hud_height
        
        # Colors
        self.hud_bg_color = (20, 20, 40, 200)  # Dark blue with transparency
        self.text_color = (255, 255, 255)
        self.accent_color = (100, 200, 255)
        self.warning_color = (255, 100, 100)
        self.success_color = (100, 255, 150)
        self.timer_color = (255, 215, 0)
        
        # Fonts
        self.main_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 36)
        
        # Animation variables
        self.pulse_phase = 0
        self.warning_flash = 0
        
        # Layout sections
        self.sections = {
            'score': {'x': 20, 'width': 150},
            'lives': {'x': 180, 'width': 100},
            'level': {'x': 290, 'width': 100},
            'qubits': {'x': 400, 'width': 120},
            'timers': {'x': 530, 'width': 250}
        }
    
    def get_game_area_height(self) -> int:
        """Return the height available for the game area (excluding HUD)"""
        return self.game_area_height
    
    def update(self, dt: float):
        """Update HUD animations"""
        self.pulse_phase += dt * 3
        self.warning_flash += dt * 8
    
    def draw(self, screen, score: int, lives: int, level: int, qubits_collected: int, 
             total_qubits: int, entanglement_timer: float = 0, superposition_timer: float = 0,
             measurement_timer: float = 0):
        """Draw the complete HUD"""
        
        # Draw HUD background
        hud_surface = pygame.Surface((self.screen_width, self.hud_height), pygame.SRCALPHA)
        pygame.draw.rect(hud_surface, self.hud_bg_color, 
                        (0, 0, self.screen_width, self.hud_height))
        
        # Add subtle border
        pygame.draw.line(hud_surface, self.accent_color, 
                        (0, 0), (self.screen_width, 0), 2)
        
        screen.blit(hud_surface, (0, self.hud_y))
        
        # Draw each section
        self._draw_score_section(screen, score)
        self._draw_lives_section(screen, lives)
        self._draw_level_section(screen, level)
        self._draw_qubits_section(screen, qubits_collected, total_qubits)
        self._draw_timers_section(screen, entanglement_timer, superposition_timer, measurement_timer)
    
    def _draw_score_section(self, screen, score: int):
        """Draw score display"""
        section = self.sections['score']
        x = section['x']
        y = self.hud_y + 15
        
        # Score label
        label = self.small_font.render("SCORE", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Score value with pulsing effect for high scores
        score_color = self.text_color
        if score > 1000:
            pulse = (math.sin(self.pulse_phase) + 1) * 0.2 + 0.8
            score_color = tuple(int(c * pulse) for c in self.success_color)
        
        score_text = self.main_font.render(f"{score:,}", True, score_color)
        screen.blit(score_text, (x, y + 20))
    
    def _draw_lives_section(self, screen, lives: int):
        """Draw lives display with heart symbols"""
        section = self.sections['lives']
        x = section['x']
        y = self.hud_y + 15
        
        # Lives label
        label = self.small_font.render("LIVES", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Heart symbols for lives
        heart_x = x
        heart_y = y + 25
        
        for i in range(max(lives, 0)):
            heart_color = self.success_color
            if lives <= 1:  # Warning color for low lives
                flash = (math.sin(self.warning_flash) + 1) * 0.5
                heart_color = tuple(int(self.warning_color[j] * flash + self.success_color[j] * (1-flash)) 
                                  for j in range(3))
            
            # Draw heart shape (simplified as diamond)
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
        y = self.hud_y + 15
        
        # Level label
        label = self.small_font.render("LEVEL", True, self.accent_color)
        screen.blit(label, (x, y))
        
        # Level value
        level_text = self.main_font.render(str(level), True, self.text_color)
        screen.blit(level_text, (x, y + 20))
    
    def _draw_qubits_section(self, screen, collected: int, total: int):
        """Draw qubits progress"""
        section = self.sections['qubits']
        x = section['x']
        y = self.hud_y + 15
        
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
        screen.blit(progress_surface, (x, y + 20))
        
        # Progress bar
        if total > 0:
            bar_width = 80
            bar_height = 6
            bar_x = x
            bar_y = y + 50
            
            # Background bar
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
            
            # Progress fill
            fill_width = int((collected / total) * bar_width)
            if fill_width > 0:
                pygame.draw.rect(screen, progress_color, (bar_x, bar_y, fill_width, bar_height))
    
    def _draw_timers_section(self, screen, entanglement_timer: float, superposition_timer: float, 
                           measurement_timer: float):
        """Draw active power-up timers"""
        section = self.sections['timers']
        x = section['x']
        y = self.hud_y + 10
        
        timer_y = y
        
        # Entanglement Timer
        if entanglement_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "ENTANGLEMENT", entanglement_timer, 
                                  self.accent_color, 10.0)
            timer_y += 20
        
        # Superposition Timer
        if superposition_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "SUPERPOSITION", superposition_timer,
                                  self.success_color, 8.0)
            timer_y += 20
        
        # Measurement Timer
        if measurement_timer > 0:
            self._draw_single_timer(screen, x, timer_y, "MEASUREMENT", measurement_timer,
                                  self.timer_color, 5.0)
    
    def _draw_single_timer(self, screen, x: int, y: int, label: str, time_left: float, 
                          color: tuple, max_time: float):
        """Draw a single timer with progress bar"""
        # Timer label and time
        label_text = self.small_font.render(f"{label}: {time_left:.1f}s", True, color)
        screen.blit(label_text, (x, y))
        
        # Timer progress bar
        bar_width = 100
        bar_height = 4
        bar_x = x + 120
        bar_y = y + 6
        
        # Background
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
        
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
    
    def draw_game_over_overlay(self, screen, final_score: int, stats_dict: dict):
        """Draw game over screen in the center area (not in HUD)"""
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
        """Draw pause overlay in the center area"""
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
