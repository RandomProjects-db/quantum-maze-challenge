import pygame
import sys
import random
import math
from enum import Enum

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GOLD = (255, 215, 0)
RED = (255, 50, 50)
GREEN = (0, 255, 150)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 12
        self.speed = 3.0
        
    def update(self, keys):
        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            
        # Keep player on screen
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
    
    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)
        # Draw quantum effect
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 4)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Qubit:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 8
        self.collected = False
        self.rotation = 0
        
    def update(self, dt):
        self.rotation += dt * 2
        
    def draw(self, screen):
        if self.collected:
            return
            
        # Draw glowing qubit
        pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), self.radius)
        
        # Draw rotating effect
        for i in range(4):
            angle = self.rotation + (i * math.pi / 2)
            end_x = self.x + math.cos(angle) * (self.radius - 2)
            end_y = self.y + math.sin(angle) * (self.radius - 2)
            pygame.draw.line(screen, WHITE, (int(self.x), int(self.y)), 
                           (int(end_x), int(end_y)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

class Ghost:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 10
        self.speed = 1.5
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        
    def update(self, dt, player):
        # Simple AI - move toward player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
        # Keep on screen
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
    
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        # Draw eyes
        pygame.draw.circle(screen, WHITE, (int(self.x - 3), int(self.y - 2)), 2)
        pygame.draw.circle(screen, WHITE, (int(self.x + 3), int(self.y - 2)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

class SimpleQuantumMaze:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple Quantum Maze")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.MENU
        
        # Game variables
        self.score = 0
        self.lives = 3
        
        # Game objects
        self.player = None
        self.qubits = []
        self.ghosts = []
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def start_new_game(self):
        """Start a new game"""
        self.game_state = GameState.PLAYING
        self.score = 0
        self.lives = 3
        
        # Create player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Create qubits
        self.qubits = []
        for _ in range(20):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.qubits.append(Qubit(x, y))
        
        # Create ghosts
        self.ghosts = []
        for _ in range(3):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.ghosts.append(Ghost(x, y))
    
    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GameState.MENU:
                        self.start_new_game()
                    elif self.game_state == GameState.GAME_OVER:
                        self.game_state = GameState.MENU
                elif event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PLAYING:
                        self.game_state = GameState.MENU
    
    def update(self):
        """Update game logic"""
        if self.game_state == GameState.PLAYING and self.player:
            dt = self.clock.get_time() / 1000.0
            
            # Update player
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            
            # Update qubits
            for qubit in self.qubits:
                qubit.update(dt)
            
            # Update ghosts
            for ghost in self.ghosts:
                ghost.update(dt, self.player)
            
            # Check qubit collection
            player_rect = self.player.get_rect()
            for qubit in self.qubits:
                if not qubit.collected and player_rect.colliderect(qubit.get_rect()):
                    qubit.collected = True
                    self.score += 10
            
            # Check ghost collision
            for ghost in self.ghosts:
                if player_rect.colliderect(ghost.get_rect()):
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_state = GameState.GAME_OVER
                    else:
                        # Reset player position
                        self.player.x = SCREEN_WIDTH // 2
                        self.player.y = SCREEN_HEIGHT // 2
            
            # Check win condition
            if all(qubit.collected for qubit in self.qubits):
                self.game_state = GameState.GAME_OVER  # Could add a win state
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.PLAYING:
            self.draw_game()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw menu"""
        title = self.font.render("SIMPLE QUANTUM MAZE", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        instruction = self.small_font.render("Press SPACE to start", True, WHITE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(instruction, instruction_rect)
        
        controls = [
            "Arrow Keys or WASD - Move",
            "Collect gold qubits, avoid red ghosts",
            "ESC - Return to menu"
        ]
        
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 350 + i * 30))
            self.screen.blit(text, text_rect)
    
    def draw_game(self):
        """Draw game"""
        # Draw qubits
        for qubit in self.qubits:
            qubit.draw(self.screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw player
        if self.player:
            self.player.draw(self.screen)
        
        # Draw UI
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        lives_text = self.small_font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 40))
        
        remaining = sum(1 for q in self.qubits if not q.collected)
        qubits_text = self.small_font.render(f"Qubits: {remaining}", True, WHITE)
        self.screen.blit(qubits_text, (10, 70))
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BLACK)
        
        game_over = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(game_over, game_over_rect)
        
        score = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(score, score_rect)
        
        restart = self.small_font.render("Press SPACE to return to menu", True, WHITE)
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(restart, restart_rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SimpleQuantumMaze()
    game.run()
