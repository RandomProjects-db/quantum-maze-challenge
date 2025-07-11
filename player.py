import pygame
import math
from typing import Tuple

class QuantumExplorer:
    def __init__(self, x: int, y: int):
        self.x = float(x)
        self.y = float(y)
        self.radius = 12
        self.speed = 3.0
        
        # Movement state
        self.dx = 0
        self.dy = 0
        self.target_dx = 0
        self.target_dy = 0
        
        # Visual effects
        self.glow_phase = 0
        self.pulse_phase = 0
        
        # Quantum states
        self.has_superposition = False
        self.superposition_timer = 0
        self.has_measurement = False
        self.measurement_timer = 0
        
        # Colors
        self.base_color = (0, 150, 255)  # Quantum blue
        self.glow_color = (100, 200, 255)
        self.superposition_color = (0, 255, 150)
        
    def handle_input(self, keys):
        """Handle keyboard input for movement"""
        self.target_dx = 0
        self.target_dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.target_dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.target_dx = 1
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.target_dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.target_dy = 1
    
    def update(self, dt: float, maze=None):
        """Update player position and state"""
        # Smooth movement interpolation with faster response
        self.dx += (self.target_dx - self.dx) * 0.3
        self.dy += (self.target_dy - self.dy) * 0.3
        
        # Calculate movement step
        move_x = self.dx * self.speed * dt * 60
        move_y = self.dy * self.speed * dt * 60
        
        # Store old position
        old_x, old_y = self.x, self.y
        
        # Try to move in both directions
        new_x = self.x + move_x
        new_y = self.y + move_y
        
        if maze:
            # Check if we can move to the new position
            if not maze.is_wall_at(new_x, new_y, self.has_superposition):
                # Free movement
                self.x, self.y = new_x, new_y
            else:
                # Try horizontal movement only
                if move_x != 0 and not maze.is_wall_at(new_x, old_y, self.has_superposition):
                    self.x = new_x
                    # Try to slide along walls
                    slide_amount = 3
                    if move_y > 0 and not maze.is_wall_at(new_x, old_y + slide_amount, self.has_superposition):
                        self.y = old_y + slide_amount * 0.3
                    elif move_y < 0 and not maze.is_wall_at(new_x, old_y - slide_amount, self.has_superposition):
                        self.y = old_y - slide_amount * 0.3
                
                # Try vertical movement only
                elif move_y != 0 and not maze.is_wall_at(old_x, new_y, self.has_superposition):
                    self.y = new_y
                    # Try to slide along walls
                    slide_amount = 3
                    if move_x > 0 and not maze.is_wall_at(old_x + slide_amount, new_y, self.has_superposition):
                        self.x = old_x + slide_amount * 0.3
                    elif move_x < 0 and not maze.is_wall_at(old_x - slide_amount, new_y, self.has_superposition):
                        self.x = old_x - slide_amount * 0.3
                
                # If we can't move, reduce momentum to prevent sticking
                else:
                    self.dx *= 0.8
                    self.dy *= 0.8
        else:
            # Fallback: keep player within screen bounds
            if 20 <= new_x <= 780:
                self.x = new_x
            if 20 <= new_y <= 580:
                self.y = new_y
            
        # Update visual effects
        self.glow_phase += dt * 3
        self.pulse_phase += dt * 5
        
        # Update quantum power-up timers
        if self.has_superposition:
            self.superposition_timer -= dt
            if self.superposition_timer <= 0:
                self.has_superposition = False
                
        if self.has_measurement:
            self.measurement_timer -= dt
            if self.measurement_timer <= 0:
                self.has_measurement = False
    
    def activate_superposition(self, duration: float = 5.0):
        """Activate superposition power-up"""
        self.has_superposition = True
        self.superposition_timer = duration
        
    def activate_measurement(self, duration: float = 3.0):
        """Activate measurement power-up"""
        self.has_measurement = True
        self.measurement_timer = duration
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle for the player"""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, screen):
        """Draw the Quantum Explorer with quantum effects"""
        # Calculate dynamic colors and sizes
        glow_intensity = (math.sin(self.glow_phase) + 1) * 0.5
        pulse_size = 1 + math.sin(self.pulse_phase) * 0.1
        
        # Determine current color based on quantum state
        if self.has_superposition:
            current_color = self.superposition_color
            # Add flickering effect for superposition
            if int(self.superposition_timer * 10) % 2:
                current_color = tuple(min(255, c + 50) for c in current_color)
        else:
            current_color = self.base_color
            
        # Draw outer glow
        glow_radius = int(self.radius * pulse_size * 1.8)
        glow_alpha = int(glow_intensity * 100)
        
        # Create glow surface
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        glow_color_with_alpha = (*self.glow_color, glow_alpha)
        
        # Draw multiple glow layers for better effect
        for i in range(3):
            alpha = glow_alpha // (i + 1)
            radius = glow_radius - i * 3
            if radius > 0:
                pygame.draw.circle(
                    glow_surface,
                    (*self.glow_color, alpha),
                    (glow_radius, glow_radius),
                    radius
                )
        
        # Blit glow to screen
        screen.blit(
            glow_surface,
            (self.x - glow_radius, self.y - glow_radius),
            special_flags=pygame.BLEND_ADD
        )
        
        # Draw main body
        main_radius = int(self.radius * pulse_size)
        pygame.draw.circle(screen, current_color, (int(self.x), int(self.y)), main_radius)
        
        # Draw inner core
        core_radius = max(1, int(main_radius * 0.6))
        core_color = tuple(min(255, c + 80) for c in current_color)
        pygame.draw.circle(screen, core_color, (int(self.x), int(self.y)), core_radius)
        
        # Draw quantum state indicators
        if self.has_measurement:
            # Draw measurement indicator (pulsing ring)
            ring_radius = int(main_radius * 1.5)
            ring_thickness = 2
            measurement_color = (255, 255, 0)  # Yellow for measurement
            pygame.draw.circle(screen, measurement_color, (int(self.x), int(self.y)), ring_radius, ring_thickness)
            
        # Draw direction indicator
        if abs(self.dx) > 0.1 or abs(self.dy) > 0.1:
            # Small arrow showing movement direction
            arrow_length = 15
            end_x = self.x + self.dx * arrow_length
            end_y = self.y + self.dy * arrow_length
            
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (int(self.x), int(self.y)),
                (int(end_x), int(end_y)),
                2
            )
    
    def draw_ui_indicators(self, screen, font):
        """Draw power-up status indicators"""
        y_offset = 100
        
        if self.has_superposition:
            time_left = max(0, self.superposition_timer)
            text = font.render(f"Superposition: {time_left:.1f}s", True, self.superposition_color)
            screen.blit(text, (10, y_offset))
            y_offset += 25
            
        if self.has_measurement:
            time_left = max(0, self.measurement_timer)
            text = font.render(f"Measurement: {time_left:.1f}s", True, (255, 255, 0))
            screen.blit(text, (10, y_offset))
