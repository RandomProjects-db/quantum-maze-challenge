#!/usr/bin/env python3
"""
Quantum Maze - Main Entry Point for Replit
AWS Build Games Challenge Entry
"""

import sys
import os

def main():
    print("🌌 QUANTUM MAZE - AWS Build Games Challenge")
    print("=" * 50)
    print("Built with Amazon Q Developer CLI")
    print()
    
    # Check if we can import pygame
    try:
        import pygame
        pygame_available = True
        print("✅ Pygame detected - Full game available!")
    except ImportError:
        pygame_available = False
        print("⚠️  Pygame not available - Running demo mode")
    
    print()
    print("🎮 Choose your experience:")
    print("1. 📱 Interactive Web Demo (Always works)")
    print("2. 🖥️ Full Game (Requires pygame)")
    print("3. 📋 Game Information")
    print()

    try:
        choice = input("Enter your choice (1, 2, or 3): ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = "1"  # Default to demo if input fails
        print("Defaulting to demo mode...")

    if choice == "2" and pygame_available:
        print("\n🚀 Starting Full Quantum Maze Game...")
        print("=" * 40)
        try:
            from quantum_maze import QuantumMazeGame
            game = QuantumMazeGame()
            game.run()
        except Exception as e:
            print(f"❌ Game failed to start: {e}")
            print("🔄 Falling back to demo mode...")
            choice = "1"
    
    if choice == "1" or (choice == "2" and not pygame_available):
        print("\n🚀 Starting Quantum Maze Web Demo...")
        print("=" * 40)
        try:
            from web_demo import QuantumMazeDemo
            demo = QuantumMazeDemo()
            demo.run_demo()
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            print("🔄 Showing basic info instead...")
            choice = "3"
    
    if choice == "3":
        show_game_info()

def show_game_info():
    print("\n📋 QUANTUM MAZE - Game Information")
    print("=" * 45)
    print()
    print("🎯 A quantum physics-enhanced retro maze game!")
    print("   Built entirely with Amazon Q Developer CLI")
    print()
    print("🌟 Features:")
    print("  ⚛️ Real quantum physics concepts (superposition, entanglement)")
    print("  🧠 Advanced AI with 3 ghost behavior types")
    print("  🎵 Dynamic audio system with procedural sounds")
    print("  🎨 Rich visual effects and particle systems")
    print("  📊 Comprehensive statistics tracking")
    print("  🌀 Quantum tunnels for teleportation")
    print("  🔗 Entangled qubits with time-based challenges")
    print()
    print("🎮 Gameplay:")
    print("  • Navigate quantum mazes as the Quantum Explorer")
    print("  • Collect qubits while avoiding Decoherence Ghosts")
    print("  • Use quantum power-ups: Superposition, Measurement, Entanglement")
    print("  • Experience unique quantum mechanics in real-time")
    print()
    print("💻 Technical Achievement:")
    print("  • Built using conversational AI programming")
    print("  • Amazon Q Developer CLI generated 90% of the code")
    print("  • Demonstrates AI-assisted game development")
    print("  • Educational quantum physics integration")
    print()
    print("🏆 AWS Build Games Challenge Entry")
    print("   Showcasing the power of AI-assisted development")
    print()
    print("📁 Repository: https://github.com/RandomProjects-db/quantum-maze-challenge")
    print("🎯 Challenge: #BuildGamesChallenge #AmazonQDevCLI")
    print()
    print("💡 To play the full game:")
    print("   1. Download from GitHub")
    print("   2. Install: pip install pygame numpy")
    print("   3. Run: python quantum_maze.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for checking out Quantum Maze!")
        print("🌌 May the quantum force be with you!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("📁 Full game available at: https://github.com/RandomProjects-db/quantum-maze-challenge")
        print("🏆 AWS Build Games Challenge - Built with Amazon Q Developer CLI")
