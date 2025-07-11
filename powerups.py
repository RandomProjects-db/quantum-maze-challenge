import pygame
import math
import random
from typing import List, Tuple
from enum import Enum
from maze import CellType

class PowerUpType(Enum):
    SUPERPOSITION = 1
    MEASUREMENT = 2
    ENTANGLEMENT = 3

class PowerUp:
    def __init__(self, x: int, y: int, power_type: PowerUpType):
        self.x = float(x)
        self.y = float(y)
        self.power_type = power_type
        self.radius = 8
        self.collected = False
        
        # Visual effects
        self.rotation = 0
        self.pulse_phase = random.random() * math.pi * 2
        self.orbit_phase = random.random() * math.pi * 2
        self.energy_phase = random.random() * math.pi * 2
        
        # Power-up specific properties
        if power_type == PowerUpType.SUPERPOSITION:
            self.color = (0, 255, 150)  # Green
            self.glow_color = (100, 255, 200)
            self.duration = 8.0
            self.points = 50
        elif power_type == PowerUpType.MEASUREMENT:
            self.color = (255, 255, 0)  # Yellow
            self.glow_color = (255, 255, 150)
            self.duration = 5.0
            self.points = 75
        elif power_type == PowerUpType.ENTANGLEMENT:
            self.color = (255, 0, 255)  # Magenta
            self.glow_color = (255, 150, 255)
            self.duration = 10.0
            self.points = 100
    
    def update(self, dt: float):
        """Update power-up visual effects"""
        if not self.collected:
            self.rotation += dt * 2
            self.pulse_phase += dt * 3
            self.orbit_phase += dt * 4
            self.energy_phase += dt * 6
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle"""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, screen):
        """Draw the power-up with quantum effects"""
        if self.collected:
            return
        
        # Calculate dynamic effects
        pulse_size = 1 + math.sin(self.pulse_phase) * 0.3
        glow_intensity = (math.sin(self.pulse_phase * 1.2) + 1) * 0.5
        energy_flow = math.sin(self.energy_phase)
        
        # Draw energy field
        field_radius = int(self.radius * 2.5 * pulse_size)
        field_alpha = int(glow_intensity * 60)
        
        field_surface = pygame.Surface((field_radius * 2, field_radius * 2), pygame.SRCALPHA)
        
        # Multiple energy layers
        for i in range(4):
            alpha = field_alpha // (i + 1)
            radius = field_radius - i * 3
            if radius > 0:
                pygame.draw.circle(
                    field_surface,
                    (*self.glow_color, alpha),
                    (field_radius, field_radius),
                    radius
                )
        
        screen.blit(
            field_surface,
            (self.x - field_radius, self.y - field_radius),
            special_flags=pygame.BLEND_ADD
        )
        
        # Draw power-up specific effects
        if self.power_type == PowerUpType.SUPERPOSITION:
            self._draw_superposition_effect(screen, pulse_size, energy_flow)
        elif self.power_type == PowerUpType.MEASUREMENT:
            self._draw_measurement_effect(screen, pulse_size, energy_flow)
        elif self.power_type == PowerUpType.ENTANGLEMENT:
            self._draw_entanglement_effect(screen, pulse_size, energy_flow)
        
        # Draw main core
        main_radius = int(self.radius * pulse_size)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), main_radius)
        
        # Draw inner energy core
        inner_radius = max(1, int(main_radius * 0.6))
        inner_color = tuple(min(255, c + 80) for c in self.color)
        pygame.draw.circle(screen, inner_color, (int(self.x), int(self.y)), inner_radius)
    
    def _draw_superposition_effect(self, screen, pulse_size: float, energy_flow: float):
        """Draw superposition-specific visual effects"""
        # Draw probability wave patterns
        for i in range(3):
            angle = self.rotation + (i * math.pi * 2 / 3)
            wave_radius = 20 + energy_flow * 5
            
            wave_x = self.x + math.cos(angle) * wave_radius
            wave_y = self.y + math.sin(angle) * wave_radius
            
            # Flickering probability nodes
            if int(self.energy_phase * 5) % 2:
                pygame.draw.circle(screen, self.color, (int(wave_x), int(wave_y)), 3)
        
        # Draw quantum interference pattern
        for i in range(6):
            angle = i * math.pi / 3
            line_length = 15 * pulse_size
            end_x = self.x + math.cos(angle) * line_length
            end_y = self.y + math.sin(angle) * line_length
            
            alpha = int(128 + 127 * abs(energy_flow))
            line_color = (*self.color, alpha)
            
            # Create line surface with alpha
            line_surf = pygame.Surface((3, int(line_length * 2)), pygame.SRCALPHA)
            pygame.draw.line(line_surf, line_color, (1, 0), (1, int(line_length * 2)), 1)
            
            # Rotate and blit line
            rotated_surf = pygame.transform.rotate(line_surf, math.degrees(angle))
            rect = rotated_surf.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_surf, rect)
    
    def _draw_measurement_effect(self, screen, pulse_size: float, energy_flow: float):
        """Draw measurement-specific visual effects"""
        # Draw measurement apparatus (crosshairs)
        crosshair_size = 20 * pulse_size
        line_color = tuple(min(255, c + 50) for c in self.color)
        
        # Horizontal line
        pygame.draw.line(screen, line_color,
                        (self.x - crosshair_size, self.y),
                        (self.x + crosshair_size, self.y), 2)
        
        # Vertical line
        pygame.draw.line(screen, line_color,
                        (self.x, self.y - crosshair_size),
                        (self.x, self.y + crosshair_size), 2)
        
        # Draw measurement probability rings
        for i in range(3):
            ring_radius = int((10 + i * 8) * pulse_size)
            ring_alpha = int(100 - i * 30)
            
            if ring_alpha > 0:
                ring_surface = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(ring_surface, (*self.color, ring_alpha),
                                 (ring_radius, ring_radius), ring_radius, 2)
                screen.blit(ring_surface, (self.x - ring_radius, self.y - ring_radius))
    
    def _draw_entanglement_effect(self, screen, pulse_size: float, energy_flow: float):
        """Draw entanglement-specific visual effects"""
        # Draw quantum entanglement pairs
        pair_distance = 25 * pulse_size
        
        for i in range(2):
            angle = self.rotation + i * math.pi
            pair_x = self.x + math.cos(angle) * pair_distance
            pair_y = self.y + math.sin(angle) * pair_distance
            
            # Draw entangled particle
            particle_radius = int(4 * pulse_size)
            pygame.draw.circle(screen, self.color, (int(pair_x), int(pair_y)), particle_radius)
            
            # Draw connection line with quantum fluctuation
            connection_color = tuple(c // 2 for c in self.color)
            
            # Add quantum noise to the line
            segments = 10
            for j in range(segments):
                t1 = j / segments
                t2 = (j + 1) / segments
                
                # Interpolate positions with quantum fluctuation
                noise1 = math.sin(self.energy_phase + j) * 3
                noise2 = math.sin(self.energy_phase + j + 1) * 3
                
                x1 = self.x + (pair_x - self.x) * t1 + noise1
                y1 = self.y + (pair_y - self.y) * t1 + noise1
                x2 = self.x + (pair_x - self.x) * t2 + noise2
                y2 = self.y + (pair_y - self.y) * t2 + noise2
                
                pygame.draw.line(screen, connection_color, (int(x1), int(y1)), (int(x2), int(y2)), 1)
        
        # Draw entanglement field
        field_lines = 8
        for i in range(field_lines):
            angle = (i / field_lines) * math.pi * 2 + self.rotation
            inner_radius = 12
            outer_radius = 20 * pulse_size
            
            inner_x = self.x + math.cos(angle) * inner_radius
            inner_y = self.y + math.sin(angle) * inner_radius
            outer_x = self.x + math.cos(angle) * outer_radius
            outer_y = self.y + math.sin(angle) * outer_radius
            
            field_alpha = int(80 + 80 * abs(energy_flow))
            field_color = (*self.color, field_alpha)
            
            # Create field line surface
            line_surf = pygame.Surface((2, int(outer_radius - inner_radius)), pygame.SRCALPHA)
            pygame.draw.line(line_surf, field_color, (0, 0), (0, int(outer_radius - inner_radius)), 1)
            
            # Position the line
            screen.blit(line_surf, (int(inner_x), int(inner_y)))

class PowerUpManager:
    def __init__(self):
        self.powerups: List[PowerUp] = []
        self.spawn_timer = 0
        self.spawn_interval = 15.0  # Spawn power-up every 15 seconds
        
    def update(self, dt: float, maze):
        """Update power-up system"""
        # Update existing power-ups
        for powerup in self.powerups:
            powerup.update(dt)
        
        # Handle spawning
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_random_powerup(maze)
            self.spawn_timer = 0
    
    def spawn_random_powerup(self, maze):
        """Spawn a random power-up in the maze"""
        # Remove collected power-ups first
        self.powerups = [p for p in self.powerups if not p.collected]
        
        # Don't spawn if there are already 3 power-ups
        if len(self.powerups) >= 3:
            return
        
        # Get random path position
        path_positions = []
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == CellType.PATH:  # Check for PATH cells
                    center_x = x * maze.cell_size + maze.cell_size // 2
                    center_y = y * maze.cell_size + maze.cell_size // 2
                    path_positions.append((center_x, center_y))
        
        if path_positions:
            x, y = random.choice(path_positions)
            power_type = random.choice(list(PowerUpType))
            self.powerups.append(PowerUp(x, y, power_type))
    
    def check_collection(self, player_rect: pygame.Rect, player) -> tuple:
        """Check for power-up collection and apply effects"""
        points_earned = 0
        collected_types = []
        
        for powerup in self.powerups:
            if not powerup.collected and player_rect.colliderect(powerup.get_rect()):
                powerup.collected = True
                points_earned += powerup.points
                collected_types.append(powerup.power_type)
                
                # Apply power-up effect
                if powerup.power_type == PowerUpType.SUPERPOSITION:
                    player.activate_superposition(powerup.duration)
                elif powerup.power_type == PowerUpType.MEASUREMENT:
                    player.activate_measurement(powerup.duration)
                elif powerup.power_type == PowerUpType.ENTANGLEMENT:
                    # Entanglement effect will be handled by enemy manager
                    player.activate_measurement(powerup.duration)  # Temporary effect
        
        return points_earned, collected_types
    
    def get_entanglement_powerups(self) -> List[PowerUp]:
        """Get active entanglement power-ups for enemy manager"""
        return [p for p in self.powerups if 
                p.power_type == PowerUpType.ENTANGLEMENT and 
                not p.collected]
    
    def draw(self, screen):
        """Draw all active power-ups"""
        for powerup in self.powerups:
            if not powerup.collected:
                powerup.draw(screen)
    
    def clear(self):
        """Clear all power-ups"""
        self.powerups.clear()
        self.spawn_timer = 0
