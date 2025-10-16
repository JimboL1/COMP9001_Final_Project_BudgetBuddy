#!/usr/bin/env python3
"""
Create a cool ASCII art style screenshot for BudgetBuddy
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np

def create_ascii_screenshot():
    """Create a cool ASCII art style screenshot"""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Dark terminal background
    terminal_bg = Rectangle((0, 0), 18, 12, facecolor='#0A0A0A', edgecolor='none')
    ax.add_patch(terminal_bg)
    
    # Terminal window
    window_bg = FancyBboxPatch((1, 1), 16, 10, boxstyle="round,pad=0.2", 
                              facecolor='#1A1A1A', edgecolor='#333333', linewidth=2)
    ax.add_patch(window_bg)
    
    # Terminal header
    header_bg = Rectangle((1, 10.2), 16, 0.8, facecolor='#2A2A2A', edgecolor='#333333', linewidth=1)
    ax.add_patch(header_bg)
    
    # ASCII art title
    ascii_title = """
    ╔══════════════════════════════════════════════════════════════╗
    ║  ██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗████████╗██████╗  ║
    ║  ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗ ║
    ║  ██████╔╝██║   ██║██║  ██║██║  ██║█████╗     ██║   ██████╔╝ ║
    ║  ██╔══██╗██║   ██║██║  ██║██║  ██║██╔══╝     ██║   ██╔══██╗ ║
    ║  ██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗   ██║   ██║  ██║ ║
    ║  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ║
    ║                                                                ║
    ║              Smart Student Budgeting Tool                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    # Terminal content
    terminal_content = """
    ┌─────────────────────────────────────────────────────────────┐
    │  🎯 Welcome to BudgetBuddy - Your Financial Companion!     │
    │  ========================================================= │
    │                                                             │
    │  📋 Main Menu:                                             │
    │     1. 💰 Set up budget (50/30/20 rule)                   │
    │     2. 💸 Add expense                                      │
    │     3. 📊 View monthly summary                             │
    │     4. 🧠 Check overspending & get suggestions            │
    │     5. 📈 Create spending chart                           │
    │     6. 📤 Export data                                      │
    │     7. 🚪 Exit                                             │
    │                                                             │
    │  Enter your choice (1-7): 2                                │
    │                                                             │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 💸 Add Expense                                      │   │
    │  │ Category: groceries                                 │   │
    │  │ Amount: $45.50                                      │   │
    │  │ Description: Weekly grocery shopping                 │   │
    │  │ ✅ Expense added successfully!                      │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 🧠 Smart Suggestions:                              │   │
    │  │ • You are within budget for groceries this month    │   │
    │  │ • Consider meal planning to reduce food waste      │   │
    │  │ • Track your spending patterns for better insights │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  🟢 Status: Ready  🔒 Data: Local  🛡️ Privacy: Secure    │
    └─────────────────────────────────────────────────────────────┘
    """
    
    # Add the ASCII art
    ax.text(9, 9.5, ascii_title, ha='center', va='center', 
            fontsize=8, color='#00FF00', fontfamily='monospace')
    
    # Add terminal content
    ax.text(2, 7.5, terminal_content, ha='left', va='top', 
            fontsize=9, color='#00FF00', fontfamily='monospace')
    
    # Add some cool effects
    # Glowing dots
    for i in range(20):
        x = np.random.uniform(1, 17)
        y = np.random.uniform(1, 11)
        circle = plt.Circle((x, y), 0.05, facecolor='#00FF00', alpha=0.3)
        ax.add_patch(circle)
    
    # Matrix-style rain effect
    for i in range(10):
        x = np.random.uniform(1, 17)
        y = np.random.uniform(1, 11)
        ax.text(x, y, '01', fontsize=6, color='#00FF00', alpha=0.2, 
                fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig('budgetbuddy_ascii_screenshot.png', dpi=300, bbox_inches='tight', 
                facecolor='#0A0A0A', edgecolor='none')
    plt.show()
    
    print("✅ ASCII screenshot saved as 'budgetbuddy_ascii_screenshot.png'")

if __name__ == "__main__":
    create_ascii_screenshot()
