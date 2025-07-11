"""
Quantum Maze Game Configuration
Easy customization of game parameters
"""

# === DISPLAY SETTINGS ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# === MAZE SETTINGS ===
MAZE_WIDTH = 40          # Number of cells horizontally
MAZE_HEIGHT = 30         # Number of cells vertically  
CELL_SIZE = 20           # Size of each maze cell in pixels

# Superposition wall settings
SUPERPOSITION_WALL_CHANCE = 0.15  # 15% chance for walls to become superposition walls

# === PLAYER SETTINGS ===
PLAYER_SPEED = 3.0       # Player movement speed
PLAYER_RADIUS = 12       # Player collision radius

# Power-up durations (in seconds)
SUPERPOSITION_DURATION = 8.0
MEASUREMENT_DURATION = 5.0
ENTANGLEMENT_DURATION = 10.0

# === ENEMY SETTINGS ===
GHOST_SPEED = 1.5        # Base ghost movement speed
GHOST_RADIUS = 10        # Ghost collision radius

# Ghost behavior timings (in seconds)
CHASE_SCATTER_INTERVAL = 10.0    # How often ghosts switch between chase/scatter
FRIGHTENED_DURATION = 5.0        # How long ghosts stay frightened

# Ghost type distribution (when spawning multiple ghosts)
GHOST_TYPE_DISTRIBUTION = {
    'CHASER': 0.4,      # 40% chasers
    'WANDERER': 0.3,    # 30% wanderers  
    'GUARDIAN': 0.3     # 30% guardians
}

# === QUBIT SETTINGS ===
QUBITS_PER_LEVEL_BASE = 30       # Base number of qubits per level
QUBITS_PER_LEVEL_INCREMENT = 5   # Additional qubits per level
MAX_QUBITS_PER_LEVEL = 50        # Maximum qubits in any level

ENTANGLED_PAIRS_PER_LEVEL = 2    # Number of entangled qubit pairs per level
ENTANGLEMENT_TIME_LIMIT = 10.0   # Time to collect partner qubit (seconds)
ENTANGLEMENT_BONUS_POINTS = 100  # Bonus points for completing entanglement

# === POWER-UP SETTINGS ===
POWERUP_SPAWN_INTERVAL = 15.0    # Seconds between power-up spawns
MAX_POWERUPS_ON_SCREEN = 3       # Maximum simultaneous power-ups

# Power-up point values
POWERUP_POINTS = {
    'SUPERPOSITION': 50,
    'MEASUREMENT': 75,
    'ENTANGLEMENT': 100
}

# === TUNNEL SETTINGS ===
TUNNELS_PER_LEVEL = 1           # Number of tunnel pairs per level
TUNNEL_COOLDOWN = 1.0           # Cooldown between teleportations (seconds)

# === AUDIO SETTINGS ===
MUSIC_VOLUME = 0.7              # Background music volume (0.0 to 1.0)
SFX_VOLUME = 0.8                # Sound effects volume (0.0 to 1.0)

# === DIFFICULTY SETTINGS ===
# These affect how the game scales with levels

def get_enemy_count(level: int) -> int:
    """Calculate number of enemies for a given level"""
    return min(6, 2 + level)

def get_qubit_count(level: int) -> int:
    """Calculate number of qubits for a given level"""
    return min(MAX_QUBITS_PER_LEVEL, 
               QUBITS_PER_LEVEL_BASE + (level - 1) * QUBITS_PER_LEVEL_INCREMENT)

def get_ghost_speed_multiplier(level: int) -> float:
    """Get speed multiplier for ghosts based on level"""
    return min(1.5, 1.0 + (level - 1) * 0.05)  # 5% speed increase per level, max 50%

def get_powerup_spawn_rate_multiplier(level: int) -> float:
    """Get power-up spawn rate multiplier (higher = more frequent)"""
    return max(0.5, 1.0 - (level - 1) * 0.05)  # Slower spawn rate on higher levels

