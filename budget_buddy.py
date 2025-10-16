#!/usr/bin/env python3
"""
BudgetBuddy - A lightweight monthly budgeting tool for students
Supports 50/30/20 or custom allocation rules, expense tracking, and smart suggestions
"""

import json
import csv
import os
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass, asdict


@dataclass
class Expense:
    """Represents a single expense entry"""
    date: str
    category: str
    amount: float
    description: str


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


class BudgetBuddy:
    """Main BudgetBuddy application class"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.expenses_file = os.path.join(data_dir, "expenses.csv")
        self.budget_file = os.path.join(data_dir, "budget.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.expenses = self._load_expenses()
        self.budget = self._load_budget()
    
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
    
    def export_data(self, format: str = 'csv') -> str:
        """Export all data in specified format"""
        if format.lower() == 'csv':
            # Export expenses
            if self.expenses:
                df = pd.DataFrame([asdict(expense) for expense in self.expenses])
                export_path = os.path.join(self.data_dir, f"export_{datetime.now().strftime('%Y%m%d')}.csv")
                df.to_csv(export_path, index=False)
                return export_path
        elif format.lower() == 'json':
            # Export both expenses and budget
            export_data = {
                'budget': asdict(self.budget) if self.budget else None,
                'expenses': [asdict(expense) for expense in self.expenses]
            }
            export_path = os.path.join(self.data_dir, f"export_{datetime.now().strftime('%Y%m%d')}.json")
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            return export_path
        
        return ""


def main():
    """Main CLI interface for BudgetBuddy"""
    print("🎯 Welcome to BudgetBuddy - Your Student Budgeting Companion!")
    print("=" * 60)
    
    # Initialize BudgetBuddy
    bb = BudgetBuddy()
    
    while True:
        print("\n📋 Main Menu:")
        print("1. Set up budget")
        print("2. Add expense")
        print("3. View monthly summary")
        print("4. Check overspending & get suggestions")
        print("5. Create spending chart")
        print("6. Export data")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\n💰 Budget Setup")
            print("Choose allocation method:")
            print("1. 50/30/20 rule (50% needs, 30% wants, 20% savings)")
            print("2. Custom percentages")
            
            method = input("Enter choice (1-2): ").strip()
            
            try:
                income = float(input("Enter your monthly income: $"))
                
                if method == '1':
                    budget = bb.set_budget(income)
                    print(f"✅ Budget set with 50/30/20 rule:")
                else:
                    needs_pct = float(input("Needs percentage (e.g., 50): "))
                    wants_pct = float(input("Wants percentage (e.g., 30): "))
                    savings_pct = float(input("Savings percentage (e.g., 20): "))
                    budget = bb.set_budget(income, needs_pct, wants_pct, savings_pct)
                    print(f"✅ Custom budget set:")
                
                print(f"   💰 Total Income: ${budget.total_income:.2f}")
                print(f"   🏠 Needs (${budget.needs_percentage}%): ${budget.needs_amount:.2f}")
                print(f"   🎯 Wants (${budget.wants_percentage}%): ${budget.wants_amount:.2f}")
                print(f"   💎 Savings (${budget.savings_percentage}%): ${budget.savings_amount:.2f}")
                
            except ValueError:
                print("❌ Invalid input. Please enter valid numbers.")
        
        elif choice == '2':
            print("\n💸 Add Expense")
            try:
                category = input("Category (e.g., groceries, rent, entertainment): ").strip()
                amount = float(input("Amount: $"))
                description = input("Description (optional): ").strip()
                
                expense = bb.add_expense(category, amount, description)
                print(f"✅ Expense added: ${expense.amount:.2f} for {expense.category}")
                
            except ValueError:
                print("❌ Invalid input. Please enter valid numbers.")
        
        elif choice == '3':
            print("\n📊 Monthly Summary")
            month = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
            if not month:
                month = None
            
            summary = bb.get_monthly_summary(month)
            print(f"\n📅 {summary['month']} Summary:")
            print(f"   💰 Total Spent: ${summary['total_spent']:.2f}")
            print(f"   📝 Number of Expenses: {summary['expense_count']}")
            
            if summary['category_totals']:
                print("\n   📊 By Category:")
                for category, amount in summary['category_totals'].items():
                    print(f"      {category}: ${amount:.2f}")
        
        elif choice == '4':
            print("\n🔍 Overspending Check & Suggestions")
            month = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
            if not month:
                month = None
            
            suggestions = bb.check_overspending(month)
            print(f"\n💡 Smart Suggestions:")
            for suggestion in suggestions:
                print(f"   {suggestion}")
        
        elif choice == '5':
            print("\n📈 Create Spending Chart")
            month = input("Enter month (YYYY-MM) or press Enter for current month: ").strip()
            if not month:
                month = None
            
            save_option = input("Save chart to file? (y/n): ").strip().lower()
            save_path = None
            if save_option == 'y':
                save_path = os.path.join(bb.data_dir, f"spending_chart_{month or datetime.now().strftime('%Y-%m')}.png")
            
            try:
                bb.create_chart(month, save_path)
                if save_path:
                    print(f"✅ Chart saved to {save_path}")
            except Exception as e:
                print(f"❌ Error creating chart: {e}")
        
        elif choice == '6':
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
        
        elif choice == '7':
            print("\n👋 Thanks for using BudgetBuddy! Keep up the great budgeting!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
