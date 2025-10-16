#!/usr/bin/env python3
"""
Demo script for BudgetBuddy
Shows how to use the main features programmatically
"""

from budget_buddy import BudgetBuddy
from datetime import datetime

def main():
    print("🎯 BudgetBuddy Demo")
    print("=" * 40)
    
    # Initialize BudgetBuddy
    bb = BudgetBuddy()
    
    # Set up a budget with 50/30/20 rule
    print("\n1. Setting up budget with 50/30/20 rule...")
    budget = bb.set_budget(total_income=2000)
    print(f"   💰 Total Income: ${budget.total_income}")
    print(f"   🏠 Needs (50%): ${budget.needs_amount}")
    print(f"   🎯 Wants (30%): ${budget.wants_amount}")
    print(f"   💎 Savings (20%): ${budget.savings_amount}")
    
    # Add some sample expenses
    print("\n2. Adding sample expenses...")
    expenses = [
        ("rent", 800, "Monthly rent"),
        ("groceries", 200, "Weekly groceries"),
        ("utilities", 150, "Electricity and water"),
        ("entertainment", 100, "Movies and games"),
        ("dining", 80, "Restaurant meals"),
        ("transport", 60, "Bus and train tickets"),
        ("shopping", 120, "Clothes and accessories")
    ]
    
    for category, amount, description in expenses:
        expense = bb.add_expense(category, amount, description)
        print(f"   ✅ Added: ${expense.amount} for {expense.category}")
    
    # Get monthly summary
    print("\n3. Monthly Summary:")
    summary = bb.get_monthly_summary()
    print(f"   💰 Total Spent: ${summary['total_spent']}")
    print(f"   📝 Number of Expenses: {summary['expense_count']}")
    print("   📊 By Category:")
    for category, amount in summary['category_totals'].items():
        print(f"      {category}: ${amount}")
    
    # Check for overspending and get suggestions
    print("\n4. Overspending Check & Smart Suggestions:")
    suggestions = bb.check_overspending()
    for suggestion in suggestions:
        print(f"   {suggestion}")
    
    # Create a chart
    print("\n5. Creating spending chart...")
    try:
        chart_path = "demo_spending_chart.png"
        bb.create_chart(save_path=chart_path)
        print(f"   📈 Chart saved to {chart_path}")
    except Exception as e:
        print(f"   ❌ Error creating chart: {e}")
    
    # Export data
    print("\n6. Exporting data...")
    csv_path = bb.export_data('csv')
    json_path = bb.export_data('json')
    print(f"   📤 CSV export: {csv_path}")
    print(f"   📤 JSON export: {json_path}")
    
    print("\n🎉 Demo completed! Check the 'data' folder for your files.")

if __name__ == "__main__":
    main()