# === COLOR PALETTE ===
COLORS = {
    # UI Colors
    'PRIMARY': (0, 255, 255),       # Cyan
    'SECONDARY': (255, 255, 0),     # Yellow  
    'WARNING': (255, 100, 100),     # Red
    'SUCCESS': (100, 255, 100),     # Green
    'BACKGROUND': (0, 0, 0),        # Black
    
    # Game Object Colors
    'QUANTUM_BLUE': (0, 150, 255),
    'QUBIT_GOLD': (255, 215, 0),
    'SUPERPOSITION_GREEN': (0, 255, 150),
    'DECOHERENCE_RED': (255, 50, 50),
    'MEASUREMENT_YELLOW': (255, 255, 0),
    'ENTANGLEMENT_MAGENTA': (255, 0, 255),
    
    # Maze Colors
    'WALL': (100, 100, 150),
    'PATH': (20, 20, 40),
    'SUPERPOSITION_WALL': (0, 255, 150)
}

# === CUSTOMIZATION HELPERS ===

def set_difficulty(difficulty: str):
    """Set predefined difficulty levels"""
    global GHOST_SPEED, POWERUP_SPAWN_INTERVAL, ENTANGLEMENT_TIME_LIMIT
    
    if difficulty.upper() == 'EASY':
        GHOST_SPEED = 1.2
        POWERUP_SPAWN_INTERVAL = 12.0
        ENTANGLEMENT_TIME_LIMIT = 15.0
    elif difficulty.upper() == 'NORMAL':
        GHOST_SPEED = 1.5
        POWERUP_SPAWN_INTERVAL = 15.0
        ENTANGLEMENT_TIME_LIMIT = 10.0
    elif difficulty.upper() == 'HARD':
        GHOST_SPEED = 1.8
        POWERUP_SPAWN_INTERVAL = 20.0
        ENTANGLEMENT_TIME_LIMIT = 7.0
    elif difficulty.upper() == 'QUANTUM':
        GHOST_SPEED = 2.0
        POWERUP_SPAWN_INTERVAL = 25.0
        ENTANGLEMENT_TIME_LIMIT = 5.0

def set_maze_size(width: int, height: int):
    """Set custom maze dimensions"""
    global MAZE_WIDTH, MAZE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
    
    MAZE_WIDTH = width
    MAZE_HEIGHT = height
    SCREEN_WIDTH = width * CELL_SIZE
    SCREEN_HEIGHT = height * CELL_SIZE

def enable_debug_mode():
    """Enable debug features"""
    global DEBUG_MODE
    DEBUG_MODE = True

# === DEBUG SETTINGS ===
DEBUG_MODE = False              # Enable debug features
SHOW_PATHFINDING = False        # Show ghost pathfinding
SHOW_COLLISION_BOXES = False    # Show collision rectangles
INVINCIBLE_PLAYER = False       # Player cannot be hurt

# === SOUND FILE PATHS ===
# These can be easily swapped out for different audio assets
SOUND_FILES = {
    'menu_music': 'sounds/menu_music.ogg',
    'game_music': 'sounds/game_music.ogg',
    'qubit_collect': 'sounds/qubit_collect.wav',
    'powerup_collect': 'sounds/powerup_collect.wav',
    'player_hit': 'sounds/player_hit.wav',
    'teleport': 'sounds/teleport.wav',
    'ghost_capture': 'sounds/ghost_capture.wav',
    'level_complete': 'sounds/level_complete.wav',
    'game_over': 'sounds/game_over.wav',
    'superposition_activate': 'sounds/superposition_activate.wav',
    'measurement_activate': 'sounds/measurement_activate.wav',
    'entanglement_activate': 'sounds/entanglement_activate.wav',
    'entangled_qubit_timer': 'sounds/entangled_qubit_timer.wav'
}

# === EXAMPLE USAGE ===
"""
# To customize the game, modify this file or use the helper functions:

# Set difficulty
set_difficulty('HARD')

# Custom maze size  
set_maze_size(50, 40)  # Larger maze

# Adjust specific settings
PLAYER_SPEED = 4.0     # Faster player
GHOST_SPEED = 1.0      # Slower ghosts
QUBITS_PER_LEVEL_BASE = 20  # Fewer qubits

# Change colors
COLORS['QUANTUM_BLUE'] = (100, 200, 255)  # Lighter blue

# Swap sound files
SOUND_FILES['game_music'] = 'sounds/my_custom_music.ogg'
"""
