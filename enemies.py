import pygame
import math
import random
from typing import List, Tuple, Optional
from enum import Enum
from maze import CellType

class GhostState(Enum):
    CHASE = 1
    SCATTER = 2
    FRIGHTENED = 3

class GhostType(Enum):
    CHASER = 1      # Follows player using pathfinding
    WANDERER = 2    # Moves randomly
    GUARDIAN = 3    # Patrols areas with many qubits

class DecoherenceGhost:
    def __init__(self, x: int, y: int, ghost_id: int = 0, ghost_type: GhostType = GhostType.CHASER):
        self.x = float(x)
        self.y = float(y)
        self.ghost_id = ghost_id
        self.ghost_type = ghost_type
        self.radius = 10
        self.speed = 1.5
        
        # AI state
        self.state = GhostState.CHASE
        self.target_x = x
        self.target_y = y
        self.direction = random.choice([(0, -1), (1, 0), (0, 1), (-1, 0)])  # Up, Right, Down, Left
        self.last_direction = self.direction
        
        # Type-specific properties
        if ghost_type == GhostType.WANDERER:
            self.speed = 1.2  # Slightly slower
            self.direction_change_timer = 0
            self.direction_change_interval = 2.0  # Change direction every 2 seconds
        elif ghost_type == GhostType.GUARDIAN:
            self.speed = 1.0  # Slower but more persistent
            self.patrol_center = (x, y)
            self.patrol_radius = 100
            self.guard_qubits = []  # Will be set by manager
        
        # Visual effects
        self.glitch_phase = random.random() * math.pi * 2
        self.instability_phase = random.random() * math.pi * 2
        self.corruption_level = 0.0
        
        # Colors based on ghost type and ID
        if ghost_type == GhostType.CHASER:
            base_colors = [(255, 50, 50), (255, 150, 50), (50, 255, 50), (150, 50, 255)]
        elif ghost_type == GhostType.WANDERER:
            base_colors = [(100, 100, 255), (100, 255, 255), (255, 100, 255), (255, 255, 100)]
        elif ghost_type == GhostType.GUARDIAN:
            base_colors = [(150, 75, 0), (200, 100, 0), (100, 50, 0), (175, 87, 25)]
        
        self.base_color = base_colors[ghost_id % len(base_colors)]
        self.glitch_color = (255, 255, 255)
        
        # Pathfinding
        self.path = []
        self.path_index = 0
        self.recalculate_path_timer = 0
        
        # Entanglement
        self.entangled_with = None
        self.is_captured = False
        
    def update(self, dt: float, maze, player, other_ghosts: List['DecoherenceGhost'], qubits=None):
        """Update ghost AI and movement"""
        if self.is_captured:
            return
            
        # Update visual effects
        self.glitch_phase += dt * 8
        self.instability_phase += dt * 5
        self.corruption_level = (math.sin(self.instability_phase) + 1) * 0.5
        
        # Update pathfinding timer
        self.recalculate_path_timer -= dt
        
        # Type-specific behavior updates
        if self.ghost_type == GhostType.WANDERER:
            self.direction_change_timer -= dt
            if self.direction_change_timer <= 0:
                self._change_random_direction()
                self.direction_change_timer = self.direction_change_interval
        
        # Determine target based on state and type
        if self.state == GhostState.FRIGHTENED:
            # All types flee when frightened
            dx = self.x - player.x
            dy = self.y - player.y
            if dx != 0 or dy != 0:
                length = math.sqrt(dx*dx + dy*dy)
                self.target_x = self.x + (dx/length) * 100
                self.target_y = self.y + (dy/length) * 100
        else:
            self._update_target_by_type(player, qubits)
        
        # Recalculate path if needed
        if self.recalculate_path_timer <= 0 or not self.path:
            if self.ghost_type == GhostType.WANDERER and self.state != GhostState.FRIGHTENED:
                self._wander_movement(dt, maze)
            else:
                self.path = self._find_path_to_target(maze)
                self.path_index = 0
            self.recalculate_path_timer = 1.0  # Recalculate every second
        
        # Move along path (except for wanderers in normal state)
        if not (self.ghost_type == GhostType.WANDERER and self.state != GhostState.FRIGHTENED):
            self._move_along_path(dt, maze)
        
        # Handle entanglement
        if self.entangled_with and self.entangled_with.is_captured:
            self.is_captured = True
    
    def _update_target_by_type(self, player, qubits):
        """Update target based on ghost type"""
        if self.ghost_type == GhostType.CHASER:
            if self.state == GhostState.CHASE:
                self.target_x = player.x
                self.target_y = player.y
            elif self.state == GhostState.SCATTER:
                corners = [(50, 50), (750, 50), (750, 550), (50, 550)]
                corner = corners[self.ghost_id % len(corners)]
                self.target_x, self.target_y = corner
                
        elif self.ghost_type == GhostType.GUARDIAN:
            if qubits and self.state == GhostState.CHASE:
                # Find nearest uncollected qubit to guard
                nearest_qubit = None
                min_distance = float('inf')
                
                for qubit in qubits:
                    if not qubit.collected:
                        distance = math.sqrt((qubit.x - self.patrol_center[0])**2 + 
                                           (qubit.y - self.patrol_center[1])**2)
                        if distance < self.patrol_radius and distance < min_distance:
                            min_distance = distance
                            nearest_qubit = qubit
                
                if nearest_qubit:
                    self.target_x = nearest_qubit.x
                    self.target_y = nearest_qubit.y
                else:
                    # No qubits to guard, patrol around center
                    angle = math.sin(self.glitch_phase) * math.pi
                    patrol_distance = 30
                    self.target_x = self.patrol_center[0] + math.cos(angle) * patrol_distance
                    self.target_y = self.patrol_center[1] + math.sin(angle) * patrol_distance
            elif self.state == GhostState.SCATTER:
                # Return to patrol center
                self.target_x, self.target_y = self.patrol_center
    
    def _change_random_direction(self):
        """Change to a random direction (for wanderer type)"""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        # Avoid immediate reversal
        opposite_direction = (-self.direction[0], -self.direction[1])
        available_directions = [d for d in directions if d != opposite_direction]
        
        if available_directions:
            self.direction = random.choice(available_directions)
    
    def _wander_movement(self, dt: float, maze):
        """Simple wandering movement for wanderer type"""
        move_distance = self.speed * dt * 60
        
        new_x = self.x + self.direction[0] * move_distance
        new_y = self.y + self.direction[1] * move_distance
        
        # Check if we can move in current direction
        if not maze.is_wall_at(new_x, new_y):
            self.x = new_x
            self.y = new_y
        else:
            # Hit a wall, change direction
            self._change_random_direction()
    
    def _find_path_to_target(self, maze) -> List[Tuple[int, int]]:
        """Simple pathfinding using A* algorithm"""
        start_grid_x = int(self.x // maze.cell_size)
        start_grid_y = int(self.y // maze.cell_size)
        target_grid_x = int(self.target_x // maze.cell_size)
        target_grid_y = int(self.target_y // maze.cell_size)
        
        # Clamp to maze bounds
        target_grid_x = max(0, min(maze.width - 1, target_grid_x))
        target_grid_y = max(0, min(maze.height - 1, target_grid_y))
        
        # Simple pathfinding - just move towards target
        path = []
        current_x, current_y = start_grid_x, start_grid_y
        
        # Add some randomness to prevent getting stuck
        for _ in range(20):  # Limit iterations
            if current_x == target_grid_x and current_y == target_grid_y:
                break
                
            # Choose direction towards target
            dx = 0
            dy = 0
            
            if current_x < target_grid_x:
                dx = 1
            elif current_x > target_grid_x:
                dx = -1
                
            if current_y < target_grid_y:
                dy = 1
            elif current_y > target_grid_y:
                dy = -1
            
            # Try to move in preferred direction
            next_x = current_x + dx
            next_y = current_y + dy
            
            # Check if move is valid
            if (0 <= next_x < maze.width and 0 <= next_y < maze.height and
                maze.grid[next_y][next_x] != CellType.WALL):
                current_x, current_y = next_x, next_y
                path.append((current_x * maze.cell_size + maze.cell_size // 2,
                           current_y * maze.cell_size + maze.cell_size // 2))
            else:
                # Try alternative directions
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(directions)
                
                for alt_dx, alt_dy in directions:
                    alt_x = current_x + alt_dx
                    alt_y = current_y + alt_dy
                    
                    if (0 <= alt_x < maze.width and 0 <= alt_y < maze.height and
                        maze.grid[alt_y][alt_x] != CellType.WALL):
                        current_x, current_y = alt_x, alt_y
                        path.append((current_x * maze.cell_size + maze.cell_size // 2,
                                   current_y * maze.cell_size + maze.cell_size // 2))
                        break
                else:
                    # No valid moves, stop pathfinding
                    break
        
        return path
        """Simple pathfinding using A* algorithm"""
        start_grid_x = int(self.x // maze.cell_size)
        start_grid_y = int(self.y // maze.cell_size)
        target_grid_x = int(self.target_x // maze.cell_size)
        target_grid_y = int(self.target_y // maze.cell_size)
        
        # Clamp to maze bounds
        target_grid_x = max(0, min(maze.width - 1, target_grid_x))
        target_grid_y = max(0, min(maze.height - 1, target_grid_y))
        
        # Simple pathfinding - just move towards target
        path = []
        current_x, current_y = start_grid_x, start_grid_y
        
        # Add some randomness to prevent getting stuck
        for _ in range(20):  # Limit iterations
            if current_x == target_grid_x and current_y == target_grid_y:
                break
                
            # Choose direction towards target
            dx = 0
            dy = 0
            
            if current_x < target_grid_x:
                dx = 1
            elif current_x > target_grid_x:
                dx = -1
                
            if current_y < target_grid_y:
                dy = 1
            elif current_y > target_grid_y:
                dy = -1
            
            # Try to move in preferred direction
            next_x = current_x + dx
            next_y = current_y + dy
            
            # Check if move is valid
            if (0 <= next_x < maze.width and 0 <= next_y < maze.height and
                maze.grid[next_y][next_x] != CellType.WALL):
                current_x, current_y = next_x, next_y
                path.append((current_x * maze.cell_size + maze.cell_size // 2,
                           current_y * maze.cell_size + maze.cell_size // 2))
            else:
                # Try alternative directions
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                random.shuffle(directions)
                
                for alt_dx, alt_dy in directions:
                    alt_x = current_x + alt_dx
                    alt_y = current_y + alt_dy
                    
                    if (0 <= alt_x < maze.width and 0 <= alt_y < maze.height and
                        maze.grid[alt_y][alt_x] != CellType.WALL):
                        current_x, current_y = alt_x, alt_y
                        path.append((current_x * maze.cell_size + maze.cell_size // 2,
                                   current_y * maze.cell_size + maze.cell_size // 2))
                        break
                else:
                    # No valid moves, stop pathfinding
                    break
        
        return path
    
    def _move_along_path(self, dt: float, maze):
        """Move ghost along the calculated path"""
        if not self.path or self.path_index >= len(self.path):
            return
            
        target_x, target_y = self.path[self.path_index]
        
        # Move towards current path target
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 5:  # Close enough to target
            self.path_index += 1
        else:
            # Move towards target
            move_x = (dx / distance) * self.speed * dt * 60
            move_y = (dy / distance) * self.speed * dt * 60
            
            new_x = self.x + move_x
            new_y = self.y + move_y
            
            # Check collision with maze
            if not maze.is_wall_at(new_x, new_y):
                self.x = new_x
                self.y = new_y
    
    def set_state(self, new_state: GhostState):
        """Change ghost state"""
        if self.state != new_state:
            self.state = new_state
            self.recalculate_path_timer = 0  # Force immediate recalculation
    
    def set_guard_area(self, center_x: float, center_y: float, radius: float = 100):
        """Set the area for guardian ghost to patrol"""
        if self.ghost_type == GhostType.GUARDIAN:
            self.patrol_center = (center_x, center_y)
            self.patrol_radius = radius
    
    def entangle_with(self, other_ghost: 'DecoherenceGhost'):
        """Create quantum entanglement with another ghost"""
        self.entangled_with = other_ghost
        other_ghost.entangled_with = self
    
    def capture(self):
        """Capture this ghost"""
        self.is_captured = True
        if self.entangled_with:
            self.entangled_with.is_captured = True
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rectangle"""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    
    def draw(self, screen):
        """Draw the decoherence ghost with glitch effects"""
        if self.is_captured:
            return
            
        # Calculate glitch effects
        glitch_offset_x = math.sin(self.glitch_phase) * 3 * self.corruption_level
        glitch_offset_y = math.cos(self.glitch_phase * 1.3) * 2 * self.corruption_level
        
        draw_x = int(self.x + glitch_offset_x)
        draw_y = int(self.y + glitch_offset_y)
        
        # Draw type-specific particle trails
        self._draw_type_effects(screen, draw_x, draw_y)
        
        # Draw multiple corrupted versions for glitch effect
        if self.corruption_level > 0.5:
            for i in range(3):
                offset_x = random.randint(-2, 2)
                offset_y = random.randint(-2, 2)
                alpha = int(100 * (1 - i * 0.3))
                
                # Create ghost surface with alpha
                ghost_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                color_with_alpha = (*self.glitch_color, alpha)
                pygame.draw.circle(ghost_surf, color_with_alpha, 
                                 (self.radius, self.radius), self.radius)
                
                screen.blit(ghost_surf, (draw_x - self.radius + offset_x, 
                                       draw_y - self.radius + offset_y))
        
        # Draw main ghost body
        if self.state == GhostState.FRIGHTENED:
            # Blue when frightened
            main_color = (50, 50, 255)
        else:
            main_color = self.base_color
            
        pygame.draw.circle(screen, main_color, (draw_x, draw_y), self.radius)
        
        # Draw corruption patterns
        corruption_intensity = int(self.corruption_level * 255)
        if corruption_intensity > 50:
            # Draw digital noise pattern
            for i in range(5):
                noise_x = draw_x + random.randint(-self.radius, self.radius)
                noise_y = draw_y + random.randint(-self.radius, self.radius)
                noise_color = (corruption_intensity, corruption_intensity, corruption_intensity)
                pygame.draw.circle(screen, noise_color, (noise_x, noise_y), 1)
        
        # Draw eyes
        eye_offset = 4
        eye_color = (255, 255, 255) if self.state != GhostState.FRIGHTENED else (255, 0, 0)
        
        pygame.draw.circle(screen, eye_color, 
                         (draw_x - eye_offset, draw_y - 2), 2)
        pygame.draw.circle(screen, eye_color, 
                         (draw_x + eye_offset, draw_y - 2), 2)
        
        # Draw entanglement connection
        if self.entangled_with and not self.entangled_with.is_captured:
            # Draw quantum entanglement line
            entanglement_color = (0, 255, 255)
            pygame.draw.line(screen, entanglement_color,
                           (int(self.x), int(self.y)),
                           (int(self.entangled_with.x), int(self.entangled_with.y)), 2)
            
            # Draw entanglement particles
            mid_x = (self.x + self.entangled_with.x) / 2
            mid_y = (self.y + self.entangled_with.y) / 2
            
            for i in range(3):
                particle_phase = self.glitch_phase + i * math.pi / 3
                particle_x = mid_x + math.sin(particle_phase) * 10
                particle_y = mid_y + math.cos(particle_phase) * 10
                pygame.draw.circle(screen, entanglement_color, 
                                 (int(particle_x), int(particle_y)), 2)
    
    def _draw_type_effects(self, screen, draw_x: int, draw_y: int):
        """Draw type-specific visual effects"""
        if self.ghost_type == GhostType.CHASER:
            # Draw pursuit trail
            trail_length = 5
            for i in range(trail_length):
                trail_alpha = int(100 - i * 15)
                if trail_alpha > 0:
                    trail_offset = i * 3
                    trail_x = draw_x - self.direction[0] * trail_offset
                    trail_y = draw_y - self.direction[1] * trail_offset
                    
                    trail_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
                    trail_color = (*self.base_color, trail_alpha)
                    pygame.draw.circle(trail_surf, trail_color, (2, 2), 2)
                    screen.blit(trail_surf, (trail_x - 2, trail_y - 2))
        
        elif self.ghost_type == GhostType.WANDERER:
            # Draw random particle cloud
            for i in range(8):
                particle_angle = random.random() * math.pi * 2
                particle_distance = random.randint(15, 25)
                particle_x = draw_x + math.cos(particle_angle) * particle_distance
                particle_y = draw_y + math.sin(particle_angle) * particle_distance
                
                particle_alpha = random.randint(50, 150)
                particle_surf = pygame.Surface((3, 3), pygame.SRCALPHA)
                particle_color = (*self.base_color, particle_alpha)
                pygame.draw.circle(particle_surf, particle_color, (1, 1), 1)
                screen.blit(particle_surf, (particle_x - 1, particle_y - 1))
        
        elif self.ghost_type == GhostType.GUARDIAN:
            # Draw patrol area indicator
            if hasattr(self, 'patrol_center'):
                patrol_alpha = int(30 + 20 * math.sin(self.glitch_phase))
                patrol_surf = pygame.Surface((self.patrol_radius * 2, self.patrol_radius * 2), pygame.SRCALPHA)
                patrol_color = (*self.base_color, patrol_alpha)
                pygame.draw.circle(patrol_surf, patrol_color, 
                                 (self.patrol_radius, self.patrol_radius), 
                                 self.patrol_radius, 2)
                screen.blit(patrol_surf, 
                          (self.patrol_center[0] - self.patrol_radius, 
                           self.patrol_center[1] - self.patrol_radius))

class EnemyManager:
    def __init__(self):
        self.ghosts: List[DecoherenceGhost] = []
        self.state_timer = 0
        self.current_mode = GhostState.CHASE
        
    def spawn_ghosts(self, maze, count: int = 4):
        """Spawn decoherence ghosts in the maze"""
        self.ghosts.clear()
        
        # Find suitable spawn positions (away from player start)
        spawn_positions = []
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == CellType.PATH:
                    center_x = x * maze.cell_size + maze.cell_size // 2
                    center_y = y * maze.cell_size + maze.cell_size // 2
                    # Avoid center area where player starts
                    if (abs(center_x - 400) > 100 or abs(center_y - 300) > 100):
                        spawn_positions.append((center_x, center_y))
        
        # Define ghost type distribution
        ghost_types = [GhostType.CHASER, GhostType.WANDERER, GhostType.GUARDIAN]
        
        # Spawn ghosts
        for i in range(min(count, len(spawn_positions))):
            x, y = spawn_positions[i * len(spawn_positions) // count]
            
            # Assign ghost type based on index
            ghost_type = ghost_types[i % len(ghost_types)]
            ghost = DecoherenceGhost(x, y, i, ghost_type)
            
            # Set up guardian patrol area
            if ghost_type == GhostType.GUARDIAN:
                ghost.set_guard_area(x, y, 80)
            
            self.ghosts.append(ghost)
        
        # Create some entanglements
        if len(self.ghosts) >= 2:
            self.ghosts[0].entangle_with(self.ghosts[1])
        if len(self.ghosts) >= 4:
            self.ghosts[2].entangle_with(self.ghosts[3])
    
    def update(self, dt: float, maze, player, qubits=None):
        """Update all ghosts"""
        # Update mode timer
        self.state_timer += dt
        
        # Change modes periodically
        if self.state_timer > 10:  # Change mode every 10 seconds
            if self.current_mode == GhostState.CHASE:
                self.current_mode = GhostState.SCATTER
            else:
                self.current_mode = GhostState.CHASE
            
            self.state_timer = 0
            
            # Update all ghost states
            for ghost in self.ghosts:
                if ghost.state != GhostState.FRIGHTENED:
                    ghost.set_state(self.current_mode)
        
        # Update individual ghosts
        for ghost in self.ghosts:
            ghost.update(dt, maze, player, self.ghosts, qubits)
    
    def set_frightened_mode(self, duration: float = 5.0):
        """Set all ghosts to frightened mode"""
        for ghost in self.ghosts:
            if not ghost.is_captured:
                ghost.set_state(GhostState.FRIGHTENED)
        
        # Reset mode timer to give player time
        self.state_timer = -duration
    
    def check_collision(self, player_rect: pygame.Rect, player_has_measurement: bool = False) -> bool:
        """Check collision between player and ghosts"""
        for ghost in self.ghosts:
            if not ghost.is_captured and player_rect.colliderect(ghost.get_rect()):
                if player_has_measurement or ghost.state == GhostState.FRIGHTENED:
                    # Player can capture ghost
                    ghost.capture()
                    return False  # No damage to player
                else:
                    # Ghost catches player
                    return True
        return False
    
    def draw(self, screen):
        """Draw all ghosts"""
        for ghost in self.ghosts:
            ghost.draw(screen)
    
    def all_captured(self) -> bool:
        """Check if all ghosts are captured"""
        return all(ghost.is_captured for ghost in self.ghosts)
    
    def get_active_count(self) -> int:
        """Get number of active (non-captured) ghosts"""
        return sum(1 for ghost in self.ghosts if not ghost.is_captured)
