import pygame
import random
import math
from typing import List, Tuple, Set
from enum import Enum

class CellType(Enum):
    WALL = 0
    PATH = 1
    SUPERPOSITION_WALL = 2

class SuperpositionWall:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.phase = random.random() * math.pi * 2
        self.frequency = 0.5 + random.random() * 1.5  # Varies flicker speed
        self.is_solid = True
        self.alpha = 255
        
    def update(self, dt: float):
        """Update superposition wall state"""
        self.phase += dt * self.frequency
        
        # Determine if wall is solid based on quantum superposition
        wave_value = math.sin(self.phase)
        self.is_solid = wave_value > 0
        
        # Calculate alpha for visual effect
        self.alpha = int(128 + 127 * abs(wave_value))

class Maze:
    def __init__(self, width: int, height: int, cell_size: int = 20):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = []
        self.superposition_walls = []
        
        # Colors
        self.wall_color = (100, 100, 150)
        self.path_color = (20, 20, 40)
        self.superposition_color = (0, 255, 150)
        
        self.generate_maze()
        
    def generate_maze(self):
        """Generate a maze using recursive backtracking algorithm"""
        # Initialize grid with walls
        self.grid = [[CellType.WALL for _ in range(self.width)] for _ in range(self.height)]
        
        # Create paths using recursive backtracking
        self._carve_paths(1, 1)
        
        # Add superposition walls
        self._add_superposition_walls()
        
        # Ensure borders are always walls
        self._ensure_borders()
        
    def _carve_paths(self, x: int, y: int, depth: int = 0):
        """Carve paths through the maze using recursive backtracking"""
        # Prevent infinite recursion
        if depth > 1000:
            return
            
        self.grid[y][x] = CellType.PATH
        
        # Define directions (up, right, down, left)
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if the new position is valid and unvisited
            if (0 < nx < self.width - 1 and 
                0 < ny < self.height - 1 and 
                self.grid[ny][nx] == CellType.WALL):
                
                # Carve the wall between current and next cell
                self.grid[y + dy // 2][x + dx // 2] = CellType.PATH
                self._carve_paths(nx, ny, depth + 1)
    
    def _add_superposition_walls(self):
        """Add superposition walls to the maze"""
        self.superposition_walls.clear()
        
        # Convert some regular walls to superposition walls
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == CellType.WALL:
                    # 15% chance to become a superposition wall
                    if random.random() < 0.15:
                        # Only if it's not a structural wall (has paths on both sides)
                        if self._can_be_superposition_wall(x, y):
                            self.grid[y][x] = CellType.SUPERPOSITION_WALL
                            self.superposition_walls.append(SuperpositionWall(x, y))
    
    def _can_be_superposition_wall(self, x: int, y: int) -> bool:
        """Check if a wall can become a superposition wall"""
        # Count adjacent paths
        path_count = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.width and 0 <= ny < self.height and 
                self.grid[ny][nx] == CellType.PATH):
                path_count += 1
        
        # Only walls with exactly 2 adjacent paths can be superposition walls
        return path_count == 2
    
    def _ensure_borders(self):
        """Ensure maze borders are always solid walls"""
        for x in range(self.width):
            self.grid[0][x] = CellType.WALL
            self.grid[self.height - 1][x] = CellType.WALL
            
        for y in range(self.height):
            self.grid[y][0] = CellType.WALL
            self.grid[y][self.width - 1] = CellType.WALL
    
    def update(self, dt: float):
        """Update maze state (mainly superposition walls)"""
        for wall in self.superposition_walls:
            wall.update(dt)
    
    def is_wall_at(self, x: int, y: int, player_has_superposition: bool = False) -> bool:
        """Check if there's a solid wall at the given position"""
        grid_x = int(x // self.cell_size)
        grid_y = int(y // self.cell_size)
        
        if not (0 <= grid_x < self.width and 0 <= grid_y < self.height):
            return True  # Out of bounds is considered a wall
            
        cell_type = self.grid[grid_y][grid_x]
        
        if cell_type == CellType.WALL:
            return True
        elif cell_type == CellType.PATH:
            return False
        elif cell_type == CellType.SUPERPOSITION_WALL:
            # Find the corresponding superposition wall
            for wall in self.superposition_walls:
                if wall.x == grid_x and wall.y == grid_y:
                    # If player has superposition power-up, they can pass through
                    if player_has_superposition:
                        return False
                    return wall.is_solid
            return True  # Default to solid if wall not found
        
        return False
    
    def get_collision_rects(self, player_has_superposition: bool = False) -> List[pygame.Rect]:
        """Get collision rectangles for all solid walls"""
        rects = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.is_wall_at(x * self.cell_size + self.cell_size // 2, 
                                 y * self.cell_size + self.cell_size // 2, 
                                 player_has_superposition):
                    rect = pygame.Rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size
                    )
                    rects.append(rect)
        
        return rects
    
    def draw(self, screen):
        """Draw the maze"""
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                
                cell_type = self.grid[y][x]
                
                if cell_type == CellType.WALL:
                    pygame.draw.rect(screen, self.wall_color, rect)
                    # Add subtle border
                    pygame.draw.rect(screen, (150, 150, 200), rect, 1)
                    
                elif cell_type == CellType.PATH:
                    pygame.draw.rect(screen, self.path_color, rect)
                    
                elif cell_type == CellType.SUPERPOSITION_WALL:
                    # Find the corresponding superposition wall for visual effects
                    wall = None
                    for sw in self.superposition_walls:
                        if sw.x == x and sw.y == y:
                            wall = sw
                            break
                    
                    if wall:
                        # Create flickering effect
                        color = list(self.superposition_color)
                        alpha = wall.alpha
                        
                        # Create surface with alpha
                        surf = pygame.Surface((self.cell_size, self.cell_size))
                        surf.set_alpha(alpha)
                        surf.fill(color)
                        
                        # Draw base (path color)
                        pygame.draw.rect(screen, self.path_color, rect)
                        
                        # Draw superposition effect
                        screen.blit(surf, rect.topleft)
                        
                        # Add quantum "particles" effect
                        if wall.is_solid:
                            for i in range(3):
                                particle_x = rect.centerx + random.randint(-5, 5)
                                particle_y = rect.centery + random.randint(-5, 5)
                                pygame.draw.circle(screen, (255, 255, 255), 
                                                 (particle_x, particle_y), 1)
    
    def get_random_path_position(self) -> Tuple[int, int]:
        """Get a random position that's on a path"""
        path_positions = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == CellType.PATH:
                    path_positions.append((
                        x * self.cell_size + self.cell_size // 2,
                        y * self.cell_size + self.cell_size // 2
                    ))
        
        if path_positions:
            return random.choice(path_positions)
        else:
            # Fallback to center if no paths found
            return (self.width * self.cell_size // 2, self.height * self.cell_size // 2)
