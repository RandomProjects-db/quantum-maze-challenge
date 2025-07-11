import pygame
import os
from typing import Dict, Optional

class AudioManager:
    def __init__(self):
        # Initialize pygame mixer
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Audio initialization failed: {e}")
            self.audio_available = False
            return
        
        self.audio_available = True
        
        # Audio settings
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.muted = False
        
        # Storage for loaded sounds
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.current_music = None
        
        # Create sounds directory if it doesn't exist
        self.sounds_dir = "sounds"
        if not os.path.exists(self.sounds_dir):
            os.makedirs(self.sounds_dir)
            
        # Load all audio assets
        self._load_sounds()
        self._create_placeholder_sounds()
    
    def _load_sounds(self):
        """Load all sound files from the sounds directory"""
        if not self.audio_available:
            return
            
        sound_files = {
            'menu_music': 'menu_music.ogg',
            'game_music': 'game_music.ogg',
            'qubit_collect': 'qubit_collect.wav',
            'powerup_collect': 'powerup_collect.wav',
            'player_hit': 'player_hit.wav',
            'teleport': 'teleport.wav',
            'ghost_capture': 'ghost_capture.wav',
            'level_complete': 'level_complete.wav',
            'game_over': 'game_over.wav',
            'superposition_activate': 'superposition_activate.wav',
            'measurement_activate': 'measurement_activate.wav',
            'entanglement_activate': 'entanglement_activate.wav',
            'entangled_qubit_timer': 'entangled_qubit_timer.wav'
        }
        
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(self.sounds_dir, filename)
            if os.path.exists(filepath):
                try:
                    if filename.endswith('.ogg') or filename.endswith('.mp3'):
                        # Music files - don't load as Sound objects
                        continue
                    else:
                        self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                except pygame.error as e:
                    print(f"Could not load sound {filename}: {e}")
    
    def _create_placeholder_sounds(self):
        """Create simple placeholder sounds using pygame's sound generation"""
        if not self.audio_available:
            return
            
        try:
            import numpy as np
            numpy_available = True
        except ImportError:
            print("NumPy not available - using simple placeholder sounds")
            numpy_available = False
        
        # Create simple beep sounds as placeholders
        if numpy_available:
            self._create_numpy_sounds()
        else:
            self._create_simple_sounds()
    
    def _create_numpy_sounds(self):
        """Create sounds using numpy"""
        import numpy as np
        
        # Qubit collect - high pitched beep
        if 'qubit_collect' not in self.sounds:
            self.sounds['qubit_collect'] = self._generate_beep(800, 0.2)
        
        # Power-up collect - ascending tones
        if 'powerup_collect' not in self.sounds:
            self.sounds['powerup_collect'] = self._generate_chord([400, 500, 600], 0.3)
        
        # Player hit - low buzz
        if 'player_hit' not in self.sounds:
            self.sounds['player_hit'] = self._generate_buzz(200, 0.5)
        
        # Teleport - whoosh effect
        if 'teleport' not in self.sounds:
            self.sounds['teleport'] = self._generate_sweep(400, 800, 0.4)
        
        # Ghost capture - victory chime
        if 'ghost_capture' not in self.sounds:
            self.sounds['ghost_capture'] = self._generate_chord([600, 800, 1000], 0.4)
        
        # Level complete - fanfare
        if 'level_complete' not in self.sounds:
            self.sounds['level_complete'] = self._generate_chord([500, 625, 750, 1000], 0.8)
        
        # Game over - descending tones
        if 'game_over' not in self.sounds:
            self.sounds['game_over'] = self._generate_descending([400, 350, 300, 250], 1.0)
        
        # Power-up activation sounds
        if 'superposition_activate' not in self.sounds:
            self.sounds['superposition_activate'] = self._generate_sweep(300, 600, 0.3)
        
        if 'measurement_activate' not in self.sounds:
            self.sounds['measurement_activate'] = self._generate_beep(1000, 0.25)
        
        if 'entanglement_activate' not in self.sounds:
            self.sounds['entanglement_activate'] = self._generate_chord([400, 600], 0.4)
        
        if 'entangled_qubit_timer' not in self.sounds:
            self.sounds['entangled_qubit_timer'] = self._generate_beep(1200, 0.1)
    
    def _create_simple_sounds(self):
        """Create simple sounds without numpy"""
        # Create very basic placeholder sounds
        try:
            # Create a simple 1-second silence as placeholder
            sample_rate = 22050
            duration = 0.2
            frames = int(duration * sample_rate)
            
            # Create a simple array of zeros (silence)
            arr = [[0, 0] for _ in range(frames)]
            
            # Convert to the format pygame expects
            sound_array = []
            for frame in arr:
                sound_array.extend(frame)
            
            # Create a simple sound (just silence for now)
            placeholder_sound = pygame.mixer.Sound(buffer=bytes(len(sound_array) * 2))
            
            # Assign placeholder to all sound effects
            sound_names = [
                'qubit_collect', 'powerup_collect', 'player_hit', 'teleport',
                'ghost_capture', 'level_complete', 'game_over',
                'superposition_activate', 'measurement_activate',
                'entanglement_activate', 'entangled_qubit_timer'
            ]
            
            for sound_name in sound_names:
                if sound_name not in self.sounds:
                    self.sounds[sound_name] = placeholder_sound
                    
        except Exception as e:
            print(f"Could not create placeholder sounds: {e}")
    
    def _generate_beep(self, frequency: int, duration: float) -> pygame.mixer.Sound:
        """Generate a simple beep sound"""
        import numpy as np
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = np.sin(2 * np.pi * frequency * time)
            # Apply envelope to avoid clicks
            envelope = min(1.0, 4.0 * time, 4.0 * (duration - time))
            arr[i] = [wave * envelope * 0.3, wave * envelope * 0.3]
        
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _generate_chord(self, frequencies: list, duration: float) -> pygame.mixer.Sound:
        """Generate a chord with multiple frequencies"""
        import numpy as np
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = 0
            for freq in frequencies:
                wave += np.sin(2 * np.pi * freq * time) / len(frequencies)
            
            # Apply envelope
            envelope = min(1.0, 4.0 * time, 4.0 * (duration - time))
            arr[i] = [wave * envelope * 0.3, wave * envelope * 0.3]
        
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _generate_buzz(self, frequency: int, duration: float) -> pygame.mixer.Sound:
        """Generate a buzzing sound"""
        import numpy as np
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            # Square wave for buzz effect
            wave = 1 if np.sin(2 * np.pi * frequency * time) > 0 else -1
            envelope = min(1.0, 2.0 * time, 2.0 * (duration - time))
            arr[i] = [wave * envelope * 0.2, wave * envelope * 0.2]
        
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _generate_sweep(self, start_freq: int, end_freq: int, duration: float) -> pygame.mixer.Sound:
        """Generate a frequency sweep"""
        import numpy as np
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            progress = time / duration
            freq = start_freq + (end_freq - start_freq) * progress
            wave = np.sin(2 * np.pi * freq * time)
            envelope = min(1.0, 4.0 * time, 4.0 * (duration - time))
            arr[i] = [wave * envelope * 0.3, wave * envelope * 0.3]
        
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def _generate_descending(self, frequencies: list, duration: float) -> pygame.mixer.Sound:
        """Generate descending tones"""
        import numpy as np
        sample_rate = 22050
        total_frames = int(duration * sample_rate)
        frames_per_tone = total_frames // len(frequencies)
        
        arr = np.zeros((total_frames, 2))
        
        for tone_idx, freq in enumerate(frequencies):
            start_frame = tone_idx * frames_per_tone
            end_frame = min(start_frame + frames_per_tone, total_frames)
            
            for i in range(start_frame, end_frame):
                time = float(i - start_frame) / sample_rate
                tone_duration = frames_per_tone / sample_rate
                wave = np.sin(2 * np.pi * freq * time)
                envelope = min(1.0, 4.0 * time, 4.0 * (tone_duration - time))
                arr[i] = [wave * envelope * 0.3, wave * envelope * 0.3]
        
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        return sound
    
    def play_sound(self, sound_name: str, volume: float = 1.0):
        """Play a sound effect"""
        if not self.audio_available or self.muted or sound_name not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(self.sfx_volume * volume)
            sound.play()
        except Exception as e:
            print(f"Could not play sound {sound_name}: {e}")
    
    def play_music(self, music_name: str, loops: int = -1):
        """Play background music"""
        if not self.audio_available or self.muted:
            return
        
        music_file = None
        if music_name == 'menu':
            music_file = os.path.join(self.sounds_dir, 'menu_music.ogg')
        elif music_name == 'game':
            music_file = os.path.join(self.sounds_dir, 'game_music.ogg')
        
        if music_file and os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
                self.current_music = music_name
            except pygame.error as e:
                print(f"Could not play music {music_file}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        if not self.audio_available:
            return
        try:
            pygame.mixer.music.stop()
            self.current_music = None
        except Exception:
            pass
    
    def toggle_mute(self):
        """Toggle audio mute"""
        if not self.audio_available:
            return
            
        self.muted = not self.muted
        try:
            if self.muted:
                pygame.mixer.music.set_volume(0)
                for sound in self.sounds.values():
                    sound.set_volume(0)
            else:
                pygame.mixer.music.set_volume(self.music_volume)
                # Sounds will get their volume set when played
        except Exception:
            pass
    
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        if not self.audio_available:
            return
            
        self.music_volume = max(0.0, min(1.0, volume))
        if not self.muted:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except Exception:
                pass
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.audio_available:
            try:
                pygame.mixer.quit()
            except Exception:
                pass

# Global audio manager instance
audio_manager = AudioManager()
