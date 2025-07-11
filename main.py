#!/usr/bin/env python3
"""
Quantum Maze - Main Entry Point for Replit
"""

print("🌌 QUANTUM MAZE - AWS Build Games Challenge")
print("=" * 50)
print()
print("🎮 Choose your experience:")
print("1. 📱 Interactive Web Demo (Works in Replit)")
print("2. 🖥️ Full Game Info (Download required)")
print()

choice = input("Enter your choice (1 or 2): ").strip()

if choice == "1":
    print("\n🚀 Starting Quantum Maze Web Demo...")
    print("=" * 40)
    from web_demo import QuantumMazeDemo
    demo = QuantumMazeDemo()
    demo.run_demo()
    
elif choice == "2":
    print("\n📋 QUANTUM MAZE - Full Game Information")
    print("=" * 45)
    print()
    print("🎯 This is a complete quantum physics-enhanced maze game!")
    print("   Built entirely with Amazon Q Developer CLI")
    print()
    print("🌟 Features:")
    print("  ⚛️ Real quantum physics concepts")
    print("  🧠 Advanced AI with 3 ghost behavior types")
    print("  🎵 Dynamic audio system")
    print("  🎨 Rich visual effects")
    print("  📊 Comprehensive statistics")
    print()
    print("💻 To play the full game:")
    print("  1. Download from: https://github.com/RandomProjects-db/quantum-maze-challenge")
    print("  2. Install pygame: pip install pygame numpy")
    print("  3. Run: python quantum_maze.py")
    print()
    print("🏆 Built for AWS Build Games Challenge")
    print("   #BuildGamesChallenge #AmazonQDevCLI")
    
else:
    print("🚀 Starting Web Demo by default...")
    from web_demo import QuantumMazeDemo
    demo = QuantumMazeDemo()
    demo.run_demo()
