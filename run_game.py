#!/usr/bin/env python3
"""
Quantum Maze Game Launcher
Simple launcher with error handling
"""

import sys
import os

def main():
    print("🌌 Quantum Maze - Enhanced Edition 🌌")
    print("=====================================")
    
    try:
        # Check if we're in the right directory
        if not os.path.exists('quantum_maze.py'):
            print("❌ Error: quantum_maze.py not found!")
            print("Please run this script from the game directory.")
            return 1
        
        # Try to import required modules
        try:
            import pygame
            print("✅ Pygame found")
        except ImportError:
            print("❌ Error: Pygame not installed!")
            print("Install with: pip install pygame")
            return 1
        
        try:
            import numpy
            print("✅ NumPy found")
        except ImportError:
            print("⚠️  Warning: NumPy not found - using basic audio")
        
        # Import and run the game
        print("🚀 Starting Quantum Maze...")
        print("\nControls:")
        print("  Arrow Keys/WASD - Move")
        print("  SPACE - Start game")
        print("  ESC - Pause/Menu")
        print("  M - Toggle audio")
        print("  Q/E - Test power-ups")
        print("\n" + "="*40)
        
        from quantum_maze import QuantumMaze
        game = QuantumMaze()
        game.run()
        
    except KeyboardInterrupt:
        print("\n👋 Thanks for playing Quantum Maze!")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting game: {e}")
        print("\nTrying simple version instead...")
        
        try:
            from simple_quantum_maze import SimpleQuantumMaze
            game = SimpleQuantumMaze()
            game.run()
        except Exception as e2:
            print(f"❌ Simple version also failed: {e2}")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
