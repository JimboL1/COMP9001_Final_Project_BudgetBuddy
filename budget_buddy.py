#!/usr/bin/env python3
"""
BudgetBuddy - A lightweight monthly budgeting tool for students
Supports 50/30/20 or custom allocation rules, expense tracking, and smart suggestions
Extended version with income tracking, goal management, and advanced analytics

================================================================================
IMPORTANT: DEPENDENCIES AND RUNNING INSTRUCTIONS
================================================================================

EXTERNAL LIBRARIES REQUIRED (outside Python's standard library):
- pandas >= 1.5.0 (data manipulation)
- matplotlib >= 3.6.0 (chart generation - GRAPHICS RENDERING LIBRARY)
- numpy >= 1.24.0 (statistical calculations)

Note: Installing these will automatically install dependencies like:
  python-dateutil, pytz, pillow, kiwisolver, pyparsing

INSTALLATION:
  pip install -r requirements.txt

HOW TO RUN:
  python3 budget_buddy.py

IMPORTANT NOTE FOR TUTOR:
This program uses matplotlib for chart generation (menu option 10).
Matplotlib is a GRAPHICS RENDERING library and will NOT work in Ed's
environment. Please run this program OUTSIDE of Ed to test chart features.

QUICK START (RECOMMENDED FOR TESTING):
  1. python3 quick_demo_setup.py  (generates demo data automatically)
  2. python3 budget_buddy.py      (run the main program)

The quick_demo_setup.py script creates sample budget, expenses, incomes,
goals, and categories for immediate testing of all features.

See README.txt for complete documentation.
================================================================================
"""

import json
import csv
import os
import shutil
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass, asdict
from collections import defaultdict


# ==================== UI ENHANCEMENT FUNCTIONS ====================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'


def print_header(text: str, width: int = 70):
    """Print a beautiful header"""
    print("\n" + Colors.CYAN + "═" * width + Colors.END)
    print(Colors.BOLD + Colors.CYAN + f"  {text}".center(width) + Colors.END)
    print(Colors.CYAN + "═" * width + Colors.END)


def print_section(text: str):
    """Print a section title"""
    print("\n" + Colors.BOLD + Colors.YELLOW + f"▶ {text}" + Colors.END)


def print_success(text: str):
    """Print success message"""
    print(Colors.GREEN + f"✓ {text}" + Colors.END)


def print_error(text: str):
    """Print error message"""
    print(Colors.RED + f"✗ {text}" + Colors.END)


def print_info(text: str):
    """Print info message"""
    print(Colors.BLUE + f"ℹ {text}" + Colors.END)


def print_warning(text: str):
    """Print warning message"""
    print(Colors.YELLOW + f"⚠ {text}" + Colors.END)


def print_table(headers: List[str], rows: List[List[str]], width: int = 70):
    """Print a formatted table"""
    if not rows:
        return
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print header
    header_line = "│ " + " │ ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " │"
    separator = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    top_border = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    bottom_border = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
    
    print(Colors.CYAN + top_border + Colors.END)
    print(Colors.BOLD + Colors.CYAN + header_line + Colors.END)
    print(Colors.CYAN + separator + Colors.END)
    
    # Print rows
    for row in rows:
        row_line = "│ " + " │ ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + " │"
        print(row_line)
    
    print(Colors.CYAN + bottom_border + Colors.END)


def print_progress_bar(current: float, total: float, length: int = 30, label: str = ""):
    """Print a progress bar"""
    if total == 0:
        percent = 0
        filled = 0
    else:
        percent = min(100, (current / total) * 100)
        filled = int(length * current / total)
    
    bar = "█" * filled + "░" * (length - filled)
    color = Colors.GREEN if percent <= 75 else Colors.YELLOW if percent <= 90 else Colors.RED
    
    if label:
        print(f"\n{label}")
    print(f"{color}[{bar}]{Colors.END} {percent:.1f}% ({Colors.BOLD}${current:.2f}${Colors.END} / ${total:.2f})")


def print_card(title: str, content: Dict[str, str], width: int = 50):
    """Print information in a card format"""
    print("\n" + Colors.CYAN + "┌" + "─" * (width - 2) + "┐" + Colors.END)
    print(Colors.BOLD + Colors.CYAN + "│ " + title.ljust(width - 4) + " │" + Colors.END)
    print(Colors.CYAN + "├" + "─" * (width - 2) + "┤" + Colors.END)
    for key, value in content.items():
        line = f"│ {key}: {Colors.BOLD}{value}{Colors.CYAN}"
        print(Colors.CYAN + line.ljust(width - len(value) - len(key) - 6) + " │" + Colors.END)
    print(Colors.CYAN + "└" + "─" * (width - 2) + "┘" + Colors.END)


def print_menu_box(items: List[Tuple[str, str]], title: str = ""):
    """Print menu items in a box"""
    if title:
        print_header(title, 60)
    else:
        print()
    
    for num, desc in items:
        icon = " " if not desc[0].isalpha() else "•"
        print(f"  {Colors.BOLD}{Colors.CYAN}{num:>3}.{Colors.END} {desc}")


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"


def format_percent(value: float) -> str:
    """Format value as percentage"""
    return f"{value:.1f}%"


@dataclass
class Expense:
    """Represents a single expense entry"""
    date: str
    category: str
    amount: float
    description: str


@dataclass
class Income:
    """Represents an income entry"""
    date: str
    source: str
    amount: float
    category: str = "salary"  # salary, part_time, bonus, other
    description: str = ""


@dataclass
class Budget:
    """Represents budget allocation for a month"""
    month: str
    total_income: float
    needs_percentage: float = 50.0
    wants_percentage: float = 30.0
    savings_percentage: float = 20.0
    needs_amount: float = 0.0
    wants_amount: float = 0.0
    savings_amount: float = 0.0


@dataclass
class Category:
    """Represents a spending category with metadata"""
    name: str
    color: str = "#3498db"  # Default blue
    icon: str = "📁"  # Default icon
    budget_type: str = "needs"  # needs, wants, savings


@dataclass
class Goal:
    """Represents a financial goal"""
    name: str
    target_amount: float
    current_amount: float = 0.0
    deadline: str = ""  # YYYY-MM-DD format
    description: str = ""
    is_completed: bool = False


