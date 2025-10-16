#!/usr/bin/env python3
"""
Create a cool, modern screenshot for BudgetBuddy
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
import numpy as np

def create_cool_screenshot():
    """Create a cool, modern screenshot of BudgetBuddy"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Modern dark theme background
    dark_bg = Rectangle((0, 0), 16, 10, facecolor='#0D1117', edgecolor='none')
    ax.add_patch(dark_bg)
    
    # Terminal window with modern styling
    terminal_bg = FancyBboxPatch((1, 1), 14, 8, boxstyle="round,pad=0.3", 
                                 facecolor='#161B22', edgecolor='#30363D', linewidth=2)
    ax.add_patch(terminal_bg)
    
    # Terminal header with gradient effect
    header_bg = FancyBboxPatch((1, 8.2), 14, 0.8, boxstyle="round,pad=0.1", 
                              facecolor='#21262D', edgecolor='#30363D', linewidth=1)
    ax.add_patch(header_bg)
    
    # Terminal title with modern font
    ax.text(8, 8.6, 'BudgetBuddy Terminal', ha='center', va='center', 
            fontsize=18, fontweight='bold', color='#58A6FF')
    
    # Welcome banner with gradient text
    ax.text(2, 7.5, '🎯 Welcome to BudgetBuddy - Your Smart Financial Companion!', 
            fontsize=14, color='#7EE787', fontweight='bold')
    ax.text(2, 7.2, '=' * 80, fontsize=10, color='#7EE787')
    
    # Main menu with modern styling
    ax.text(2, 6.7, '📋 Main Menu:', fontsize=13, color='#FFFFFF', fontweight='bold')
    
    menu_items = [
        '1. 💰 Set up budget',
        '2. 💸 Add expense', 
        '3. 📊 View monthly summary',
        '4. 🧠 Check overspending & get suggestions',
        '5. 📈 Create spending chart',
        '6. 📤 Export data',
        '7. 🚪 Exit'
    ]
    
    y_start = 6.3
    for i, option in enumerate(menu_items):
        ax.text(2, y_start - i*0.25, option, fontsize=11, color='#C9D1D9')
    
    # User interaction with modern styling
    ax.text(2, 4.5, 'Enter your choice (1-7): 2', fontsize=11, color='#FFD700', fontweight='bold')
    
    # Expense input form with modern design
    expense_bg = FancyBboxPatch((1.5, 3.5), 13, 1.2, boxstyle="round,pad=0.1", 
                               facecolor='#1F6FEB', alpha=0.1, edgecolor='#1F6FEB', linewidth=1)
    ax.add_patch(expense_bg)
    
    ax.text(2, 4.0, '💸 Add Expense', fontsize=12, color='#7EE787', fontweight='bold')
    ax.text(2, 3.7, 'Category: groceries', fontsize=11, color='#C9D1D9')
    ax.text(2, 3.4, 'Amount: $45.50', fontsize=11, color='#C9D1D9')
    ax.text(2, 3.1, 'Description: Weekly grocery shopping', fontsize=11, color='#C9D1D9')
    ax.text(2, 2.8, '✅ Expense added successfully!', fontsize=11, color='#7EE787', fontweight='bold')
    
    # Smart suggestions with modern styling
    suggestions_bg = FancyBboxPatch((1.5, 1.8), 13, 1.0, boxstyle="round,pad=0.1", 
                                   facecolor='#FFA500', alpha=0.1, edgecolor='#FFA500', linewidth=1)
    ax.add_patch(suggestions_bg)
    
    ax.text(2, 2.3, '🧠 Smart Suggestions:', fontsize=12, color='#FFA500', fontweight='bold')
    ax.text(2, 2.0, '• You are within budget for groceries this month', fontsize=10, color='#7EE787')
    ax.text(2, 1.7, '• Consider meal planning to reduce food waste', fontsize=10, color='#FFA500')
    ax.text(2, 1.4, '• Track your spending patterns for better insights', fontsize=10, color='#FFA500')
    
    # Status bar with modern design
    status_bg = FancyBboxPatch((1, 0.5), 14, 0.6, boxstyle="round,pad=0.1", 
                              facecolor='#21262D', edgecolor='#30363D', linewidth=1)
    ax.add_patch(status_bg)
    
    # Status indicators with modern styling
    ax.text(2, 0.8, '🟢 Status: Ready', fontsize=10, color='#7EE787', fontweight='bold')
    ax.text(5, 0.8, '🔒 Data: Local Storage', fontsize=10, color='#58A6FF')
    ax.text(9, 0.8, '🛡️ Privacy: Secure', fontsize=10, color='#7EE787')
    ax.text(13, 0.8, '⚡ Version: 1.0', fontsize=10, color='#C9D1D9')
    
    # Add some modern decorative elements
    # Floating icons
    icons = ['💰', '📊', '🎯', '💡', '📈', '🔒']
    positions = [(0.5, 8.5), (15.5, 8.5), (0.5, 5), (15.5, 5), (0.5, 2), (15.5, 2)]
    
    for icon, (x, y) in zip(icons, positions):
        ax.text(x, y, icon, fontsize=20, ha='center', va='center', alpha=0.7)
    
    # Add some subtle glow effects
    glow_circles = [(2, 4), (8, 6), (14, 3)]
    for x, y in glow_circles:
        circle = Circle((x, y), 0.3, facecolor='#58A6FF', alpha=0.1)
        ax.add_patch(circle)
    
    # Add modern border
    border = FancyBboxPatch((0.2, 0.2), 15.6, 9.6, boxstyle="round,pad=0.1", 
                           facecolor='none', edgecolor='#30363D', linewidth=2, alpha=0.5)
    ax.add_patch(border)
    
    plt.tight_layout()
    plt.savefig('budgetbuddy_cool_screenshot.png', dpi=300, bbox_inches='tight', 
                facecolor='#0D1117', edgecolor='none')
    plt.show()
    
    print("✅ Cool screenshot saved as 'budgetbuddy_cool_screenshot.png'")

if __name__ == "__main__":
    create_cool_screenshot()
