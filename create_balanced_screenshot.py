#!/usr/bin/env python3
"""
Create a balanced ASCII screenshot with content on both sides
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
import numpy as np

def create_balanced_screenshot():
    """Create a balanced screenshot with content on both sides"""
    
    fig, ax = plt.subplots(1, 1, figsize=(22, 14))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Dark terminal background
    terminal_bg = Rectangle((0, 0), 22, 14, facecolor='#0A0A0A', edgecolor='none')
    ax.add_patch(terminal_bg)
    
    # Terminal window
    window_bg = FancyBboxPatch((0.5, 0.5), 21, 13, boxstyle="round,pad=0.3", 
                              facecolor='#1A1A1A', edgecolor='#333333', linewidth=2)
    ax.add_patch(window_bg)
    
    # Terminal header
    header_bg = Rectangle((0.5, 12.2), 21, 1.3, facecolor='#2A2A2A', edgecolor='#333333', linewidth=1)
    ax.add_patch(header_bg)
    
    # ASCII art title
    ascii_title = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║  ██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗████████╗██████╗  ██████╗ ██╗   ██╗██████╗ ██╗   ██╗██╗   ██╗ ║
    ║  ██╔══██╗██║   ██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗╚██╗ ██╔╝╚██╗ ██╔╝ ║
    ║  ██████╔╝██║   ██║██║  ██║██║  ██║█████╗     ██║   ██████╔╝██║  ██║ ╚████╔╝ ██║  ██║ ╚████╔╝  ╚████╔╝  ║
    ║  ██╔══██╗██║   ██║██║  ██║██║  ██║██╔══╝     ██║   ██╔══██╗██║  ██║  ╚██╔╝  ██║  ██║  ╚██╔╝    ╚██╔╝   ║
    ║  ██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗   ██║   ██║  ██║╚██████╔╝   ██║   ██████╔╝   ██║      ██║    ║
    ║  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═════╝    ╚═╝      ╚═╝    ║
    ║                                                                                                        ║
    ║                          Smart Student Budgeting Tool v1.0                                            ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    
    # Main terminal content (left side)
    terminal_content = """
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │  🎯 Welcome to BudgetBuddy - Your Smart Financial Companion!                │
    │  ======================================================================== │
    │                                                                             │
    │  📋 Main Menu:                                                             │
    │     1. 💰 Set up budget (50/30/20 rule or custom)                        │
    │     2. 💸 Add expense                                                      │
    │     3. 📊 View monthly summary                                             │
    │     4. 🧠 Check overspending & get suggestions                            │
    │     5. 📈 Create spending chart                                           │
    │     6. 📤 Export data                                                      │
    │     7. 🚪 Exit                                                             │
    │                                                                             │
    │  Enter your choice (1-7): 1                                                │
    │                                                                             │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │ 💰 Budget Setup                                                     │   │
    │  │ Choose allocation method:                                           │   │
    │  │ 1. 50/30/20 rule (50% needs, 30% wants, 20% savings)               │   │
    │  │ 2. Custom percentages                                               │   │
    │  │ Enter choice (1-2): 1                                               │   │
    │  │ Enter your monthly income: $2000                                   │   │
    │  │ ✅ Budget set with 50/30/20 rule:                                   │   │
    │  │    💰 Total Income: $2000.00                                        │   │
    │  │    🏠 Needs (50%): $1000.00                                          │   │
    │  │    🎯 Wants (30%): $600.00                                           │   │
    │  │    💎 Savings (20%): $400.00                                        │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                                                             │
    │  Enter your choice (1-7): 2                                                │
    │                                                                             │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │ 💸 Add Expense                                                      │   │
    │  │ Category: groceries                                                 │   │
    │  │ Amount: $45.50                                                      │   │
    │  │ Description: Weekly grocery shopping                                │   │
    │  │ ✅ Expense added: $45.50 for groceries                              │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                                                             │
    │  Enter your choice (1-7): 3                                                │
    │                                                                             │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │ 📊 Monthly Summary                                                 │   │
    │  │ 💰 Total Spent: $1510.00                                           │   │
    │  │ 📝 Number of Expenses: 7                                           │   │
    │  │ 📊 By Category:                                                     │   │
    │  │    groceries: $200.00                                               │   │
    │  │    rent: $800.00                                                    │   │
    │  │    entertainment: $100.00                                          │   │
    │  │    utilities: $150.00                                               │   │
    │  │    dining: $80.00                                                   │   │
    │  │    transport: $60.00                                                │   │
    │  │    shopping: $120.00                                                │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                                                             │
    │  Enter your choice (1-7): 4                                                │
    │                                                                             │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │ 🧠 Smart Suggestions:                                              │   │
    │  │ ⚠️  You've overspent by $110.00 this month!                         │   │
    │  │ 💡 Needs spending exceeded by $210.00. Consider:                     │   │
    │  │    cheaper groceries, energy-saving tips, or public transport.      │   │
    │  │ 🎯 Wants spending exceeded by $50.00. Try:                          │   │
    │  │    cooking at home, free entertainment, or delayed gratification.  │   │
    │  │ 📊 High spending in rent: $800.00 average. Consider:                │   │
    │  │    reducing frequency or finding alternatives.                      │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                                                             │
    │  🟢 Status: Ready  🔒 Data: Local Storage  🛡️ Privacy: Secure  ⚡ v1.0    │
    └─────────────────────────────────────────────────────────────────────────────┘
    """
    
    # Right side content - Features and Stats
    right_content = """
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │  🚀 BudgetBuddy Features                                                   │
    │  ======================================================================== │
    │                                                                             │
    │  💰 Smart Budget Allocation:                                               │
    │     • 50/30/20 Rule Support                                               │
    │     • Custom Percentage Allocation                                         │
    │     • Automatic Category Calculation                                       │
    │                                                                             │
    │  📊 Advanced Analytics:                                                     │
    │     • Real-time Spending Tracking                                          │
    │     • Category-wise Analysis                                               │
    │     • Monthly/Weekly Reports                                               │
    │     • Visual Chart Generation                                              │
    │                                                                             │
    │  🧠 AI-Powered Insights:                                                   │
    │     • Overspending Detection                                               │
    │     • Personalized Suggestions                                             │
    │     • Spending Pattern Analysis                                            │
    │     • Smart Recommendations                                                │
    │                                                                             │
    │  🔒 Privacy & Security:                                                    │
    │     • Local Data Storage Only                                               │
    │     • No Cloud Dependencies                                                │
    │     • CSV/JSON Export Options                                              │
    │     • Complete Data Control                                                │
    │                                                                             │
    │  📈 Current Session Stats:                                                 │
    │     • Total Expenses: 7                                                    │
    │     • Amount Spent: $1,510.00                                             │
    │     • Budget Remaining: $490.00                                           │
    │     • Categories Used: 7                                                   │
    │                                                                             │
    │  🎯 Student Benefits:                                                      │
    │     • Simple CLI Interface                                                 │
    │     • Educational Financial Learning                                       │
    │     • No Subscription Required                                             │
    │     • Offline Functionality                                                │
    │                                                                             │
    │  📱 Quick Actions:                                                         │
    │     • Press 'h' for help                                                   │
    │     • Press 'q' to quit                                                    │
    │     • Press 's' for stats                                                  │
    │     • Press 'c' for chart                                                  │
    │                                                                             │
    │  🔧 Technical Info:                                                        │
    │     • Python 3.7+ Required                                                │
    │     • Dependencies: pandas, matplotlib, numpy                               │
    │     • Storage: Local CSV/JSON files                                        │
    │     • License: Open Source                                                 │
    │                                                                             │
    │  📞 Support:                                                               │
    │     • GitHub: github.com/JimboL1/BudgetBuddy                              │
    │     • Documentation: README.md                                             │
    │     • Issues: GitHub Issues                                                 │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
    """
    
    # Add the ASCII art
    ax.text(11, 12.8, ascii_title, ha='center', va='center', 
            fontsize=6, color='#00FF00', fontfamily='monospace')
    
    # Add main terminal content (left side)
    ax.text(1, 10.5, terminal_content, ha='left', va='top', 
            fontsize=7, color='#00FF00', fontfamily='monospace')
    
    # Add right side content
    ax.text(11, 10.5, right_content, ha='left', va='top', 
            fontsize=6, color='#00FF00', fontfamily='monospace')
    
    # Add some cool effects
    # Glowing dots
    for i in range(40):
        x = np.random.uniform(1, 21)
        y = np.random.uniform(1, 13)
        circle = plt.Circle((x, y), 0.03, facecolor='#00FF00', alpha=0.2)
        ax.add_patch(circle)
    
    # Matrix-style rain effect
    for i in range(30):
        x = np.random.uniform(1, 21)
        y = np.random.uniform(1, 13)
        ax.text(x, y, '01', fontsize=4, color='#00FF00', alpha=0.1, 
                fontfamily='monospace')
    
    # Add some floating symbols
    symbols = ['💰', '📊', '🎯', '💡', '📈', '🔒', '💸', '🧠', '🚀', '⚡']
    for i, symbol in enumerate(symbols):
        x = 0.3 + i * 2.0
        y = 0.3
        ax.text(x, y, symbol, fontsize=8, color='#00FF00', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('budgetbuddy_balanced_screenshot.png', dpi=300, bbox_inches='tight', 
                facecolor='#0A0A0A', edgecolor='none')
    plt.show()
    
    print("✅ Balanced screenshot saved as 'budgetbuddy_balanced_screenshot.png'")

if __name__ == "__main__":
    create_balanced_screenshot()
