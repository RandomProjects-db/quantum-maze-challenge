import time
from typing import Dict

class GameStats:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset all statistics for a new game"""
        self.start_time = time.time()
        self.score = 0
        self.qubits_collected = 0
        self.ghosts_dodged = 0
        self.powerups_used = 0
        self.levels_completed = 0
        self.teleportations = 0
        self.entanglements_completed = 0
        self.superposition_time = 0
        self.measurement_time = 0
        self.deaths = 0
        
        # Tracking variables
        self.last_ghost_encounter_time = 0
        self.ghost_encounter_threshold = 2.0  # 2 seconds
        
    def add_score(self, points: int):
        """Add points to score"""
        self.score += points
        
    def collect_qubit(self, is_entangled: bool = False):
        """Record qubit collection"""
        self.qubits_collected += 1
        if is_entangled:
            self.entanglements_completed += 1
            
    def use_powerup(self, powerup_type: str, duration: float = 0):
        """Record power-up usage"""
        self.powerups_used += 1
        
        if powerup_type == "superposition":
            self.superposition_time += duration
        elif powerup_type == "measurement":
            self.measurement_time += duration
            
    def complete_level(self):
        """Record level completion"""
        self.levels_completed += 1
        
    def player_death(self):
        """Record player death"""
        self.deaths += 1
        
    def teleport(self):
        """Record teleportation"""
        self.teleportations += 1
        
    def ghost_encounter(self, avoided: bool = True):
        """Record ghost encounter"""
        current_time = time.time()
        
        # Only count if enough time has passed since last encounter
        if current_time - self.last_ghost_encounter_time > self.ghost_encounter_threshold:
            if avoided:
                self.ghosts_dodged += 1
            self.last_ghost_encounter_time = current_time
            
    def get_survival_time(self) -> float:
        """Get total survival time in seconds"""
        return time.time() - self.start_time
        
    def get_stats_dict(self) -> Dict:
        """Get all stats as a dictionary"""
        return {
            'score': self.score,
            'qubits_collected': self.qubits_collected,
            'ghosts_dodged': self.ghosts_dodged,
            'powerups_used': self.powerups_used,
            'levels_completed': self.levels_completed,
            'survival_time': self.get_survival_time(),
            'teleportations': self.teleportations,
            'entanglements_completed': self.entanglements_completed,
            'superposition_time': self.superposition_time,
            'measurement_time': self.measurement_time,
            'deaths': self.deaths
        }
        
    def get_performance_rating(self) -> str:
        """Get a performance rating based on stats"""
        survival_time = self.get_survival_time()
        
        # Calculate performance score
        score_factor = min(self.score / 10000, 1.0)  # Max factor at 10k points
        survival_factor = min(survival_time / 300, 1.0)  # Max factor at 5 minutes
        level_factor = min(self.levels_completed / 10, 1.0)  # Max factor at 10 levels
        efficiency_factor = min(self.qubits_collected / max(1, self.deaths * 10), 1.0)
        
        performance = (score_factor + survival_factor + level_factor + efficiency_factor) / 4
        
        if performance >= 0.9:
            return "QUANTUM MASTER"
        elif performance >= 0.7:
            return "QUANTUM EXPERT"
        elif performance >= 0.5:
            return "QUANTUM ADEPT"
        elif performance >= 0.3:
            return "QUANTUM NOVICE"
        else:
            return "QUANTUM STUDENT"
