from pydub.generators import Sine
from pydub import AudioSegment

# Generate simple menu music
menu_music = Sine(440).to_audio_segment(duration=5000).fade_in(500).fade_out(500)
menu_music.export("menu_music.ogg", format="ogg")

# Generate game music
game_music = Sine(880).to_audio_segment(duration=5000).fade_in(500).fade_out(500)
game_music.export("game_music.ogg", format="ogg")

# Generate qubit collect (short beep)
collect_sfx = Sine(1200).to_audio_segment(duration=200)
collect_sfx.export("qubit_collect.wav", format="wav")

# Generate teleport sound (quick high-to-low tone)
teleport = Sine(1800).to_audio_segment(duration=100) + Sine(900).to_audio_segment(duration=100)
teleport.export("teleport.wav", format="wav")

