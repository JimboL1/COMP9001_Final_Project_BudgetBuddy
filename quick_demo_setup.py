#!/usr/bin/env python3
"""
Quick Demo Setup Script
Generate demo data quickly for BudgetBuddy demonstration
"""

from budget_buddy import BudgetBuddy, Expense, Income
from datetime import datetime, timedelta
import os

def setup_demo_data():
    """Set up demo data for BudgetBuddy"""
    print("🎯 Setting up BudgetBuddy demo data...")
    print("=" * 60)
    
    # Clear existing data
    data_dir = "data"
    if os.path.exists(data_dir):
        import shutil
        shutil.rmtree(data_dir)
        print("✓ Cleared existing data")
    
    # Initialize BudgetBuddy
    bb = BudgetBuddy(data_dir=data_dir)
    
    # Step 1: Set up budget
    print("\n📊 Setting up budget...")
    budget = bb.set_budget(2000)  # $2000 monthly income (50/30/20 rule)
    print(f"  ✓ Budget set: ${budget.total_income:.2f}/month")
    print(f"    - Needs: ${budget.needs_amount:.2f}")
    print(f"    - Wants: ${budget.wants_amount:.2f}")
    print(f"    - Savings: ${budget.savings_amount:.2f}")
    
    # Step 2: Add expenses (with different dates to simulate history)
    print("\n💸 Adding expenses...")
    expenses = [
        # Needs
        ("rent", 800, "Monthly apartment rent", -5),
        ("groceries", 150, "Weekly grocery shopping", -4),
        ("groceries", 145, "Weekly grocery shopping", -2),
        ("utilities", 120, "Electricity and water bill", -3),
        ("transport", 60, "Monthly bus and train passes", -1),
        # Wants
        ("entertainment", 80, "Movie tickets with friends", -6),
        ("dining", 120, "Restaurant meals", -3),
        ("dining", 95, "Lunch out", -1),
        ("shopping", 150, "New clothes", -7),
        ("entertainment", 65, "Concert tickets", -4),
    ]
    
    today = datetime.now().date()
    for category, amount, description, days_ago in expenses:
        expense_date = today + timedelta(days=days_ago)
        expense = Expense(
            date=expense_date.isoformat(),
            category=category,
            amount=amount,
            description=description
        )
        bb.expenses.append(expense)
        print(f"  ✓ Added: ${amount:.2f} for {category}")
    
    bb._save_expenses()
    print(f"  ✓ Total expenses added: {len(expenses)}")
    
    # Step 3: Add incomes
    print("\n💰 Adding incomes...")
    incomes = [
        ("Salary", 2000, "salary", "Monthly salary from company", -1),
        ("Part-time Job", 300, "part_time", "Weekend work", -2),
    ]
    
    for source, amount, category, description, days_ago in incomes:
        income_date = today + timedelta(days=days_ago)
        income = Income(
            date=income_date.isoformat(),
            source=source,
            amount=amount,
            category=category,
            description=description
        )
        bb.incomes.append(income)
        print(f"  ✓ Added: ${amount:.2f} from {source}")
    
    bb._save_incomes()
    print(f"  ✓ Total incomes added: {len(incomes)}")
    
    # Step 4: Add goals
    print("\n🎯 Setting up goals...")
    goals = [
        ("Vacation to Japan", 3000, "2024-12-31", "Save for Japan trip", 500),
        ("New Laptop", 1500, "2025-06-30", "MacBook Pro", 200),
    ]
    
    for name, target, deadline, description, current in goals:
        goal = bb.add_goal(name, target, deadline, description)
        bb.update_goal_progress(name, current)
        print(f"  ✓ Goal: {name} (${current}/{target})")
    
    # Step 5: Add custom category
    print("\n🏷️  Adding custom category...")
    bb.add_category("books", "#9b59b6", "📚", "wants")
    print("  ✓ Added category: books")
    
    # Step 6: Summary
    print("\n" + "=" * 60)
    print("✅ Demo data setup complete!")
    print("\n📊 Summary:")
    print(f"  - Budget: ${budget.total_income:.2f}/month")
    print(f"  - Expenses: {len(bb.expenses)} records")
    print(f"  - Incomes: {len(bb.incomes)} records")
    print(f"  - Goals: {len(bb.goals)} goals")
    print(f"  - Categories: {len(bb.categories)} categories")
    
    # Calculate total spent
    total_spent = sum(exp.amount for exp in bb.expenses)
    print(f"\n💰 Current Month Spending: ${total_spent:.2f}")
    print(f"   Remaining Budget: ${budget.total_income - total_spent:.2f}")
    
    print("\n🚀 You can now run: python3 budget_buddy.py")
    print("=" * 60)


if __name__ == "__main__":
    setup_demo_data()