class BudgetBuddy:
    """Main BudgetBuddy application class"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.expenses_file = os.path.join(data_dir, "expenses.csv")
        self.budget_file = os.path.join(data_dir, "budget.json")
        self.incomes_file = os.path.join(data_dir, "incomes.csv")
        self.categories_file = os.path.join(data_dir, "categories.json")
        self.goals_file = os.path.join(data_dir, "goals.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.expenses = self._load_expenses()
        self.budget = self._load_budget()
        self.incomes = self._load_incomes()
        self.categories = self._load_categories()
        self.goals = self._load_goals()
        
        # Initialize default categories if none exist
        if not self.categories:
            self._initialize_default_categories()
    
    def _load_expenses(self) -> List[Expense]:
        """Load expenses from CSV file"""
        expenses = []
        if os.path.exists(self.expenses_file):
            try:
                df = pd.read_csv(self.expenses_file)
                for _, row in df.iterrows():
                    expenses.append(Expense(
                        date=row['date'],
                        category=row['category'],
                        amount=float(row['amount']),
                        description=row['description']
                    ))
            except Exception as e:
                print(f"Error loading expenses: {e}")
        return expenses
    
    def _save_expenses(self):
        """Save expenses to CSV file"""
        if self.expenses:
            df = pd.DataFrame([asdict(expense) for expense in self.expenses])
            df.to_csv(self.expenses_file, index=False)
    
    def _load_budget(self) -> Optional[Budget]:
        """Load budget from JSON file"""
        if os.path.exists(self.budget_file):
            try:
                with open(self.budget_file, 'r') as f:
                    data = json.load(f)
                    return Budget(**data)
            except Exception as e:
                print(f"Error loading budget: {e}")
        return None
    
    def _save_budget(self):
        """Save budget to JSON file"""
        if self.budget:
            with open(self.budget_file, 'w') as f:
                json.dump(asdict(self.budget), f, indent=2)
    
    def _load_incomes(self) -> List[Income]:
        """Load incomes from CSV file"""
        incomes = []
        if os.path.exists(self.incomes_file):
            try:
                df = pd.read_csv(self.incomes_file)
                for _, row in df.iterrows():
                    incomes.append(Income(
                        date=row['date'],
                        source=row['source'],
                        amount=float(row['amount']),
                        category=row.get('category', 'salary'),
                        description=row.get('description', '')
                    ))
            except Exception as e:
                print(f"Error loading incomes: {e}")
        return incomes
    
    def _save_incomes(self):
        """Save incomes to CSV file"""
        if self.incomes:
            df = pd.DataFrame([asdict(income) for income in self.incomes])
            df.to_csv(self.incomes_file, index=False)
    
    def _load_categories(self) -> Dict[str, Category]:
        """Load categories from JSON file"""
        categories = {}
        if os.path.exists(self.categories_file):
            try:
                with open(self.categories_file, 'r') as f:
                    data = json.load(f)
                    for name, cat_data in data.items():
                        categories[name] = Category(**cat_data)
            except Exception as e:
                print(f"Error loading categories: {e}")
        return categories
    
    def _save_categories(self):
        """Save categories to JSON file"""
        with open(self.categories_file, 'w') as f:
            data = {name: asdict(cat) for name, cat in self.categories.items()}
            json.dump(data, f, indent=2)
    
    def _initialize_default_categories(self):
        """Initialize default categories"""
        default_categories = {
            'rent': Category('rent', '#e74c3c', '🏠', 'needs'),
            'groceries': Category('groceries', '#27ae60', '🛒', 'needs'),
            'utilities': Category('utilities', '#f39c12', '⚡', 'needs'),
            'transport': Category('transport', '#3498db', '🚌', 'needs'),
            'insurance': Category('insurance', '#9b59b6', '🛡️', 'needs'),
            'entertainment': Category('entertainment', '#e91e63', '🎬', 'wants'),
            'dining': Category('dining', '#ff9800', '🍽️', 'wants'),
            'shopping': Category('shopping', '#00bcd4', '🛍️', 'wants'),
            'hobbies': Category('hobbies', '#4caf50', '🎨', 'wants'),
            'savings': Category('savings', '#2196f3', '💰', 'savings'),
        }
        self.categories = default_categories
        self._save_categories()
    
    def _load_goals(self) -> List[Goal]:
        """Load goals from JSON file"""
        goals = []
        if os.path.exists(self.goals_file):
            try:
                with open(self.goals_file, 'r') as f:
                    data = json.load(f)
                    for goal_data in data:
                        goals.append(Goal(**goal_data))
            except Exception as e:
                print(f"Error loading goals: {e}")
        return goals
    
    def _save_goals(self):
        """Save goals to JSON file"""
        with open(self.goals_file, 'w') as f:
            json.dump([asdict(goal) for goal in self.goals], f, indent=2)
    
    def set_budget(self, total_income: float, needs_pct: float = 50.0, 
                   wants_pct: float = 30.0, savings_pct: float = 20.0) -> Budget:
        """Set up monthly budget with custom or 50/30/20 rule"""
        current_month = datetime.now().strftime("%Y-%m")
        
        budget = Budget(
            month=current_month,
            total_income=total_income,
            needs_percentage=needs_pct,
            wants_percentage=wants_pct,
            savings_percentage=savings_pct,
            needs_amount=total_income * needs_pct / 100,
            wants_amount=total_income * wants_pct / 100,
            savings_amount=total_income * savings_pct / 100
        )
        
        self.budget = budget
        self._save_budget()
        return budget
    
    def add_expense(self, category: str, amount: float, description: str = "") -> Expense:
        """Add a new expense entry"""
        expense = Expense(
            date=date.today().isoformat(),
            category=category,
            amount=amount,
            description=description
        )
        self.expenses.append(expense)
        self._save_expenses()
        return expense
    
    def get_expense_by_index(self, index: int) -> Optional[Expense]:
        """Get expense by index"""
        if 0 <= index < len(self.expenses):
            return self.expenses[index]
        return None
    
    def list_expenses(self, month: str = None, limit: int = 50) -> List[Tuple[int, Expense]]:
        """List expenses with their indices"""
        if month:
            filtered = [(i, exp) for i, exp in enumerate(self.expenses) if exp.date.startswith(month)]
        else:
            filtered = [(i, exp) for i, exp in enumerate(self.expenses)]
        
        # Sort by date descending
        filtered.sort(key=lambda x: x[1].date, reverse=True)
        return filtered[:limit]
    
    def edit_expense(self, index: int, category: str = None, amount: float = None, 
                     description: str = None, expense_date: str = None) -> Optional[Expense]:
        """Edit an existing expense"""
        if not (0 <= index < len(self.expenses)):
            return None
        
        expense = self.expenses[index]
        if category is not None:
            expense.category = category
        if amount is not None:
            expense.amount = amount
        if description is not None:
            expense.description = description
        if expense_date is not None:
            expense.date = expense_date
        
        self._save_expenses()
        return expense
    
    def delete_expense(self, index: int) -> bool:
        """Delete an expense by index"""
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self._save_expenses()
            return True
        return False
    
    def get_monthly_summary(self, month: str = None) -> Dict:
        """Get spending summary for a specific month"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        # Filter expenses for the month
        month_expenses = [exp for exp in self.expenses if exp.date.startswith(month)]
        
        # Calculate totals by category
        category_totals = {}
        total_spent = 0
        
        for expense in month_expenses:
            category = expense.category
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += expense.amount
            total_spent += expense.amount
        
        return {
            'month': month,
            'total_spent': total_spent,
            'category_totals': category_totals,
            'expense_count': len(month_expenses)
        }
    
    def check_overspending(self, month: str = None) -> List[str]:
        """Check for overspending and generate shrink suggestions"""
        if not self.budget:
            return ["No budget set. Please set up your budget first."]
        
        summary = self.get_monthly_summary(month)
        suggestions = []
        
        # Check if total spending exceeds income
        if summary['total_spent'] > self.budget.total_income:
            overspend = summary['total_spent'] - self.budget.total_income
            suggestions.append(f"⚠️  You've overspent by ${overspend:.2f} this month!")
        
        # Check category-specific overspending
        needs_categories = ['rent', 'groceries', 'utilities', 'transport', 'insurance']
        wants_categories = ['entertainment', 'dining', 'shopping', 'hobbies']
        
        needs_spent = sum(summary['category_totals'].get(cat, 0) for cat in needs_categories)
        wants_spent = sum(summary['category_totals'].get(cat, 0) for cat in wants_categories)
        
        if needs_spent > self.budget.needs_amount:
            excess = needs_spent - self.budget.needs_amount
            suggestions.append(f"💡 Needs spending exceeded by ${excess:.2f}. Consider: cheaper groceries, energy-saving tips, or public transport.")
        
        if wants_spent > self.budget.wants_amount:
            excess = wants_spent - self.budget.wants_amount
            suggestions.append(f"🎯 Wants spending exceeded by ${excess:.2f}. Try: cooking at home, free entertainment, or delayed gratification.")
        
        # Generate smart suggestions based on recent spending patterns
        if len(self.expenses) >= 5:  # Need some history for suggestions
            recent_expenses = sorted(self.expenses, key=lambda x: x.date, reverse=True)[:10]
            high_spending_categories = {}
            
            for exp in recent_expenses:
                if exp.category not in high_spending_categories:
                    high_spending_categories[exp.category] = []
                high_spending_categories[exp.category].append(exp.amount)
            
            # Find categories with high average spending
            for category, amounts in high_spending_categories.items():
                avg_amount = sum(amounts) / len(amounts)
                if avg_amount > 50:  # Threshold for "high" spending
                    suggestions.append(f"📊 High spending in {category}: ${avg_amount:.2f} average. Consider reducing frequency or finding alternatives.")
        
        return suggestions if suggestions else ["✅ Great job! You're staying within your budget."]
    
    def create_chart(self, month: str = None, save_path: str = None):
        """Create a pie chart of spending by category"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        summary = self.get_monthly_summary(month)
        
        if not summary['category_totals']:
            print("No expenses found for this month.")
            return
        
        # Prepare data for pie chart
        categories = list(summary['category_totals'].keys())
        amounts = list(summary['category_totals'].values())
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title(f'Spending by Category - {month}')
        plt.axis('equal')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
    
    # ==================== FEATURE 2: INCOME TRACKING ====================
    
    def add_income(self, source: str, amount: float, category: str = "salary", description: str = "") -> Income:
        """Add a new income entry"""
        income = Income(
            date=date.today().isoformat(),
            source=source,
            amount=amount,
            category=category,
            description=description
        )
        self.incomes.append(income)
        self._save_incomes()
        return income
    
    def get_income_summary(self, month: str = None) -> Dict:
        """Get income summary for a specific month"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        month_incomes = [inc for inc in self.incomes if inc.date.startswith(month)]
        total_income = sum(inc.amount for inc in month_incomes)
        source_totals = defaultdict(float)
        
        for income in month_incomes:
            source_totals[income.source] += income.amount
        
        return {
            'month': month,
            'total_income': total_income,
            'source_totals': dict(source_totals),
            'income_count': len(month_incomes)
        }
    
    # ==================== FEATURE 3: MORE CHART TYPES ====================
    
    def create_bar_chart(self, month: str = None, save_path: str = None):
        """Create a bar chart of spending by category"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        summary = self.get_monthly_summary(month)
        if not summary['category_totals']:
            print("No expenses found for this month.")
            return
        
        categories = list(summary['category_totals'].keys())
        amounts = list(summary['category_totals'].values())
        colors = [self.categories.get(cat, Category(cat)).color for cat in categories]
        
        plt.figure(figsize=(12, 6))
        plt.bar(categories, amounts, color=colors)
        plt.title(f'Spending by Category - {month}')
        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        plt.close()
    
    def create_trend_chart(self, months: int = 6, save_path: str = None):
        """Create a line chart showing spending trends over months"""
        end_date = datetime.now()
        monthly_totals = []
        month_labels = []
        
        for i in range(months):
            month_date = (end_date - timedelta(days=30*i)).strftime("%Y-%m")
            summary = self.get_monthly_summary(month_date)
            monthly_totals.insert(0, summary['total_spent'])
            month_labels.insert(0, month_date)
        
        plt.figure(figsize=(12, 6))
        plt.plot(month_labels, monthly_totals, marker='o', linewidth=2, markersize=8)
        plt.title(f'Spending Trends - Last {months} Months')
        plt.xlabel('Month')
        plt.ylabel('Total Spending ($)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        plt.close()
    
    def create_budget_vs_actual_chart(self, month: str = None, save_path: str = None):
        """Create a comparison chart of budget vs actual spending"""
        if not self.budget:
            print("No budget set. Please set up your budget first.")
            return
        
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        summary = self.get_monthly_summary(month)
        budget_needs = self.budget.needs_amount
        budget_wants = self.budget.wants_amount
        budget_savings = self.budget.savings_amount
        
        # Calculate actual spending
        needs_categories = ['rent', 'groceries', 'utilities', 'transport', 'insurance']
        wants_categories = ['entertainment', 'dining', 'shopping', 'hobbies']
        
        actual_needs = sum(summary['category_totals'].get(cat, 0) for cat in needs_categories)
        actual_wants = sum(summary['category_totals'].get(cat, 0) for cat in wants_categories)
        actual_savings = self.budget.total_income - summary['total_spent']
        
        categories = ['Needs', 'Wants', 'Savings']
        budget_amounts = [budget_needs, budget_wants, budget_savings]
        actual_amounts = [actual_needs, actual_wants, max(0, actual_savings)]
        
        x = np.arange(len(categories))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x - width/2, budget_amounts, width, label='Budget', color='#3498db')
        bars2 = ax.bar(x + width/2, actual_amounts, width, label='Actual', color='#e74c3c')
        
        ax.set_xlabel('Category')
        ax.set_ylabel('Amount ($)')
        ax.set_title(f'Budget vs Actual Spending - {month}')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.show()
        plt.close()
    
    # ==================== FEATURE 4: CATEGORY MANAGEMENT ====================
    
    def add_category(self, name: str, color: str = "#3498db", icon: str = "📁", budget_type: str = "needs") -> Category:
        """Add a new category"""
        category = Category(name, color, icon, budget_type)
        self.categories[name] = category
        self._save_categories()
        return category
    
    def update_category(self, name: str, color: str = None, icon: str = None, budget_type: str = None) -> Optional[Category]:
        """Update an existing category"""
        if name not in self.categories:
            return None
        
        category = self.categories[name]
        if color is not None:
            category.color = color
        if icon is not None:
            category.icon = icon
        if budget_type is not None:
            category.budget_type = budget_type
        
        self._save_categories()
        return category
    
    def get_category_info(self, name: str) -> Optional[Category]:
        """Get category information"""
        return self.categories.get(name)
    
    def list_categories(self) -> Dict[str, Category]:
        """List all categories"""
        return self.categories.copy()
    
    # ==================== FEATURE 5: BUDGET PROGRESS ====================
    
    def get_budget_progress(self, month: str = None) -> Dict:
        """Get budget progress information"""
        if not self.budget:
            return {"error": "No budget set"}
        
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        summary = self.get_monthly_summary(month)
        needs_categories = ['rent', 'groceries', 'utilities', 'transport', 'insurance']
        wants_categories = ['entertainment', 'dining', 'shopping', 'hobbies']
        
        needs_spent = sum(summary['category_totals'].get(cat, 0) for cat in needs_categories)
        wants_spent = sum(summary['category_totals'].get(cat, 0) for cat in wants_categories)
        total_spent = summary['total_spent']
        
        needs_percent = (needs_spent / self.budget.needs_amount * 100) if self.budget.needs_amount > 0 else 0
        wants_percent = (wants_spent / self.budget.wants_amount * 100) if self.budget.wants_amount > 0 else 0
        total_percent = (total_spent / self.budget.total_income * 100) if self.budget.total_income > 0 else 0
        
        return {
            'month': month,
            'needs': {
                'budget': self.budget.needs_amount,
                'spent': needs_spent,
                'remaining': max(0, self.budget.needs_amount - needs_spent),
                'percent': min(100, needs_percent)
            },
            'wants': {
                'budget': self.budget.wants_amount,
                'spent': wants_spent,
                'remaining': max(0, self.budget.wants_amount - wants_spent),
                'percent': min(100, wants_percent)
            },
            'total': {
                'budget': self.budget.total_income,
                'spent': total_spent,
                'remaining': max(0, self.budget.total_income - total_spent),
                'percent': min(100, total_percent)
            }
        }
    
    # ==================== FEATURE 6: MULTI-TIMEFRAME ANALYSIS ====================
    
    def get_weekly_summary(self, week_start: str = None) -> Dict:
        """Get spending summary for a specific week"""
        if week_start is None:
            today = date.today()
            week_start = (today - timedelta(days=today.weekday())).isoformat()
        
        week_end = (datetime.fromisoformat(week_start) + timedelta(days=6)).isoformat()[:10]
        
        week_expenses = [exp for exp in self.expenses if week_start <= exp.date <= week_end]
        category_totals = defaultdict(float)
        total_spent = 0
        
        for expense in week_expenses:
            category_totals[expense.category] += expense.amount
            total_spent += expense.amount
        
        return {
            'week_start': week_start,
            'week_end': week_end,
            'total_spent': total_spent,
            'category_totals': dict(category_totals),
            'expense_count': len(week_expenses)
        }
    
    def get_yearly_summary(self, year: str = None) -> Dict:
        """Get spending summary for a specific year"""
        if year is None:
            year = datetime.now().strftime("%Y")
        
        year_expenses = [exp for exp in self.expenses if exp.date.startswith(year)]
        category_totals = defaultdict(float)
        monthly_totals = defaultdict(float)
        total_spent = 0
        
        for expense in year_expenses:
            category_totals[expense.category] += expense.amount
            month = expense.date[:7]
            monthly_totals[month] += expense.amount
            total_spent += expense.amount
        
        return {
            'year': year,
            'total_spent': total_spent,
            'category_totals': dict(category_totals),
            'monthly_totals': dict(monthly_totals),
            'expense_count': len(year_expenses),
            'average_monthly': total_spent / 12 if total_spent > 0 else 0
        }
    
    # ==================== FEATURE 7: GOAL SETTING ====================
    
    def add_goal(self, name: str, target_amount: float, deadline: str = "", description: str = "") -> Goal:
        """Add a new financial goal"""
        goal = Goal(
            name=name,
            target_amount=target_amount,
            current_amount=0.0,
            deadline=deadline,
            description=description,
            is_completed=False
        )
        self.goals.append(goal)
        self._save_goals()
        return goal
    
    def update_goal_progress(self, goal_name: str, amount: float) -> Optional[Goal]:
        """Update goal progress"""
        for goal in self.goals:
            if goal.name == goal_name and not goal.is_completed:
                goal.current_amount += amount
                if goal.current_amount >= goal.target_amount:
                    goal.is_completed = True
                self._save_goals()
                return goal
        return None
    
    def get_goals_status(self) -> List[Dict]:
        """Get status of all goals"""
        status = []
        for goal in self.goals:
            progress = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
            status.append({
                'name': goal.name,
                'current': goal.current_amount,
                'target': goal.target_amount,
                'remaining': max(0, goal.target_amount - goal.current_amount),
                'progress': min(100, progress),
                'is_completed': goal.is_completed,
                'deadline': goal.deadline
            })
        return status
    
    # ==================== FEATURE 8: TREND PREDICTION ====================
    
    def predict_next_month_spending(self) -> Dict:
        """Predict next month's spending based on historical data"""
        if len(self.expenses) < 3:
            return {"error": "Insufficient data for prediction (need at least 3 months)"}
        
        # Get last 3 months of data
        monthly_spending = []
        for i in range(3):
            month_date = (datetime.now() - timedelta(days=30*i)).strftime("%Y-%m")
            summary = self.get_monthly_summary(month_date)
            monthly_spending.insert(0, summary['total_spent'])
        
        # Simple linear regression prediction
        if len(monthly_spending) >= 2:
            trend = monthly_spending[-1] - monthly_spending[0]
            predicted = monthly_spending[-1] + (trend / len(monthly_spending))
        else:
            predicted = monthly_spending[-1] if monthly_spending else 0
        
        # Category-wise prediction
        category_predictions = {}
        last_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")
        last_summary = self.get_monthly_summary(last_month)
        
        for category, amount in last_summary['category_totals'].items():
            category_predictions[category] = amount * (predicted / last_summary['total_spent']) if last_summary['total_spent'] > 0 else 0
        
        return {
            'predicted_total': max(0, predicted),
            'predicted_by_category': category_predictions,
            'based_on_months': len(monthly_spending),
            'trend': 'increasing' if trend > 0 else 'decreasing' if trend < 0 else 'stable'
        }
    
    # ==================== FEATURE 9: DATA STATISTICS ====================
    
    def get_statistics(self, month: str = None) -> Dict:
        """Get comprehensive spending statistics"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        summary = self.get_monthly_summary(month)
        month_expenses = [exp for exp in self.expenses if exp.date.startswith(month)]
        
        if not month_expenses:
            return {"error": "No expenses found for this month"}
        
        amounts = [exp.amount for exp in month_expenses]
        
        # Find most frequent category
        category_counts = defaultdict(int)
        for exp in month_expenses:
            category_counts[exp.category] += 1
        most_frequent = max(category_counts.items(), key=lambda x: x[1]) if category_counts else ("", 0)
        
        # Find largest expense
        largest_expense = max(month_expenses, key=lambda x: x.amount) if month_expenses else None
        
        return {
            'month': month,
            'total_expenses': len(month_expenses),
            'total_spent': summary['total_spent'],
            'average_expense': np.mean(amounts),
            'median_expense': np.median(amounts),
            'min_expense': np.min(amounts),
            'max_expense': np.max(amounts),
            'std_deviation': np.std(amounts),
            'most_frequent_category': {
                'name': most_frequent[0],
                'count': most_frequent[1]
            },
            'largest_expense': {
                'category': largest_expense.category,
                'amount': largest_expense.amount,
                'date': largest_expense.date,
                'description': largest_expense.description
            } if largest_expense else None,
            'average_daily_spending': summary['total_spent'] / 30  # Approximate
        }
    
    # ==================== FEATURE 10: BACKUP & RESTORE ====================
    
    def backup_data(self, backup_dir: str = "backups") -> str:
        """Create a backup of all data"""
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"budgetbuddy_backup_{timestamp}")
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy all data files
        files_to_backup = [
            (self.expenses_file, "expenses.csv"),
            (self.budget_file, "budget.json"),
            (self.incomes_file, "incomes.csv"),
            (self.categories_file, "categories.json"),
            (self.goals_file, "goals.json")
        ]
        
        for source, dest_name in files_to_backup:
            if os.path.exists(source):
                dest_path = os.path.join(backup_path, dest_name)
                shutil.copy2(source, dest_path)
        
        print(f"✅ Backup created at: {backup_path}")
        return backup_path
    
    def restore_data(self, backup_path: str) -> bool:
        """Restore data from backup"""
        if not os.path.exists(backup_path):
            print(f"❌ Backup path does not exist: {backup_path}")
            return False
        
        try:
            # Restore files
            restore_files = {
                "expenses.csv": self.expenses_file,
                "budget.json": self.budget_file,
                "incomes.csv": self.incomes_file,
                "categories.json": self.categories_file,
                "goals.json": self.goals_file
            }
            
            for backup_file, dest_file in restore_files.items():
                source = os.path.join(backup_path, backup_file)
                if os.path.exists(source):
                    shutil.copy2(source, dest_file)
            
            # Reload data
            self.expenses = self._load_expenses()
            self.budget = self._load_budget()
            self.incomes = self._load_incomes()
            self.categories = self._load_categories()
            self.goals = self._load_goals()
            
            print(f"✅ Data restored from: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Error restoring data: {e}")
            return False
    
    def export_data(self, format: str = 'csv') -> str:
        """Export all data in specified format"""
        if format.lower() == 'csv':
            # Export expenses and incomes
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_dir = os.path.join(self.data_dir, f"export_{timestamp}")
            os.makedirs(export_dir, exist_ok=True)
            
            if self.expenses:
                df_expenses = pd.DataFrame([asdict(expense) for expense in self.expenses])
                df_expenses.to_csv(os.path.join(export_dir, "expenses.csv"), index=False)
            
            if self.incomes:
                df_incomes = pd.DataFrame([asdict(income) for income in self.incomes])
                df_incomes.to_csv(os.path.join(export_dir, "incomes.csv"), index=False)
            
            return export_dir
        elif format.lower() == 'json':
            # Export all data
            export_data = {
                'budget': asdict(self.budget) if self.budget else None,
                'expenses': [asdict(expense) for expense in self.expenses],
                'incomes': [asdict(income) for income in self.incomes],
                'categories': {name: asdict(cat) for name, cat in self.categories.items()},
                'goals': [asdict(goal) for goal in self.goals]
            }
            export_path = os.path.join(self.data_dir, f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            return export_path
        
        return ""


def main():
    """Main CLI interface for BudgetBuddy"""
    # Welcome screen
    clear_screen()
    print(Colors.BOLD + Colors.CYAN)
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "🎯  Welcome to BudgetBuddy - Your Student Budgeting Companion!".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝" + Colors.END)
    
    # Initialize BudgetBuddy
    bb = BudgetBuddy()
    
    while True:
        print_header("📋 MAIN MENU", 70)
        
        menu_items = [
            ("💰 BUDGET & EXPENSES", []),
            ("1", "💵 Set up budget"),
            ("2", "➕ Add expense"),
            ("3", "✏️  Edit/Delete expense"),
            ("4", "📊 View monthly summary"),
            ("5", "🔍 Check overspending & get suggestions"),
            ("6", "📈 Budget progress tracker"),
            ("", ""),
            ("💵 INCOME & GOALS", []),
            ("7", "💰 Add income"),
            ("8", "📊 View income summary"),
            ("9", "🎯 Manage goals"),
            ("", ""),
            ("📊 ANALYTICS & CHARTS", []),
            ("10", "📈 Create charts (pie/bar/trend/comparison)"),
            ("11", "📊 View statistics"),
            ("12", "📅 Multi-timeframe analysis (week/year)"),
            ("13", "🔮 Predict next month spending"),
            ("", ""),
            ("⚙️  SETTINGS & DATA", []),
            ("14", "🏷️  Manage categories"),
            ("15", "💾 Backup data"),
            ("16", "📂 Restore data"),
            ("17", "📤 Export data"),
            ("", ""),
            ("0", "🚪 Exit")
        ]
        
        current_section = ""
        for item in menu_items:
            if isinstance(item, tuple) and len(item) == 2:
                if item[0] and not item[0][0].isdigit():
                    # Section header
                    if current_section:
                        print()
                    current_section = item[0]
                    print_section(item[0])
                elif item[0] or item[1]:
                    num, desc = item
                    if num:
                        print(f"  {Colors.BOLD}{Colors.CYAN}{num:>3}.{Colors.END} {desc}")
                    elif desc:
                        print()
        
        print()
        choice = input(f"{Colors.BOLD}Enter your choice {Colors.CYAN}(0-17){Colors.END}: ").strip()
        
        if choice == '1':
            print_header("💰 BUDGET SETUP")
            print_info("Choose your budget allocation method:")
            print(f"  {Colors.BOLD}1.{Colors.END} 50/30/20 rule (50% needs, 30% wants, 20% savings)")
            print(f"  {Colors.BOLD}2.{Colors.END} Custom percentages")
            
            method = input(f"\n{Colors.BOLD}Enter choice (1-2):{Colors.END} ").strip()
            
            try:
                income = float(input(f"{Colors.BOLD}Enter your monthly income:${Colors.END} "))
                
                if method == '1':
                    budget = bb.set_budget(income)
                    print_success("Budget set with 50/30/20 rule!")
                else:
                    needs_pct = float(input(f"{Colors.BOLD}Needs percentage (e.g., 50):{Colors.END} "))
                    wants_pct = float(input(f"{Colors.BOLD}Wants percentage (e.g., 30):{Colors.END} "))
                    savings_pct = float(input(f"{Colors.BOLD}Savings percentage (e.g., 20):{Colors.END} "))
                    budget = bb.set_budget(income, needs_pct, wants_pct, savings_pct)
                    print_success("Custom budget set!")
                
                print_card("Budget Overview", {
                    "💰 Total Income": format_currency(budget.total_income),
                    "🏠 Needs": f"{format_percent(budget.needs_percentage)} = {format_currency(budget.needs_amount)}",
                    "🎯 Wants": f"{format_percent(budget.wants_percentage)} = {format_currency(budget.wants_amount)}",
                    "💎 Savings": f"{format_percent(budget.savings_percentage)} = {format_currency(budget.savings_amount)}"
                })
                
            except ValueError:
                print_error("Invalid input. Please enter valid numbers.")
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}")
        
        elif choice == '2':
            print_header("➕ ADD EXPENSE")
            try:
                # Show available categories
                categories = bb.list_categories()
                print_info(f"Available categories: {', '.join(list(categories.keys())[:5])}...")
                
                category = input(f"\n{Colors.BOLD}Category{Colors.END} (e.g., groceries, rent, entertainment): ").strip()
                amount = float(input(f"{Colors.BOLD}Amount:${Colors.END} "))
                description = input(f"{Colors.BOLD}Description{Colors.END} (optional): ").strip()
                
                expense = bb.add_expense(category, amount, description)
                print_success(f"Expense added successfully!")
                print_card("Expense Details", {
                    "Amount": format_currency(expense.amount),
                    "Category": expense.category,
                    "Description": description or "None",
                    "Date": expense.date
                })
                
            except ValueError:
                print_error("Invalid input. Please enter valid numbers.")
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}")
        
        elif choice == '3':
            print_header("✏️  EDIT/DELETE EXPENSE")
            expenses_list = bb.list_expenses(limit=20)
            if not expenses_list:
                print_warning("No expenses found.")
            else:
                print_section("Recent Expenses")
                table_rows = []
                for idx, (orig_idx, expense) in enumerate(expenses_list, 1):
                    table_rows.append([
                        str(idx),
                        expense.date,
                        expense.category.capitalize(),
                        format_currency(expense.amount),
                        expense.description[:30] + "..." if len(expense.description) > 30 else expense.description or "None"
                    ])
                print_table(["#", "Date", "Category", "Amount", "Description"], table_rows)
                
                try:
                    sel = input("\nEnter expense number to edit/delete (or 'c' to cancel): ").strip().lower()
                    if sel == 'c':
                        continue
                    
                    sel_num = int(sel) - 1
                    if 0 <= sel_num < len(expenses_list):
                        orig_idx, expense = expenses_list[sel_num]
                        print(f"\nSelected: {expense.date} - {expense.category}: ${expense.amount:.2f}")
                        action = input("Edit (e) or Delete (d)? ").strip().lower()
                        
                        if action == 'e':
                            print("Leave blank to keep current value")
                            new_category = input(f"Category [{expense.category}]: ").strip() or expense.category
                            new_amount = input(f"Amount [${expense.amount:.2f}]: ").strip()
                            new_amount = float(new_amount) if new_amount else expense.amount
                            new_desc = input(f"Description [{expense.description}]: ").strip() or expense.description
                            
                            bb.edit_expense(orig_idx, new_category, new_amount, new_desc)
                            print("✅ Expense updated!")
                        elif action == 'd':
                            confirm = input("Are you sure? (yes/no): ").strip().lower()
                            if confirm == 'yes':
                                bb.delete_expense(orig_idx)
                                print("✅ Expense deleted!")
                except (ValueError, IndexError):
                    print("❌ Invalid selection.")
        
        elif choice == '4':
            print_header("📊 MONTHLY SUMMARY")
            month = input(f"{Colors.BOLD}Enter month (YYYY-MM) or press Enter for current month:{Colors.END} ").strip()
            if not month:
                month = None
            
            summary = bb.get_monthly_summary(month)
            print_header(f"📅 {summary['month']} Summary", 70)
            
            # Summary card
            print_card("Overview", {
                "💰 Total Spent": format_currency(summary['total_spent']),
                "📝 Number of Expenses": str(summary['expense_count']),
                "📊 Average per Expense": format_currency(summary['total_spent'] / summary['expense_count']) if summary['expense_count'] > 0 else "$0.00"
            })
            
            # Category breakdown table
            if summary['category_totals']:
                print_section("Breakdown by Category")
                table_data = []
                for category, amount in sorted(summary['category_totals'].items(), key=lambda x: x[1], reverse=True):
                    pct = (amount / summary['total_spent'] * 100) if summary['total_spent'] > 0 else 0
                    table_data.append([category.capitalize(), format_currency(amount), f"{pct:.1f}%"])
                
                print_table(["Category", "Amount", "Percentage"], table_data)
            
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}")
        
        elif choice == '5':
            print_header("🔍 OVERSPENDING CHECK & SUGGESTIONS")
            month = input(f"{Colors.BOLD}Enter month (YYYY-MM) or press Enter for current month:{Colors.END} ").strip()
            if not month:
                month = None
            
            suggestions = bb.check_overspending(month)
            print_section("💡 Smart Suggestions")
            for suggestion in suggestions:
                if "⚠️" in suggestion or "overspent" in suggestion.lower():
                    print_warning(suggestion)
                elif "✅" in suggestion:
                    print_success(suggestion)
                else:
                    print_info(suggestion)
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}")
        
        elif choice == '6':
            print_header("📈 BUDGET PROGRESS TRACKER")
            month = input(f"{Colors.BOLD}Enter month (YYYY-MM) or press Enter for current month:{Colors.END} ").strip()
            if not month:
                month = None
            
            progress = bb.get_budget_progress(month)
            if 'error' in progress:
                print_error(progress['error'])
            else:
                print_header(f"📅 Budget Progress - {progress['month']}", 70)
                
                # Needs progress
                print_section("🏠 Needs")
                print_progress_bar(
                    progress['needs']['spent'],
                    progress['needs']['budget'],
                    label=f"Budget: {format_currency(progress['needs']['budget'])} | Remaining: {format_currency(progress['needs']['remaining'])}"
                )
                
                # Wants progress
                print_section("🎯 Wants")
                print_progress_bar(
                    progress['wants']['spent'],
                    progress['wants']['budget'],
                    label=f"Budget: {format_currency(progress['wants']['budget'])} | Remaining: {format_currency(progress['wants']['remaining'])}"
                )
                
                # Total progress
                print_section("💰 Total")
                print_progress_bar(
                    progress['total']['spent'],
                    progress['total']['budget'],
                    label=f"Budget: {format_currency(progress['total']['budget'])} | Remaining: {format_currency(progress['total']['remaining'])}"
                )
                
                # Summary table
                print_section("Summary")
                table_data = [
                    ["Category", "Budget", "Spent", "Remaining", "Progress"],
                    ["🏠 Needs", format_currency(progress['needs']['budget']), 
                     format_currency(progress['needs']['spent']),
                     format_currency(progress['needs']['remaining']),
                     f"{progress['needs']['percent']:.1f}%"],
                    ["🎯 Wants", format_currency(progress['wants']['budget']),
                     format_currency(progress['wants']['spent']),
                     format_currency(progress['wants']['remaining']),
                     f"{progress['wants']['percent']:.1f}%"],
                    ["💰 Total", format_currency(progress['total']['budget']),
                     format_currency(progress['total']['spent']),
                     format_currency(progress['total']['remaining']),
                     f"{progress['total']['percent']:.1f}%"]
                ]
                print_table(table_data[0], table_data[1:])
            
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}")
        
        elif choice == '7':
            print("\n💵 Add Income")
            try:
                source = input("Income source (e.g., Salary, Part-time): ").strip()
                amount = float(input("Amount: $"))
                category = input("Category (salary/part_time/bonus/other) [salary]: ").strip() or "salary"
                description = input("Description (optional): ").strip()
                
                income = bb.add_income(source, amount, category, description)
                print(f"✅ Income added: ${income.amount:.2f} from {income.source}")
            except ValueError:
                print("❌ Invalid input. Please enter valid numbers.")
        
        elif choice == '8':
            print("\n💵 Income Summary")
            month = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
            if not month:
                month = None
            
            summary = bb.get_income_summary(month)
            print(f"\n📅 {summary['month']} Income Summary:")
            print(f"   💰 Total Income: ${summary['total_income']:.2f}")
            print(f"   📝 Number of Income Records: {summary['income_count']}")
            if summary['source_totals']:
                print("\n   📊 By Source:")
                for source, amount in summary['source_totals'].items():
                    print(f"      {source}: ${amount:.2f}")
        
        elif choice == '9':
            print("\n🎯 Manage Goals")
            print("1. View goals")
            print("2. Add goal")
            print("3. Update goal progress")
            sub_choice = input("Enter choice (1-3): ").strip()
            
            if sub_choice == '1':
                goals_status = bb.get_goals_status()
                if not goals_status:
                    print("No goals set yet.")
                else:
                    print("\n📋 Your Goals:")
                    for goal in goals_status:
                        status_icon = "✅" if goal['is_completed'] else "⏳"
                        print(f"\n{status_icon} {goal['name']}")
                        print(f"   Progress: ${goal['current']:.2f} / ${goal['target']:.2f} ({goal['progress']:.1f}%)")
                        print(f"   Remaining: ${goal['remaining']:.2f}")
                        if goal['deadline']:
                            print(f"   Deadline: {goal['deadline']}")
            
            elif sub_choice == '2':
                try:
                    name = input("Goal name: ").strip()
                    target = float(input("Target amount: $"))
                    deadline = input("Deadline (YYYY-MM-DD, optional): ").strip()
                    description = input("Description (optional): ").strip()
                    bb.add_goal(name, target, deadline, description)
                    print("✅ Goal added!")
                except ValueError:
                    print("❌ Invalid input.")
            
            elif sub_choice == '3':
                goals_status = bb.get_goals_status()
                active_goals = [g for g in goals_status if not g['is_completed']]
                if not active_goals:
                    print("No active goals.")
                else:
                    print("\nActive Goals:")
                    for idx, goal in enumerate(active_goals, 1):
                        print(f"{idx}. {goal['name']} - ${goal['current']:.2f} / ${goal['target']:.2f}")
                    try:
                        sel = int(input("Select goal number: ")) - 1
                        if 0 <= sel < len(active_goals):
                            amount = float(input("Amount to add: $"))
                            bb.update_goal_progress(active_goals[sel]['name'], amount)
                            print("✅ Goal progress updated!")
                    except (ValueError, IndexError):
                        print("❌ Invalid selection.")
        
        elif choice == '10':
            print("\n📈 Create Charts")
            print("1. Pie chart")
            print("2. Bar chart")
            print("3. Trend chart")
            print("4. Budget vs Actual")
            chart_choice = input("Select chart type (1-4): ").strip()
            
            month = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
            if not month:
                month = None
            
            save_option = input("Save chart to file? (y/n): ").strip().lower()
            save_path = None
            if save_option == 'y':
                chart_type = ['pie', 'bar', 'trend', 'comparison'][int(chart_choice) - 1] if chart_choice.isdigit() else 'chart'
                save_path = os.path.join(bb.data_dir, f"{chart_type}_chart_{month or datetime.now().strftime('%Y-%m')}.png")
            
            try:
                if chart_choice == '1':
                    bb.create_chart(month, save_path)
                elif chart_choice == '2':
                    bb.create_bar_chart(month, save_path)
                elif chart_choice == '3':
                    months = int(input("Number of months to show (default 6): ").strip() or "6")
                    bb.create_trend_chart(months, save_path)
                elif chart_choice == '4':
                    bb.create_budget_vs_actual_chart(month, save_path)
                if save_path:
                    print(f"✅ Chart saved to {save_path}")
            except Exception as e:
                print(f"❌ Error creating chart: {e}")
        
        elif choice == '11':
            print_header("📊 STATISTICS")
            month = input(f"{Colors.BOLD}Enter month (YYYY-MM) or press Enter for current month:{Colors.END} ").strip()
            if not month:
                month = None
            
            stats = bb.get_statistics(month)
            if 'error' in stats:
                print_error(stats['error'])
            else:
                print_header(f"📅 Statistics for {stats['month']}", 70)
                
                # Basic statistics table
                print_section("Basic Statistics")
                stat_table = [
                    ["Metric", "Value"],
                    ["Total Expenses", str(stats['total_expenses'])],
                    ["Total Spent", format_currency(stats['total_spent'])],
                    ["Average Expense", format_currency(stats['average_expense'])],
                    ["Median Expense", format_currency(stats['median_expense'])],
                    ["Min Expense", format_currency(stats['min_expense'])],
                    ["Max Expense", format_currency(stats['max_expense'])],
                    ["Standard Deviation", format_currency(stats['std_deviation'])],
                    ["Average Daily Spending", format_currency(stats['average_daily_spending'])]
                ]
                print_table(stat_table[0], stat_table[1:])
                
                # Highlights
                print_section("Highlights")
                highlights = {
                    "Most Frequent Category": f"{stats['most_frequent_category']['name'].capitalize()} ({stats['most_frequent_category']['count']} times)",
                    "Average Daily Spending": format_currency(stats['average_daily_spending'])
                }
                if stats['largest_expense']:
                    highlights["Largest Expense"] = f"{stats['largest_expense']['category'].capitalize()}: {format_currency(stats['largest_expense']['amount'])}"
                
                print_card("Key Insights", highlights)
                
                if stats['largest_expense']:
                    print_section("Largest Expense Details")
                    print_card("Expense Details", {
                        "Category": stats['largest_expense']['category'].capitalize(),
                        "Amount": format_currency(stats['largest_expense']['amount']),
                        "Date": stats['largest_expense']['date'],
                        "Description": stats['largest_expense']['description'] or "None"
                    })
            
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}")
        
        elif choice == '12':
            print("\n📊 Multi-Timeframe Analysis")
            print("1. Weekly summary")
            print("2. Yearly summary")
            tf_choice = input("Select timeframe (1-2): ").strip()
            
            if tf_choice == '1':
                week_start = input("Enter week start date (YYYY-MM-DD) or press Enter for current week: ").strip()
                if not week_start:
                    week_start = None
                summary = bb.get_weekly_summary(week_start)
                print(f"\n📅 Week Summary ({summary['week_start']} to {summary['week_end']}):")
                print(f"   💰 Total Spent: ${summary['total_spent']:.2f}")
                print(f"   📝 Number of Expenses: {summary['expense_count']}")
                if summary['category_totals']:
                    print("\n   📊 By Category:")
                    for category, amount in summary['category_totals'].items():
                        print(f"      {category}: ${amount:.2f}")
            
            elif tf_choice == '2':
                year = input("Enter year (YYYY) or press Enter for current year: ").strip()
                if not year:
                    year = None
                summary = bb.get_yearly_summary(year)
                print(f"\n📅 Year Summary - {summary['year']}:")
                print(f"   💰 Total Spent: ${summary['total_spent']:.2f}")
                print(f"   📝 Number of Expenses: {summary['expense_count']}")
                print(f"   📊 Average Monthly: ${summary['average_monthly']:.2f}")
                if summary['category_totals']:
                    print("\n   📊 By Category:")
                    for category, amount in sorted(summary['category_totals'].items(), key=lambda x: x[1], reverse=True):
                        print(f"      {category}: ${amount:.2f}")
                if summary['monthly_totals']:
                    print("\n   📊 By Month:")
                    for month, amount in sorted(summary['monthly_totals'].items()):
                        print(f"      {month}: ${amount:.2f}")
        
        elif choice == '13':
            print("\n🔮 Predict Next Month Spending")
            prediction = bb.predict_next_month_spending()
            if 'error' in prediction:
                print(f"❌ {prediction['error']}")
            else:
                print(f"\n📊 Prediction Results:")
                print(f"   Predicted Total: ${prediction['predicted_total']:.2f}")
                print(f"   Trend: {prediction['trend']}")
                print(f"   Based on {prediction['based_on_months']} months of data")
                if prediction['predicted_by_category']:
                    print(f"\n   Predicted by Category:")
                    for category, amount in sorted(prediction['predicted_by_category'].items(), key=lambda x: x[1], reverse=True):
                        print(f"      {category}: ${amount:.2f}")
        
        elif choice == '14':
            print("\n⚙️  Manage Categories")
            print("1. List categories")
            print("2. Add category")
            print("3. Update category")
            cat_choice = input("Enter choice (1-3): ").strip()
            
            if cat_choice == '1':
                categories = bb.list_categories()
                print("\n📋 Categories:")
                for name, cat in categories.items():
                    print(f"   {cat.icon} {name} - {cat.budget_type} - Color: {cat.color}")
            
            elif cat_choice == '2':
                name = input("Category name: ").strip()
                color = input("Color (hex code, e.g., #3498db): ").strip() or "#3498db"
                icon = input("Icon (emoji): ").strip() or "📁"
                budget_type = input("Budget type (needs/wants/savings): ").strip() or "needs"
                bb.add_category(name, color, icon, budget_type)
                print("✅ Category added!")
            
            elif cat_choice == '3':
                categories = bb.list_categories()
                print("\nCategories:")
                for idx, name in enumerate(categories.keys(), 1):
                    print(f"{idx}. {name}")
                try:
                    sel = int(input("Select category number: ")) - 1
                    cat_names = list(categories.keys())
                    if 0 <= sel < len(cat_names):
                        cat_name = cat_names[sel]
                        print("Leave blank to keep current value")
                        color = input(f"Color [{categories[cat_name].color}]: ").strip() or None
                        icon = input(f"Icon [{categories[cat_name].icon}]: ").strip() or None
                        budget_type = input(f"Budget type [{categories[cat_name].budget_type}]: ").strip() or None
                        bb.update_category(cat_name, color, icon, budget_type)
                        print("✅ Category updated!")
                except (ValueError, IndexError):
                    print("❌ Invalid selection.")
        
        elif choice == '15':
            print("\n💾 Backup Data")
            backup_path = bb.backup_data()
            print(f"Backup location: {backup_path}")
        
        elif choice == '16':
            print("\n📂 Restore Data")
            backup_path = input("Enter backup folder path: ").strip()
            bb.restore_data(backup_path)
        
        elif choice == '17':
            print("\n📤 Export Data")
            format_choice = input("Export format (csv/json): ").strip().lower()
            if format_choice in ['csv', 'json']:
                export_path = bb.export_data(format_choice)
                if export_path:
                    print(f"✅ Data exported to {export_path}")
                else:
                    print("❌ No data to export")
            else:
                print("❌ Invalid format. Choose 'csv' or 'json'")
        
        elif choice == '0':
            print_header("👋 THANK YOU!", 70)
            print(f"{Colors.BOLD}{Colors.GREEN}Thanks for using BudgetBuddy!{Colors.END}")
            print(f"{Colors.GREEN}Keep up the great budgeting! 💰{Colors.END}\n")
            break
        
        else:
            print_error("Invalid choice. Please enter 0-17.")
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}")


if __name__ == "__main__":
    main()
