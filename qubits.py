import pygame
import math
import random
from typing import List, Tuple, Optional
from maze import CellType

class Qubit:
    def __init__(self, x: int, y: int, is_entangled: bool = False):
        self.x = float(x)
        self.y = float(y)
        self.radius = 6
        self.collected = False
        self.is_entangled = is_entangled
        self.entangled_partner: Optional['Qubit'] = None
        
        # Visual effects
        self.rotation = random.random() * math.pi * 2
        self.pulse_phase = random.random() * math.pi * 2
        self.orbit_phase = random.random() * math.pi * 2
        self.spin_speed = 2.0 + random.random() * 2.0
        
        # Colors
        if is_entangled:
            self.core_color = (255, 100, 255)  # Magenta for entangled
            self.glow_color = (255, 150, 255)
            self.orbit_color = (200, 100, 255)
            self.points = 25  # More points for entangled qubits
        else:
            self.core_color = (255, 215, 0)  # Gold for regular
            self.glow_color = (255, 255, 150)
            self.orbit_color = (200, 200, 255)
            self.points = 10
    
    def entangle_with(self, other_qubit: 'Qubit'):
        """Create entanglement with another qubit"""
        self.entangled_partner = other_qubit
        other_qubit.entangled_partner = self
        self.is_entangled = True
        other_qubit.is_entangled = True
        
        # Update colors and points
        for qubit in [self, other_qubit]:
            qubit.core_color = (255, 100, 255)
            qubit.glow_color = (255, 150, 255)
            qubit.orbit_color = (200, 100, 255)
            qubit.points = 25
        
    def update(self, dt: float):
        """Update qubit visual effects"""
        if not self.collected:
            self.rotation += dt * self.spin_speed
            self.pulse_phase += dt * 4
            self.orbit_phase += dt * 3
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle"""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, screen):
        """Draw the qubit with quantum effects"""
        if self.collected:
            return
            
        # Calculate dynamic effects
        pulse_size = 1 + math.sin(self.pulse_phase) * 0.2
        glow_intensity = (math.sin(self.pulse_phase * 1.5) + 1) * 0.5
        
        # Draw entanglement connection first (so it appears behind qubits)
        if self.is_entangled and self.entangled_partner and not self.entangled_partner.collected:
            self._draw_entanglement_connection(screen)
        
        # Draw orbital particles
        for i in range(3):
            angle = self.orbit_phase + (i * math.pi * 2 / 3)
            orbit_radius = 15
            orbit_x = self.x + math.cos(angle) * orbit_radius
            orbit_y = self.y + math.sin(angle) * orbit_radius
            
            particle_alpha = int(100 + 100 * math.sin(angle + self.orbit_phase))
            particle_color = (*self.orbit_color, particle_alpha)
            
            # Create particle surface with alpha
            particle_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, particle_color, (2, 2), 2)
            screen.blit(particle_surf, (orbit_x - 2, orbit_y - 2))
        
        # Draw outer glow
        glow_radius = int(self.radius * 2 * pulse_size)
        glow_alpha = int(glow_intensity * 80)
        
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        
        # Multiple glow layers
        for i in range(3):
            alpha = glow_alpha // (i + 1)
            radius = glow_radius - i * 2
            if radius > 0:
                pygame.draw.circle(
                    glow_surface,
                    (*self.glow_color, alpha),
                    (glow_radius, glow_radius),
                    radius
                )
        
        screen.blit(
            glow_surface,
            (self.x - glow_radius, self.y - glow_radius),
            special_flags=pygame.BLEND_ADD
        )
        
        # Draw main qubit body
        main_radius = int(self.radius * pulse_size)
        pygame.draw.circle(screen, self.core_color, (int(self.x), int(self.y)), main_radius)
        
        # Draw inner quantum state visualization
        inner_radius = max(1, int(main_radius * 0.6))
        
        # Rotating quantum state indicator
        state_x = self.x + math.cos(self.rotation) * inner_radius * 0.5
        state_y = self.y + math.sin(self.rotation) * inner_radius * 0.5
        pygame.draw.circle(screen, (255, 255, 255), (int(state_x), int(state_y)), 2)
        
        # Draw quantum interference pattern
        pattern_lines = 6 if self.is_entangled else 4
        for i in range(pattern_lines):
            angle = self.rotation + (i * math.pi / pattern_lines)
            line_end_x = self.x + math.cos(angle) * main_radius * 0.8
            line_end_y = self.y + math.sin(angle) * main_radius * 0.8
            
            line_color = (255, 255, 200) if not self.is_entangled else (255, 200, 255)
            pygame.draw.line(
                screen,
                line_color,
                (int(self.x), int(self.y)),
                (int(line_end_x), int(line_end_y)),
                1
            )
    
    def _draw_entanglement_connection(self, screen):
        """Draw the quantum entanglement connection"""
        if not self.entangled_partner:
            return
        
        partner = self.entangled_partner
        
        # Draw pulsating connection line
        connection_alpha = int(100 + 100 * math.sin(self.pulse_phase))
        connection_color = (255, 0, 255, connection_alpha)
        
        # Create connection surface
        dx = partner.x - self.x
        dy = partner.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Draw multiple connection lines for quantum effect
            for i in range(3):
                offset = (i - 1) * 2
                
                # Calculate perpendicular offset
                perp_x = -dy / distance * offset
                perp_y = dx / distance * offset
                
                start_x = self.x + perp_x
                start_y = self.y + perp_y
                end_x = partner.x + perp_x
                end_y = partner.y + perp_y
                
                # Draw wavy line
                segments = 10
                points = []
                for j in range(segments + 1):
                    t = j / segments
                    
                    # Interpolate position
                    line_x = start_x + (end_x - start_x) * t
                    line_y = start_y + (end_y - start_y) * t
                    
                    # Add wave effect
                    wave_offset = math.sin(t * math.pi * 4 + self.pulse_phase) * 3
                    wave_x = line_x + perp_x * wave_offset
                    wave_y = line_y + perp_y * wave_offset
                    
                    points.append((int(wave_x), int(wave_y)))
                
                if len(points) > 1:
                    line_alpha = connection_alpha // (i + 1)
                    line_color = (255, 100, 255, line_alpha)
                    
                    # Draw line segments
                    for k in range(len(points) - 1):
                        pygame.draw.line(screen, line_color[:3], points[k], points[k+1], 2)
        
        # Draw entanglement particles along the connection
        particle_count = 5
        for i in range(particle_count):
            t = (i / particle_count + self.pulse_phase * 0.1) % 1.0
            
            particle_x = self.x + (partner.x - self.x) * t
            particle_y = self.y + (partner.y - self.y) * t
            
            particle_alpha = int(150 * math.sin(t * math.pi))
            if particle_alpha > 50:
                particle_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                particle_color = (255, 100, 255, particle_alpha)
                pygame.draw.circle(particle_surf, particle_color, (3, 3), 3)
                screen.blit(particle_surf, (particle_x - 3, particle_y - 3))

class QubitManager:
    def __init__(self):
        self.qubits: List[Qubit] = []
        self.total_qubits = 0
        self.collected_qubits = 0
        self.entangled_pairs: List[Tuple[Qubit, Qubit]] = []
        self.entanglement_timer = 0
        self.entanglement_duration = 10.0  # 10 seconds to collect partner
        self.active_entanglement = None  # Currently active entanglement bonus
        
    def generate_qubits(self, maze, count: int = 50, entangled_pairs: int = 2):
        """Generate qubits in the maze paths"""
        self.qubits.clear()
        self.entangled_pairs.clear()
        self.total_qubits = count
        self.collected_qubits = 0
        self.active_entanglement = None
        
        # Get all path positions
        path_positions = []
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == CellType.PATH:
                    center_x = x * maze.cell_size + maze.cell_size // 2
                    center_y = y * maze.cell_size + maze.cell_size // 2
                    path_positions.append((center_x, center_y))
        
        if len(path_positions) < count:
            count = len(path_positions)
            self.total_qubits = count
        
        # Check if we have enough positions for entangled pairs
        needed_positions = count
        if needed_positions > len(path_positions):
            # Reduce entangled pairs if necessary
            max_entangled_pairs = (len(path_positions) - (count - entangled_pairs * 2)) // 2
            entangled_pairs = max(0, min(entangled_pairs, max_entangled_pairs))
        
        # Select positions for qubits
        selected_positions = random.sample(path_positions, count)
        
        # Create regular qubits
        regular_count = count - (entangled_pairs * 2)
        for i in range(regular_count):
            x, y = selected_positions[i]
            self.qubits.append(Qubit(x, y, False))
        
        # Create entangled pairs
        for i in range(entangled_pairs):
            if regular_count + i * 2 + 1 < len(selected_positions):
                # Create first qubit of pair
                x1, y1 = selected_positions[regular_count + i * 2]
                qubit1 = Qubit(x1, y1, True)
                
                # Create second qubit of pair
                x2, y2 = selected_positions[regular_count + i * 2 + 1]
                qubit2 = Qubit(x2, y2, True)
                
                # Entangle them
                qubit1.entangle_with(qubit2)
                
                # Add to lists
                self.qubits.extend([qubit1, qubit2])
                self.entangled_pairs.append((qubit1, qubit2))
    
    def update(self, dt: float):
        """Update all qubits and entanglement timers"""
        for qubit in self.qubits:
            qubit.update(dt)
        
        # Update entanglement timer
        if self.active_entanglement:
            self.entanglement_timer -= dt
            if self.entanglement_timer <= 0:
                # Timer expired, no bonus
                self.active_entanglement = None
    
    def check_collection(self, player_rect: pygame.Rect) -> Tuple[int, bool]:
        """Check for qubit collection and return (points earned, entanglement_activated)"""
        points_earned = 0
        entanglement_activated = False
        
        for qubit in self.qubits:
            if not qubit.collected and player_rect.colliderect(qubit.get_rect()):
                qubit.collected = True
                self.collected_qubits += 1
                
                if qubit.is_entangled and qubit.entangled_partner:
                    # Check if this starts or completes an entanglement
                    partner = qubit.entangled_partner
                    
                    if not partner.collected:
                        # First of the pair collected - start timer
                        self.active_entanglement = (qubit, partner)
                        self.entanglement_timer = self.entanglement_duration
                        points_earned += qubit.points
                        entanglement_activated = True
                    else:
                        # Partner already collected - this shouldn't happen normally
                        points_earned += qubit.points
                elif self.active_entanglement:
                    # Check if this completes an active entanglement
                    active_qubit, active_partner = self.active_entanglement
                    
                    if qubit == active_partner:
                        # Entanglement completed in time!
                        bonus_points = 100  # Bonus for completing entanglement
                        points_earned += qubit.points + bonus_points
                        self.active_entanglement = None
                        entanglement_activated = True
                    else:
                        # Different qubit collected
                        points_earned += qubit.points
                else:
                    # Regular qubit
                    points_earned += qubit.points
                
        return points_earned, entanglement_activated
    
    def draw(self, screen):
        """Draw all uncollected qubits"""
        for qubit in self.qubits:
            if not qubit.collected:
                qubit.draw(screen)
    
    def draw_entanglement_timer(self, screen, font):
        """Draw entanglement timer if active"""
        if self.active_entanglement and self.entanglement_timer > 0:
            timer_text = f"Entanglement: {self.entanglement_timer:.1f}s"
            timer_color = (255, 100, 255)
            
            # Flash when time is running out
            if self.entanglement_timer < 3.0:
                flash_alpha = int(128 + 127 * math.sin(self.entanglement_timer * 10))
                timer_color = (255, flash_alpha, 255)
            
            text_surface = font.render(timer_text, True, timer_color)
            screen.blit(text_surface, (10, 130))
    
    def all_collected(self) -> bool:
        """Check if all qubits have been collected"""
        return self.collected_qubits >= self.total_qubits
    
    def get_remaining_count(self) -> int:
        """Get number of remaining qubits"""
        return self.total_qubits - self.collected_qubits
    
    def get_entangled_qubits(self) -> List[Qubit]:
        """Get all entangled qubits for guardian ghosts"""
        return [q for q in self.qubits if q.is_entangled and not q.collected]
