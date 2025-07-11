#!/usr/bin/env python3
"""
Quantum Notation Display Test
Demonstrates the quantum equation overlay system
"""

import pygame
import sys
from quantum_notation import QuantumNotationDisplay

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quantum Notation Test - Press Keys to See Equations!")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)

# Create quantum notation display
quantum_notation = QuantumNotationDisplay(SCREEN_WIDTH, SCREEN_HEIGHT)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Game loop
clock = pygame.time.Clock()
running = True

print("🌌 Quantum Notation Test Started!")
print("📋 Controls:")
print("  1 - Show Superposition Equation (2.5s duration)")
print("  2 - Show Entanglement (Bell State) (2.5s duration)")
print("  3 - Show Measurement Equation (1.8s duration)")
print("  4 - Show Tunneling Equation (1.5s duration)")
print("  5 - Show Quantum Gate/Operation (2.0s duration)")
print("  SPACE - Rapid fire test (multiple notifications)")
print("  ESC - Exit")
print("")
print("💡 TIP: Press keys rapidly to see stacking effect!")

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                print("🌀 Showing Superposition Equation!")
                quantum_notation.show_superposition_notification()
            elif event.key == pygame.K_2:
                print("🔗 Showing Entanglement (Bell State)!")
                quantum_notation.show_entanglement_notification()
            elif event.key == pygame.K_3:
                print("📏 Showing Measurement Equation!")
                quantum_notation.show_measurement_notification()
            elif event.key == pygame.K_4:
                print("🌀 Showing Tunneling Equation!")
                quantum_notation.show_tunneling_notification()
            elif event.key == pygame.K_5:
                print("⚛️ Showing Quantum Gate/Operation!")
                quantum_notation.show_quantum_gate_notification()
            elif event.key == pygame.K_SPACE:
                print("🚀 Rapid Fire Test - Multiple Notifications!")
                quantum_notation.show_superposition_notification()
                quantum_notation.show_entanglement_notification()
                quantum_notation.show_measurement_notification()
                quantum_notation.show_quantum_gate_notification()
    
    # Update quantum notation
    quantum_notation.update(dt)
    
    # Draw everything
    screen.fill(BLACK)
    
    # Draw title
    title_text = font.render("Quantum Notation Display Test", True, CYAN)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    
    # Draw instructions
    instructions = [
        "Press keys to see quantum equations:",
        "",
        "1 - Superposition: |+⟩ = 1/√2 (|0⟩ + |1⟩) [2.5s]",
        "2 - Entanglement: Bell States (random) [2.5s]",
        "3 - Measurement: Wave Function Collapse [1.8s]",
        "4 - Tunneling: Quantum Tunneling Probability [1.5s]",
        "5 - Quantum Gates: H, X, Z, CNOT & More [2.0s]",
        "",
        "SPACE - Rapid Fire Test (Multiple at once)",
        "ESC - Exit",
        "",
        "💡 Try pressing 1,2,5 rapidly to see stacking!"
    ]
    
    y_offset = 120
    for instruction in instructions:
        if instruction:  # Skip empty lines
            text = small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
        y_offset += 30
    
    # Draw quantum notation overlays (this is the magic!)
    quantum_notation.draw(screen)
    
    # Show active notifications count
    if quantum_notation.has_active_notifications():
        active_text = small_font.render(f"Active Notifications: {len(quantum_notation.active_notifications)}", 
                                      True, CYAN)
        screen.blit(active_text, (10, SCREEN_HEIGHT - 30))
    
    pygame.display.flip()

pygame.quit()
print("🌌 Quantum Notation Test Complete!")
