import pygame
import sys
import math
from enum import Enum
from typing import List, Tuple, Optional
from player import QuantumExplorer
from maze import Maze
from qubits import QubitManager
from enemies import EnemyManager
from powerups import PowerUpManager
from tunnels import TunnelManager
from hud import RetroHUD
from simple_separated_hud import SimpleSeparatedHUD
from stats import GameStats
from audio import audio_manager
from quantum_notation import QuantumNotationDisplay
import config

# Initialize Pygame
pygame.init()

# Game Constants (from config)
SCREEN_WIDTH = config.SCREEN_WIDTH
SCREEN_HEIGHT = config.SCREEN_HEIGHT
FPS = config.FPS

# Colors (from config)
BLACK = config.COLORS['BACKGROUND']
WHITE = (255, 255, 255)
QUANTUM_BLUE = config.COLORS['QUANTUM_BLUE']
QUANTUM_PURPLE = (150, 0, 255)
QUBIT_GOLD = config.COLORS['QUBIT_GOLD']
DECOHERENCE_RED = config.COLORS['DECOHERENCE_RED']
SUPERPOSITION_GREEN = config.COLORS['SUPERPOSITION_GREEN']

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class QuantumMaze:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Quantum Maze - AWS Build Games Challenge")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = GameState.MENU
        
        # Game variables
        self.score = 0
        self.lives = 3
        self.level = 1
        
        # Game over countdown
        self.game_over_timer = 0
        self.game_over_duration = 10.0  # 10 seconds countdown
        
        # Game objects
        self.player = None
        self.maze = None
        self.qubit_manager = QubitManager()
        self.enemy_manager = EnemyManager()
        self.powerup_manager = PowerUpManager()
        self.tunnel_manager = TunnelManager()
        self.hud = SimpleSeparatedHUD(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.stats = GameStats()
        self.quantum_notation = QuantumNotationDisplay(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dt = 0
        
        # Level transition
        self.level_complete_timer = 0
        self.level_complete_duration = 2.0
        self.showing_level_complete = False
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Start menu music
        audio_manager.play_music('menu')
        
    def create_hud_adjusted_maze(self):
        """Create a maze with dimensions adjusted for HUD space"""
        available_height = self.hud.game_area_height
        adjusted_maze_height = min(config.MAZE_HEIGHT, available_height // config.CELL_SIZE)
        return Maze(config.MAZE_WIDTH, adjusted_maze_height, config.CELL_SIZE)
        
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PLAYING:
                        self.game_state = GameState.PAUSED
                    elif self.game_state == GameState.PAUSED:
                        self.game_state = GameState.PLAYING
                    elif self.game_state == GameState.GAME_OVER:
                        self.reset_game()  # Return to menu from game over
                elif event.key == pygame.K_SPACE:
                    if self.game_state == GameState.MENU:
                        self.start_new_game()
                    elif self.game_state == GameState.GAME_OVER:
                        self.start_new_game()  # Restart game from game over
                elif event.key == pygame.K_m:
                    # Toggle audio mute
                    audio_manager.toggle_mute()
                # Test power-up activation (temporary for testing)
                elif event.key == pygame.K_q and self.player:
                    self.player.activate_superposition()
                    audio_manager.play_sound('superposition_activate')
                    self.stats.use_powerup('superposition', config.SUPERPOSITION_DURATION)
                    # Show quantum notation for superposition
                    self.quantum_notation.show_superposition_notification()
                elif event.key == pygame.K_e and self.player:
                    self.player.activate_measurement()
                    audio_manager.play_sound('measurement_activate')
                    # Also frighten enemies when measurement is activated
                    self.enemy_manager.set_frightened_mode()
                    self.stats.use_powerup('measurement', config.MEASUREMENT_DURATION)
                    # Show quantum notation for measurement
                    self.quantum_notation.show_measurement_notification()
    
    def start_new_game(self):
        """Initialize a new game"""
        self.game_state = GameState.PLAYING
        self.score = 0
        self.lives = 3
        self.level = 1
        self.showing_level_complete = False
        
        # Reset statistics
        self.stats.reset()
        
        # Create maze using HUD-adjusted dimensions to prevent overlap
        self.maze = self.create_hud_adjusted_maze()
        
        # Initialize player at a random path position
        start_x, start_y = self.maze.get_random_path_position()
        self.player = QuantumExplorer(start_x, start_y)
        
        # Generate qubits with entangled pairs
        qubit_count = config.get_qubit_count(self.level)
        self.qubit_manager.generate_qubits(self.maze, qubit_count, config.ENTANGLED_PAIRS_PER_LEVEL)
        
        # Spawn enemies
        enemy_count = config.get_enemy_count(self.level)
        self.enemy_manager.spawn_ghosts(self.maze, enemy_count)
        
        # Clear power-ups and tunnels
        self.powerup_manager.clear()
        self.tunnel_manager.clear()
        
        # Create quantum tunnels
        self.tunnel_manager.create_tunnel_pair(self.maze, 0)
        
        # Start game music
        audio_manager.stop_music()
        audio_manager.play_music('game')
        
    def reset_game(self):
        """Reset game to menu state"""
        self.game_state = GameState.MENU
        
    def update(self):
        """Update game logic based on current state"""
        # Update HUD animations
        self.hud.update(self.dt)
        
        # Update quantum notation display
        self.quantum_notation.update(self.dt)
        
        if self.game_state == GameState.PLAYING and self.player and self.maze:
            # Handle level complete display
            if self.showing_level_complete:
                self.level_complete_timer -= self.dt
                if self.level_complete_timer <= 0:
                    self.showing_level_complete = False
                return
            
            # Handle continuous input (movement)
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            
            # Update maze (superposition walls)
            self.maze.update(self.dt)
            
            # Update player with maze collision
            self.player.update(self.dt, self.maze)
            
            # Update qubits
            self.qubit_manager.update(self.dt)
            
            # Update enemies with qubits for guardian AI
            entangled_qubits = self.qubit_manager.get_entangled_qubits()
            self.enemy_manager.update(self.dt, self.maze, self.player, entangled_qubits)
            
            # Update power-ups
            self.powerup_manager.update(self.dt, self.maze)
            
            # Update tunnels
            self.tunnel_manager.update(self.dt)
            
            # Check qubit collection
            points_earned, entanglement_activated = self.qubit_manager.check_collection(self.player.get_rect())
            if points_earned > 0:
                self.score += points_earned
                self.stats.add_score(points_earned)
                self.stats.collect_qubit(entanglement_activated)
                audio_manager.play_sound('qubit_collect')
                
                if entanglement_activated:
                    audio_manager.play_sound('entangled_qubit_timer')
                    # Show quantum notation for entanglement
                    self.quantum_notation.show_entanglement_notification()
                else:
                    # Show quantum gate/operation for single qubit collection
                    self.quantum_notation.show_quantum_gate_notification()
            
            # Check power-up collection
            powerup_points, collected_types = self.powerup_manager.check_collection(self.player.get_rect(), self.player)
            if powerup_points > 0:
                self.score += powerup_points
                self.stats.add_score(powerup_points)
                self.stats.use_powerup('collected')
                audio_manager.play_sound('powerup_collect')
                
                # Show quantum notation based on collected power-up types
                from powerups import PowerUpType
                for power_type in collected_types:
                    if power_type == PowerUpType.SUPERPOSITION:
                        self.quantum_notation.show_superposition_notification()
                    elif power_type == PowerUpType.MEASUREMENT:
                        self.quantum_notation.show_measurement_notification()
                    elif power_type == PowerUpType.ENTANGLEMENT:
                        self.quantum_notation.show_entanglement_notification()
            
            # Check teleportation
            if self.tunnel_manager.check_teleportation(self.player.get_rect(), self.player):
                self.stats.teleport()
                audio_manager.play_sound('teleport')
                # Show quantum notation for tunneling
                self.quantum_notation.show_tunneling_notification()
            
            # Apply entanglement power-up effects to enemies
            entanglement_powerups = self.powerup_manager.get_entanglement_powerups()
            if entanglement_powerups:
                self.enemy_manager.set_frightened_mode(8.0)
            
            # Check enemy collision
            if self.enemy_manager.check_collision(self.player.get_rect(), self.player.has_measurement):
                if not config.INVINCIBLE_PLAYER:  # Debug option
                    self.player_hit()
            else:
                # Player avoided ghosts
                self.stats.ghost_encounter(avoided=True)
            
            # Check if level is complete
            if self.qubit_manager.all_collected():
                self.next_level()
            
        elif self.game_state == GameState.PAUSED:
            # Game is paused, no updates needed
            pass
        elif self.game_state == GameState.GAME_OVER:
            # Handle game over countdown
            if self.game_over_timer > 0:
                self.game_over_timer -= self.dt
                if self.game_over_timer <= 0:
                    # Auto return to menu after countdown
                    self.reset_game()
            
    def draw_menu(self):
        """Draw the main menu"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font.render("QUANTUM MAZE", True, QUANTUM_BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.small_font.render("Navigate quantum realms, collect qubits, avoid decoherence!", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instructions
        instructions = [
            "SPACE - Start Game",
            "Arrow Keys / WASD - Move",
            "ESC - Pause/Menu",
            "M - Toggle Audio",
            "",
            "Q - Superposition (Test)",
            "E - Measurement (Test)"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction:  # Skip empty lines
                text = self.small_font.render(instruction, True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 280 + i * 25))
                self.screen.blit(text, text_rect)
        
        # Audio status
        audio_status = "Audio: ON" if not audio_manager.muted else "Audio: OFF"
        audio_text = self.small_font.render(audio_status, True, SUPERPOSITION_GREEN if not audio_manager.muted else DECOHERENCE_RED)
        audio_rect = audio_text.get_rect(center=(SCREEN_WIDTH//2, 500))
        self.screen.blit(audio_text, audio_rect)
            
    def next_level(self):
        """Advance to the next level"""
        self.level += 1
        self.stats.complete_level()
        self.showing_level_complete = True
        self.level_complete_timer = self.level_complete_duration
        
        # Play level complete sound
        audio_manager.play_sound('level_complete')
        
        # Create new maze with HUD-adjusted dimensions (same as start_new_game)
        self.maze = self.create_hud_adjusted_maze()
        
        # Reset player position
        start_x, start_y = self.maze.get_random_path_position()
        self.player.x, self.player.y = start_x, start_y
        
        # Generate more qubits for higher levels
        qubit_count = config.get_qubit_count(self.level)
        self.qubit_manager.generate_qubits(self.maze, qubit_count, config.ENTANGLED_PAIRS_PER_LEVEL)
        
        # Spawn more enemies for higher levels
        enemy_count = config.get_enemy_count(self.level)
        self.enemy_manager.spawn_ghosts(self.maze, enemy_count)
        
        # Clear power-ups and tunnels for new level
        self.powerup_manager.clear()
        self.tunnel_manager.clear()
        
        # Create new quantum tunnels
        self.tunnel_manager.create_tunnel_pair(self.maze, 0)
        
    def player_hit(self):
        """Handle player being hit by enemy"""
        self.lives -= 1
        self.stats.player_death()
        
        # Play hit sound
        audio_manager.play_sound('player_hit')
        
        if self.lives <= 0:
            self.game_state = GameState.GAME_OVER
            self.game_over_timer = self.game_over_duration  # Start countdown
            # Play game over sound and stop music
            audio_manager.play_sound('game_over')
            audio_manager.stop_music()
        else:
            # Reset player position
            start_x, start_y = self.maze.get_random_path_position()
            self.player.x, self.player.y = start_x, start_y
            
            # Brief invincibility could be added here
    
    def draw_game(self):
        """Draw the main game screen"""
        self.screen.fill(BLACK)
        
        # Set clipping to game area to prevent overlap with HUD
        game_area_rect = pygame.Rect(0, 0, SCREEN_WIDTH, self.hud.game_area_height)
        self.screen.set_clip(game_area_rect)
        
        # Draw game content within clipped area
        if self.maze:
            self.maze.draw(self.screen)
        
        self.tunnel_manager.draw(self.screen)
        self.qubit_manager.draw(self.screen)
        self.powerup_manager.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        
        if self.player:
            self.player.draw(self.screen)
        
        # Reset clipping for HUD drawing
        self.screen.set_clip(None)
        
        # Get timer values
        entanglement_timer = self.qubit_manager.get_entanglement_timer() if hasattr(self.qubit_manager, 'get_entanglement_timer') else 0
        superposition_timer = self.player.superposition_timer if self.player and hasattr(self.player, 'superposition_timer') else 0
        measurement_timer = self.player.measurement_timer if self.player and hasattr(self.player, 'measurement_timer') else 0
        
        # Get qubit counts
        total_qubits = len(self.qubit_manager.qubits) if hasattr(self.qubit_manager, 'qubits') else 0
        collected_qubits = total_qubits - self.qubit_manager.get_remaining_count() if hasattr(self.qubit_manager, 'get_remaining_count') else 0
        
        # Draw the simple separated HUD
        self.hud.draw(self.screen, self.score, self.lives, self.level, 
                     collected_qubits, total_qubits,
                     entanglement_timer, superposition_timer, measurement_timer)
        
        # Draw level complete overlay
        if self.showing_level_complete:
            bonus_points = 100 * self.level
            stats_dict = {
                'Qubits Collected': collected_qubits,
                'Total Qubits': total_qubits,
                'Level Bonus': bonus_points
            }
            self.hud.draw_level_complete_overlay(self.screen, self.score, stats_dict, self.level)
        
    def draw_ui(self):
        """Draw game UI elements"""
        # Score
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Lives
        lives_text = self.small_font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 40))
        
        # Level
        level_text = self.small_font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 70))
        
        # Remaining qubits
        remaining = self.qubit_manager.get_remaining_count()
        qubits_text = self.small_font.render(f"Qubits: {remaining}", True, QUBIT_GOLD)
        self.screen.blit(qubits_text, (SCREEN_WIDTH - 120, 10))
        
        # Player power-up indicators
        if self.player:
            self.player.draw_ui_indicators(self.screen, self.small_font)
            
        # Test controls (temporary)
        if self.game_state == GameState.PLAYING:
            controls_text = self.small_font.render("Q - Superposition | E - Measurement", True, (128, 128, 128))
            self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
        
    def draw_pause_screen(self):
        """Draw pause overlay"""
        self.hud.draw_pause_overlay(self.screen)
        
    def draw_game_over(self):
        """Draw game over screen"""
        # Draw the game state first (faded)
        self.draw_game()
        
        # Get comprehensive stats
        stats_dict = self.stats.get_stats_dict() if hasattr(self.stats, 'get_stats_dict') else {}
        
        # Add performance rating to stats
        if hasattr(self.stats, 'get_performance_rating'):
            stats_dict['performance_rating'] = self.stats.get_performance_rating()
        
        # Draw game over overlay with countdown
        self.hud.draw_game_over_overlay(self.screen, self.score, stats_dict, self.game_over_timer)
        
    def draw(self):
        """Main drawing method"""
        if self.game_state == GameState.MENU:
            self.draw_menu()
        elif self.game_state == GameState.PLAYING:
            self.draw_game()
        elif self.game_state == GameState.PAUSED:
            self.draw_game()  # Draw game first
            self.draw_pause_screen()  # Then overlay pause screen
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        
        # Draw quantum notation overlays on top of everything
        self.quantum_notation.draw(self.screen)
            
        pygame.display.flip()
        
    def reset_game(self):
        """Reset game to menu state"""
        self.game_state = GameState.MENU
        # Start menu music
        audio_manager.stop_music()
        audio_manager.play_music('menu')
        
    def cleanup(self):
        """Clean up resources"""
        audio_manager.cleanup()
        
    def run(self):
        """Main game loop"""
        try:
            while self.running:
                # Calculate delta time for smooth animations
                self.dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
                
                self.handle_events()
                self.update()
                self.draw()
                
        finally:
            self.cleanup()
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    game = QuantumMaze()
    game.run()
