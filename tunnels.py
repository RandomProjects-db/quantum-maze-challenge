import pygame
import math
import random
from typing import List, Tuple, Optional
from maze import CellType

class QuantumTunnel:
    def __init__(self, x: int, y: int, tunnel_id: int):
        self.x = float(x)
        self.y = float(y)
        self.tunnel_id = tunnel_id
        self.radius = 15
        self.linked_tunnel: Optional['QuantumTunnel'] = None
        
        # Visual effects
        self.rotation = 0
        self.pulse_phase = random.random() * math.pi * 2
        self.energy_phase = random.random() * math.pi * 2
        self.portal_phase = random.random() * math.pi * 2
        
        # Teleportation cooldown to prevent rapid teleporting
        self.cooldown_timer = 0
        self.cooldown_duration = 1.0  # 1 second cooldown
        
        # Colors based on tunnel ID
        tunnel_colors = [
            (0, 255, 255),   # Cyan
            (255, 0, 255),   # Magenta
            (255, 255, 0),   # Yellow
            (0, 255, 0),     # Green
        ]
        self.color = tunnel_colors[tunnel_id % len(tunnel_colors)]
        self.glow_color = tuple(min(255, c + 100) for c in self.color)
        
    def update(self, dt: float):
        """Update tunnel visual effects and cooldown"""
        self.rotation += dt * 2
        self.pulse_phase += dt * 4
        self.energy_phase += dt * 6
        self.portal_phase += dt * 3
        
        # Update cooldown
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
    
    def link_to(self, other_tunnel: 'QuantumTunnel'):
        """Link this tunnel to another tunnel"""
        self.linked_tunnel = other_tunnel
        other_tunnel.linked_tunnel = self
    
    def can_teleport(self) -> bool:
        """Check if teleportation is available"""
        return self.cooldown_timer <= 0 and self.linked_tunnel is not None
    
    def teleport_player(self, player) -> bool:
        """Teleport player to linked tunnel"""
        if not self.can_teleport():
            return False
        
        if self.linked_tunnel:
            # Set player position to linked tunnel
            player.x = self.linked_tunnel.x
            player.y = self.linked_tunnel.y
            
            # Set cooldown on both tunnels
            self.cooldown_timer = self.cooldown_duration
            self.linked_tunnel.cooldown_timer = self.cooldown_duration
            
            return True
        return False
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle"""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, screen):
        """Draw the quantum tunnel with portal effects"""
        # Calculate dynamic effects
        pulse_size = 1 + math.sin(self.pulse_phase) * 0.3
        glow_intensity = (math.sin(self.pulse_phase * 1.5) + 1) * 0.5
        energy_flow = math.sin(self.energy_phase)
        
        # Determine if tunnel is active
        is_active = self.can_teleport()
        alpha_multiplier = 1.0 if is_active else 0.5
        
        # Draw outer energy field
        field_radius = int(self.radius * 2.5 * pulse_size)
        field_alpha = int(glow_intensity * 80 * alpha_multiplier)
        
        field_surface = pygame.Surface((field_radius * 2, field_radius * 2), pygame.SRCALPHA)
        
        # Multiple energy layers
        for i in range(5):
            alpha = field_alpha // (i + 1)
            radius = field_radius - i * 4
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
        
        # Draw portal ring
        ring_radius = int(self.radius * pulse_size)
        ring_thickness = 3
        
        # Main portal ring
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), ring_radius, ring_thickness)
        
        # Inner portal rings
        for i in range(3):
            inner_radius = ring_radius - (i + 1) * 4
            if inner_radius > 0:
                inner_alpha = int(150 - i * 40)
                inner_color = (*self.color, inner_alpha)
                
                # Create ring surface with alpha
                ring_surf = pygame.Surface((inner_radius * 2, inner_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(ring_surf, inner_color, (inner_radius, inner_radius), inner_radius, 2)
                screen.blit(ring_surf, (self.x - inner_radius, self.y - inner_radius))
        
        # Draw portal vortex effect
        vortex_lines = 8
        for i in range(vortex_lines):
            angle = (i / vortex_lines) * math.pi * 2 + self.portal_phase
            
            # Spiral effect
            for j in range(5):
                spiral_radius = (j + 1) * 3
                spiral_angle = angle + j * 0.5
                
                spiral_x = self.x + math.cos(spiral_angle) * spiral_radius
                spiral_y = self.y + math.sin(spiral_angle) * spiral_radius
                
                particle_alpha = int(100 - j * 15)
                if particle_alpha > 0:
                    particle_color = (*self.color, particle_alpha)
                    particle_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surf, particle_color, (2, 2), 2)
                    screen.blit(particle_surf, (spiral_x - 2, spiral_y - 2))
        
        # Draw energy bolts
        if is_active:
            bolt_count = 6
            for i in range(bolt_count):
                bolt_angle = (i / bolt_count) * math.pi * 2 + self.energy_phase
                bolt_length = 20 + energy_flow * 5
                
                start_x = self.x + math.cos(bolt_angle) * (ring_radius - 5)
                start_y = self.y + math.sin(bolt_angle) * (ring_radius - 5)
                end_x = self.x + math.cos(bolt_angle) * bolt_length
                end_y = self.y + math.sin(bolt_angle) * bolt_length
                
                # Draw jagged energy bolt
                segments = 4
                for j in range(segments):
                    t1 = j / segments
                    t2 = (j + 1) / segments
                    
                    # Add randomness to bolt path
                    noise1 = random.uniform(-2, 2)
                    noise2 = random.uniform(-2, 2)
                    
                    x1 = start_x + (end_x - start_x) * t1 + noise1
                    y1 = start_y + (end_y - start_y) * t1 + noise1
                    x2 = start_x + (end_x - start_x) * t2 + noise2
                    y2 = start_y + (end_y - start_y) * t2 + noise2
                    
                    pygame.draw.line(screen, self.color, (int(x1), int(y1)), (int(x2), int(y2)), 2)
        
        # Draw cooldown indicator
        if self.cooldown_timer > 0:
            cooldown_progress = self.cooldown_timer / self.cooldown_duration
            cooldown_radius = int(self.radius * 1.2)
            
            # Draw cooldown arc
            arc_angle = cooldown_progress * math.pi * 2
            arc_points = []
            arc_segments = 20
            
            for i in range(arc_segments + 1):
                angle = (i / arc_segments) * arc_angle - math.pi / 2
                arc_x = self.x + math.cos(angle) * cooldown_radius
                arc_y = self.y + math.sin(angle) * cooldown_radius
                arc_points.append((int(arc_x), int(arc_y)))
            
            if len(arc_points) > 1:
                pygame.draw.lines(screen, (255, 0, 0), False, arc_points, 3)
        
        # Draw tunnel ID indicator
        font = pygame.font.Font(None, 24)
        id_text = font.render(str(self.tunnel_id + 1), True, self.color)
        text_rect = id_text.get_rect(center=(int(self.x), int(self.y - self.radius - 15)))
        screen.blit(id_text, text_rect)

class TunnelManager:
    def __init__(self):
        self.tunnels: List[QuantumTunnel] = []
        
    def create_tunnel_pair(self, maze, tunnel_id: int = 0) -> bool:
        """Create a pair of linked tunnels in the maze"""
        # Find suitable positions for tunnels (far apart)
        path_positions = []
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == CellType.PATH:
                    center_x = x * maze.cell_size + maze.cell_size // 2
                    center_y = y * maze.cell_size + maze.cell_size // 2
                    path_positions.append((center_x, center_y))
        
        if len(path_positions) < 2:
            return False
        
        # Find two positions that are far apart
        max_distance = 0
        best_positions = None
        
        for i, pos1 in enumerate(path_positions):
            for j, pos2 in enumerate(path_positions[i+1:], i+1):
                distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                if distance > max_distance:
                    max_distance = distance
                    best_positions = (pos1, pos2)
        
        if best_positions:
            pos1, pos2 = best_positions
            
            # Create tunnels
            tunnel1 = QuantumTunnel(pos1[0], pos1[1], tunnel_id)
            tunnel2 = QuantumTunnel(pos2[0], pos2[1], tunnel_id)
            
            # Link them together
            tunnel1.link_to(tunnel2)
            
            # Add to manager
            self.tunnels.extend([tunnel1, tunnel2])
            return True
        
        return False
    
    def update(self, dt: float):
        """Update all tunnels"""
        for tunnel in self.tunnels:
            tunnel.update(dt)
    
    def check_teleportation(self, player_rect: pygame.Rect, player) -> bool:
        """Check if player should be teleported"""
        for tunnel in self.tunnels:
            if tunnel.get_rect().colliderect(player_rect):
                if tunnel.teleport_player(player):
                    return True
        return False
    
    def draw(self, screen):
        """Draw all tunnels"""
        for tunnel in self.tunnels:
            tunnel.draw(screen)
    
    def clear(self):
        """Clear all tunnels"""
        self.tunnels.clear()
    
    def get_tunnel_count(self) -> int:
        """Get number of tunnel pairs"""
        return len(self.tunnels) // 2
