#!/usr/bin/env python3
"""
Simple Separated HUD - Just adds HUD without breaking anything
"""

import pygame
import math
import random

class SimpleSeparatedHUD:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Simple separation - just reserve space at bottom
        self.hud_height = 100
        self.separator_height = 4
        self.game_area_height = screen_height - self.hud_height - self.separator_height
        self.separator_y = self.game_area_height
        self.hud_start_y = self.separator_y + self.separator_height
        
        # Colors
        self.separator_color = (0, 255, 255)  # Cyan separator
        self.hud_bg_color = (15, 15, 30)
        self.text_color = (255, 255, 255)
        self.accent_color = (0, 255, 255)
        self.success_color = (100, 255, 150)
        self.warning_color = (255, 100, 100)
        self.timer_color = (255, 215, 0)
        self.fact_color = (180, 180, 255)
        
        # Fonts
        self.main_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        self.fact_font = pygame.font.Font(None, 18)
        
        # Animation
        self.pulse_phase = 0
        self.warning_flash = 0
        self.fact_timer = 0
        self.current_fact = 0
        
        # Simple facts
        self.facts = [
            "🌀 Hadamard gates create superposition states",
            "🔗 Entangled qubits affect each other instantly",
            "⚛️ Qubits hold infinite possible states",
            "🚪 CNOT gates create quantum entanglement",
            "📡 Quantum teleportation transfers information",
            "🌊 Superposition enables quantum parallelism",
            "🚫 No-Cloning: Can't copy quantum states",
            "🔐 Shor's algorithm breaks encryption fast",
            "🔍 Grover's algorithm searches in √N time",
            "💨 Decoherence destroys quantum properties"
        ]
    
    def get_game_area_height(self):
        return self.game_area_height
    
    def update(self, dt):
        self.pulse_phase += dt * 3
        self.warning_flash += dt * 8
        self.fact_timer += dt
        if self.fact_timer >= 5.0:
            self.fact_timer = 0
            self.current_fact = (self.current_fact + 1) % len(self.facts)
    
    def draw(self, screen, score, lives, level, qubits_collected, total_qubits, 
             entanglement_timer=0, superposition_timer=0, measurement_timer=0):
        
        # Draw separator
        pygame.draw.rect(screen, self.separator_color, 
                        (0, self.separator_y, self.screen_width, self.separator_height))
        
        # Draw HUD background
        pygame.draw.rect(screen, self.hud_bg_color, 
                        (0, self.hud_start_y, self.screen_width, self.hud_height))
        
        # Draw HUD content
        y = self.hud_start_y + 10
        
        # Score
        score_text = self.main_font.render(f"SCORE: {score:,}", True, self.text_color)
        screen.blit(score_text, (20, y))
        
        # Lives with heart symbols - horizontal layout
        lives_label = self.small_font.render("LIVES:", True, self.text_color)
        screen.blit(lives_label, (180, y))
        
        # Draw hearts horizontally next to the label
        hearts_start_x = 180 + 50  # Start after "LIVES:" text
        for i in range(lives):
            heart_x = hearts_start_x + (i * 20)  # 20 pixels apart horizontally
            heart_y = y + 8  # Align with text baseline
            
            # Draw heart symbol (♥) 
            heart_color = (255, 100, 100)  # Red hearts
            pygame.draw.circle(screen, heart_color, (heart_x, heart_y), 6)
            # Add a smaller inner circle for depth
            pygame.draw.circle(screen, (255, 150, 150), (heart_x, heart_y), 3)
        
        # Level
        level_text = self.main_font.render(f"LEVEL: {level}", True, self.text_color)
        screen.blit(level_text, (280, y))
        
        # Qubits
        qubits_text = self.main_font.render(f"QUBITS: {qubits_collected}/{total_qubits}", True, self.text_color)
        screen.blit(qubits_text, (380, y))
        
        # Timers
        timer_x = 20
        timer_y = y + 30
        
        if entanglement_timer > 0:
            timer_text = self.small_font.render(f"ENTANGLE: {entanglement_timer:.1f}s", True, self.accent_color)
            screen.blit(timer_text, (timer_x, timer_y))
            timer_x += 120
        
        if superposition_timer > 0:
            timer_text = self.small_font.render(f"SUPERPOS: {superposition_timer:.1f}s", True, self.success_color)
            screen.blit(timer_text, (timer_x, timer_y))
            timer_x += 120
        
        if measurement_timer > 0:
            timer_text = self.small_font.render(f"MEASURE: {measurement_timer:.1f}s", True, self.timer_color)
            screen.blit(timer_text, (timer_x, timer_y))
        
        # Did you know fact - moved to bottom row to avoid overlap
        fact_y = timer_y + 25  # Position below timers
        fact_text = self.small_font.render("DID YOU KNOW?", True, self.accent_color)
        screen.blit(fact_text, (20, fact_y))
        
        current_fact_text = self.facts[self.current_fact]
        fact_surface = self.fact_font.render(current_fact_text, True, self.fact_color)
        screen.blit(fact_surface, (20, fact_y + 15))
    
    def draw_pause_overlay(self, screen):
        overlay = pygame.Surface((self.screen_width, self.game_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        
        pause_text = pygame.font.Font(None, 48).render("PAUSED", True, self.accent_color)
        pause_rect = pause_text.get_rect(center=(self.screen_width//2, self.game_area_height//2))
        screen.blit(pause_text, pause_rect)
    
    def draw_level_complete_overlay(self, screen, final_score, stats_dict, level):
        overlay = pygame.Surface((self.screen_width, self.game_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Level Complete title
        level_complete_text = pygame.font.Font(None, 48).render(f"LEVEL {level-1} COMPLETE!", True, self.success_color)
        level_complete_rect = level_complete_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 - 80))
        screen.blit(level_complete_text, level_complete_rect)
        
        # Final score
        score_text = pygame.font.Font(None, 36).render(f"Score: {final_score:,}", True, self.text_color)
        score_rect = score_text.get_rect(center=(self.screen_width//2, self.game_area_height//2 - 40))
        screen.blit(score_text, score_rect)
        
        # Stats
        y_offset = self.game_area_height//2
        for stat_name, stat_value in stats_dict.items():
            stat_text = pygame.font.Font(None, 24).render(f"{stat_name}: {stat_value}", True, self.text_color)
            stat_rect = stat_text.get_rect(center=(self.screen_width//2, y_offset))
            screen.blit(stat_text, stat_rect)
            y_offset += 25
        
        # Next level message
        next_text = pygame.font.Font(None, 24).render("Preparing next level...", True, self.accent_color)
        next_rect = next_text.get_rect(center=(self.screen_width//2, y_offset + 20))
        screen.blit(next_text, next_rect)

    def draw_game_over_overlay(self, screen, final_score, stats_dict, countdown_timer=0):
        overlay = pygame.Surface((self.screen_width, self.game_area_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Game Over title
        game_over_text = pygame.font.Font(None, 48).render("GAME OVER", True, self.warning_color)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width//2, 60))
        screen.blit(game_over_text, game_over_rect)
        
        # Final Score
        score_text = pygame.font.Font(None, 36).render(f"FINAL SCORE: {final_score:,}", True, self.accent_color)
        score_rect = score_text.get_rect(center=(self.screen_width//2, 110))
        screen.blit(score_text, score_rect)
        
        # Detailed Stats in two columns
        left_x = self.screen_width//2 - 150
        right_x = self.screen_width//2 + 50
        y_start = 150
        
        # Left column stats
        left_stats = [
            ('Qubits Collected', stats_dict.get('qubits_collected', 0)),
            ('Ghosts Dodged', stats_dict.get('ghosts_dodged', 0)),
            ('Power-ups Used', stats_dict.get('powerups_used', 0)),
            ('Levels Completed', stats_dict.get('levels_completed', 0)),
        ]
        
        # Right column stats  
        right_stats = [
            ('Teleportations', stats_dict.get('teleportations', 0)),
            ('Entanglements', stats_dict.get('entanglements_completed', 0)),
            ('Deaths', stats_dict.get('deaths', 0)),
            ('Survival Time', f"{stats_dict.get('survival_time', 0):.1f}s"),
        ]
        
        # Draw left column
        for i, (stat_name, stat_value) in enumerate(left_stats):
            stat_text = pygame.font.Font(None, 24).render(f"{stat_name}: {stat_value}", True, self.text_color)
            screen.blit(stat_text, (left_x, y_start + i * 25))
        
        # Draw right column
        for i, (stat_name, stat_value) in enumerate(right_stats):
            stat_text = pygame.font.Font(None, 24).render(f"{stat_name}: {stat_value}", True, self.text_color)
            screen.blit(stat_text, (right_x, y_start + i * 25))
        
        # Performance rating
        if hasattr(stats_dict, 'get') and 'performance_rating' in stats_dict:
            rating_text = pygame.font.Font(None, 28).render(f"Rating: {stats_dict['performance_rating']}", True, self.success_color)
            rating_rect = rating_text.get_rect(center=(self.screen_width//2, y_start + 120))
            screen.blit(rating_text, rating_rect)
        
        # Countdown timer with nanoseconds
        if countdown_timer > 0:
            # Convert to nanoseconds for display
            total_ns = int(countdown_timer * 1_000_000_000)
            seconds = int(countdown_timer)
            nanoseconds = total_ns % 1_000_000_000
            
            countdown_text = pygame.font.Font(None, 24).render(
                f"Returning to menu in: {seconds}.{nanoseconds:09d}s", 
                True, self.timer_color
            )
            countdown_rect = countdown_text.get_rect(center=(self.screen_width//2, y_start + 160))
            screen.blit(countdown_text, countdown_rect)
        
        # Instructions
        instruction_text = pygame.font.Font(None, 20).render("Press SPACE to restart or ESC for menu", True, self.text_color)
        instruction_rect = instruction_text.get_rect(center=(self.screen_width//2, y_start + 190))
        screen.blit(instruction_text, instruction_rect)
