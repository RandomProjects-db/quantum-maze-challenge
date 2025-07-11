import pygame
import math
from typing import Optional, List

class RetroHUD:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Fonts
        self.large_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        
        # Colors
        self.primary_color = (0, 255, 255)      # Cyan
        self.secondary_color = (255, 255, 0)    # Yellow
        self.warning_color = (255, 100, 100)    # Red
        self.success_color = (100, 255, 100)    # Green
        self.background_color = (0, 0, 50, 180) # Semi-transparent dark blue
        
        # Animation states
        self.warning_flash_phase = 0
        self.powerup_glow_phase = 0
        
        # Alert system
        self.proximity_alert_active = False
        self.proximity_alert_intensity = 0
        
    def update(self, dt: float):
        """Update HUD animations"""
        self.warning_flash_phase += dt * 8
        self.powerup_glow_phase += dt * 4
    
    def draw_main_hud(self, screen, score: int, lives: int, level: int, qubits_remaining: int):
        """Draw the main game HUD"""
        # Draw HUD text directly without background panel
        y_offset = 20
        
        # Score
        score_text = self.medium_font.render(f"SCORE: {score:06d}", True, self.primary_color)
        screen.blit(score_text, (20, y_offset))
        y_offset += 25
        
        # Lives with heart symbols
        lives_text = self.small_font.render("LIVES:", True, self.secondary_color)
        screen.blit(lives_text, (20, y_offset))
        
        for i in range(lives):
            heart_x = 70 + i * 15
            self._draw_heart(screen, heart_x, y_offset + 2, self.warning_color)
        y_offset += 20
        
        # Level
        level_text = self.small_font.render(f"LEVEL: {level}", True, self.success_color)
        screen.blit(level_text, (20, y_offset))
        y_offset += 20
        
        # Qubits remaining
        qubits_color = self.secondary_color
        if qubits_remaining <= 5:
            # Flash when few qubits remain
            flash_intensity = (math.sin(self.warning_flash_phase) + 1) * 0.5
            qubits_color = (255, int(255 * flash_intensity), 0)
        
        qubits_text = self.small_font.render(f"QUBITS: {qubits_remaining}", True, qubits_color)
        screen.blit(qubits_text, (20, y_offset))
    
    def draw_powerup_status(self, screen, player):
        """Draw active power-up status"""
        if not (player.has_superposition or player.has_measurement):
            return
        
        # Power-up status panel
        panel_x = self.screen_width - 220
        panel_y = 10
        panel_width = 200
        panel_height = 80
        
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.background_color)
        
        # Glowing border for active power-ups
        glow_intensity = (math.sin(self.powerup_glow_phase) + 1) * 0.5
        border_color = (int(100 + 155 * glow_intensity), 
                       int(100 + 155 * glow_intensity), 255)
        pygame.draw.rect(panel_surface, border_color, panel_surface.get_rect(), 3)
        
        screen.blit(panel_surface, (panel_x, panel_y))
        
        y_offset = panel_y + 15
        
        # Superposition status
        if player.has_superposition:
            time_left = max(0, player.superposition_timer)
            superposition_text = f"SUPERPOSITION: {time_left:.1f}s"
            color = (0, 255, 150)
            
            # Flash when time is running out
            if time_left < 2.0:
                flash_alpha = int(128 + 127 * math.sin(time_left * 10))
                color = (0, flash_alpha, 150)
            
            text_surface = self.small_font.render(superposition_text, True, color)
            screen.blit(text_surface, (panel_x + 10, y_offset))
            
            # Draw progress bar
            bar_width = 180
            bar_height = 6
            bar_x = panel_x + 10
            bar_y = y_offset + 15
            
            # Background bar
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Progress bar
            progress = time_left / 8.0  # Assuming 8 second duration
            progress_width = int(bar_width * progress)
            pygame.draw.rect(screen, color, (bar_x, bar_y, progress_width, bar_height))
            
            y_offset += 30
        
        # Measurement status
        if player.has_measurement:
            time_left = max(0, player.measurement_timer)
            measurement_text = f"MEASUREMENT: {time_left:.1f}s"
            color = (255, 255, 0)
            
            # Flash when time is running out
            if time_left < 2.0:
                flash_alpha = int(128 + 127 * math.sin(time_left * 10))
                color = (255, flash_alpha, 0)
            
            text_surface = self.small_font.render(measurement_text, True, color)
            screen.blit(text_surface, (panel_x + 10, y_offset))
            
            # Draw progress bar
            bar_width = 180
            bar_height = 6
            bar_x = panel_x + 10
            bar_y = y_offset + 15
            
            # Background bar
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Progress bar
            progress = time_left / 5.0  # Assuming 5 second duration
            progress_width = int(bar_width * progress)
            pygame.draw.rect(screen, color, (bar_x, bar_y, progress_width, bar_height))
    
    def draw_proximity_alert(self, screen, player, ghosts):
        """Draw proximity alert when ghosts are near"""
        min_distance = float('inf')
        nearest_ghost = None
        
        # Find nearest ghost
        for ghost in ghosts:
            if not ghost.is_captured and ghost.state.name != 'FRIGHTENED':
                distance = math.sqrt((ghost.x - player.x)**2 + (ghost.y - player.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_ghost = ghost
        
        # Activate alert if ghost is close
        alert_distance = 80
        if min_distance < alert_distance:
            self.proximity_alert_active = True
            self.proximity_alert_intensity = 1.0 - (min_distance / alert_distance)
        else:
            self.proximity_alert_active = False
            self.proximity_alert_intensity = 0
        
        # Draw alert
        if self.proximity_alert_active:
            # Screen edge warning
            alert_alpha = int(self.proximity_alert_intensity * 100 * 
                            (math.sin(self.warning_flash_phase * 2) + 1) * 0.5)
            
            if alert_alpha > 20:
                # Create warning overlay
                warning_surface = pygame.Surface((self.screen_width, self.screen_height), 
                                               pygame.SRCALPHA)
                
                # Draw warning border
                border_thickness = int(5 * self.proximity_alert_intensity)
                warning_color = (255, 0, 0, alert_alpha)
                
                # Top border
                pygame.draw.rect(warning_surface, warning_color, 
                               (0, 0, self.screen_width, border_thickness))
                # Bottom border
                pygame.draw.rect(warning_surface, warning_color, 
                               (0, self.screen_height - border_thickness, 
                                self.screen_width, border_thickness))
                # Left border
                pygame.draw.rect(warning_surface, warning_color, 
                               (0, 0, border_thickness, self.screen_height))
                # Right border
                pygame.draw.rect(warning_surface, warning_color, 
                               (self.screen_width - border_thickness, 0, 
                                border_thickness, self.screen_height))
                
                screen.blit(warning_surface, (0, 0))
            
            # Warning text
            if self.proximity_alert_intensity > 0.7:
                warning_text = "DECOHERENCE DETECTED!"
                text_color = (255, int(100 + 155 * self.proximity_alert_intensity), 100)
                text_surface = self.medium_font.render(warning_text, True, text_color)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, 50))
                
                # Add text shadow
                shadow_surface = self.medium_font.render(warning_text, True, (100, 0, 0))
                screen.blit(shadow_surface, (text_rect.x + 2, text_rect.y + 2))
                screen.blit(text_surface, text_rect)
    
    def draw_entanglement_timer(self, screen, qubit_manager):
        """Draw entanglement timer"""
        qubit_manager.draw_entanglement_timer(screen, self.small_font)
    
    def draw_game_over_stats(self, screen, stats: dict):
        """Draw game over statistics screen"""
        # Background overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Stats panel
        panel_width = 400
        panel_height = 300
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.background_color)
        pygame.draw.rect(panel_surface, self.primary_color, panel_surface.get_rect(), 3)
        
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Title
        title_text = self.large_font.render("QUANTUM DECOHERENCE!", True, self.warning_color)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, panel_y + 40))
        screen.blit(title_text, title_rect)
        
        # Stats
        y_offset = panel_y + 80
        stats_to_show = [
            ("Final Score", f"{stats.get('score', 0):06d}"),
            ("Qubits Collected", str(stats.get('qubits_collected', 0))),
            ("Ghosts Dodged", str(stats.get('ghosts_dodged', 0))),
            ("Power-ups Used", str(stats.get('powerups_used', 0))),
            ("Survival Time", f"{stats.get('survival_time', 0):.1f}s"),
            ("Levels Completed", str(stats.get('levels_completed', 0)))
        ]
        
        for i, (label, value) in enumerate(stats_to_show):
            label_text = self.small_font.render(f"{label}:", True, self.secondary_color)
            value_text = self.small_font.render(value, True, self.primary_color)
            
            screen.blit(label_text, (panel_x + 30, y_offset))
            screen.blit(value_text, (panel_x + 250, y_offset))
            y_offset += 25
        
        # Continue instruction
        continue_text = self.small_font.render("Press SPACE to play again", True, self.success_color)
        continue_rect = continue_text.get_rect(center=(self.screen_width // 2, panel_y + panel_height - 30))
        screen.blit(continue_text, continue_rect)
    
    def _draw_heart(self, screen, x: int, y: int, color: tuple):
        """Draw a small heart symbol"""
        # Simple heart using circles and triangle
        pygame.draw.circle(screen, color, (x + 3, y + 3), 3)
        pygame.draw.circle(screen, color, (x + 7, y + 3), 3)
        
        # Triangle for bottom of heart
        points = [(x + 2, y + 5), (x + 8, y + 5), (x + 5, y + 9)]
        pygame.draw.polygon(screen, color, points)
    
    def draw_level_complete(self, screen, level: int, bonus_points: int):
        """Draw level complete notification"""
        # Background overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Notification panel
        panel_width = 300
        panel_height = 150
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.background_color)
        pygame.draw.rect(panel_surface, self.success_color, panel_surface.get_rect(), 3)
        
        screen.blit(panel_surface, (panel_x, panel_y))
        
        # Text
        level_text = self.large_font.render(f"LEVEL {level} COMPLETE!", True, self.success_color)
        level_rect = level_text.get_rect(center=(self.screen_width // 2, panel_y + 50))
        screen.blit(level_text, level_rect)
        
        if bonus_points > 0:
            bonus_text = self.medium_font.render(f"Bonus: {bonus_points} points", True, self.secondary_color)
            bonus_rect = bonus_text.get_rect(center=(self.screen_width // 2, panel_y + 90))
            screen.blit(bonus_text, bonus_rect)
        
        continue_text = self.small_font.render("Preparing next level...", True, self.primary_color)
        continue_rect = continue_text.get_rect(center=(self.screen_width // 2, panel_y + 120))
        screen.blit(continue_text, continue_rect)
