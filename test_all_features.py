#!/usr/bin/env python3
"""
Comprehensive test script for all BudgetBuddy features
Tests all 10 new features and existing functionality
"""

import os
import shutil
from datetime import datetime, date, timedelta
from budget_buddy import BudgetBuddy

def print_test_header(test_name):
    """Print a formatted test header"""
    print("\n" + "="*70)
    print(f"🧪 TEST: {test_name}")
    print("="*70)

def print_test_result(test_name, passed):
    """Print test result"""
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"\n{status}: {test_name}")

def test_backup_restore():
    """Test backup and restore functionality"""
    print_test_header("Backup & Restore")
    
    # Create test instance
    bb = BudgetBuddy(data_dir="test_data")
    
    # Add some test data
    bb.set_budget(2000)
    bb.add_expense("groceries", 100, "Test expense")
    bb.add_income("Salary", 2000, "salary", "Test income")
    
    # Test backup
    try:
        backup_path = bb.backup_data(backup_dir="test_backups")
        passed = os.path.exists(backup_path)
        print_test_result("Backup Creation", passed)
        
        if passed:
            # Test restore
            # Create new instance and restore
            bb2 = BudgetBuddy(data_dir="test_data_restored")
            passed_restore = bb2.restore_data(backup_path)
            print_test_result("Restore Data", passed_restore)
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        if os.path.exists("test_data_restored"):
            shutil.rmtree("test_data_restored")
        if os.path.exists("test_backups"):
            shutil.rmtree("test_backups")
            
        return passed and passed_restore
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_edit_delete_expense():
    """Test expense editing and deletion"""
    print_test_header("Edit/Delete Expense")
    
    bb = BudgetBuddy(data_dir="test_data")
    bb.add_expense("groceries", 50, "Original")
    
    try:
        # Test list expenses
        expenses = bb.list_expenses()
        assert len(expenses) > 0, "Should have expenses"
        print("✅ List expenses works")
        
        # Test edit expense
        if expenses:
            idx, expense = expenses[0]
            edited = bb.edit_expense(idx, "dining", 75, "Edited expense")
            assert edited is not None, "Edit should return expense"
            assert edited.category == "dining", "Category should be updated"
            assert edited.amount == 75, "Amount should be updated"
            print("✅ Edit expense works")
        
        # Test delete expense
        expenses_before = len(bb.expenses)
        if expenses:
            idx, _ = expenses[0]
            deleted = bb.delete_expense(idx)
            assert deleted, "Delete should return True"
            assert len(bb.expenses) == expenses_before - 1, "Expense count should decrease"
            print("✅ Delete expense works")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_income_tracking():
    """Test income tracking functionality"""
    print_test_header("Income Tracking")
    
    bb = BudgetBuddy(data_dir="test_data")
    
    try:
        # Test add income
        income1 = bb.add_income("Salary", 2000, "salary", "Monthly salary")
        assert income1.amount == 2000, "Income amount should match"
        assert income1.source == "Salary", "Income source should match"
        print("✅ Add income works")
        
        # Test income summary
        summary = bb.get_income_summary()
        assert summary['total_income'] == 2000, "Total income should match"
        assert "Salary" in summary['source_totals'], "Salary should be in sources"
        print("✅ Income summary works")
        
        # Add multiple incomes
        bb.add_income("Part-time", 500, "part_time", "Weekend job")
        summary2 = bb.get_income_summary()
        assert summary2['total_income'] == 2500, "Total should be sum of all incomes"
        print("✅ Multiple incomes work")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_category_management():
    """Test category management"""
    print_test_header("Category Management")
    
    bb = BudgetBuddy(data_dir="test_data")
    
    try:
        # Test list categories
        categories = bb.list_categories()
        assert len(categories) > 0, "Should have default categories"
        print(f"✅ Found {len(categories)} default categories")
        
        # Test add category
        new_cat = bb.add_category("books", "#9b59b6", "📚", "wants")
        assert "books" in bb.categories, "New category should be added"
        print("✅ Add category works")
        
        # Test update category
        updated = bb.update_category("books", color="#e74c3c", icon="📖")
        assert updated is not None, "Update should return category"
        assert bb.categories["books"].color == "#e74c3c", "Color should be updated"
        print("✅ Update category works")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_charts():
    """Test chart creation functions"""
    print_test_header("Chart Creation")
    
    bb = BudgetBuddy(data_dir="test_data")
    bb.set_budget(2000)
    
    # Add test expenses
    bb.add_expense("groceries", 200, "Test")
    bb.add_expense("dining", 150, "Test")
    bb.add_expense("transport", 100, "Test")
    
    try:
        # Test pie chart
        chart_path = "test_charts/pie_test.png"
        os.makedirs("test_charts", exist_ok=True)
        bb.create_chart(save_path=chart_path)
        passed_pie = os.path.exists(chart_path)
        print_test_result("Pie Chart", passed_pie)
        
        # Test bar chart
        bar_path = "test_charts/bar_test.png"
        bb.create_bar_chart(save_path=bar_path)
        passed_bar = os.path.exists(bar_path)
        print_test_result("Bar Chart", passed_bar)
        
        # Test trend chart
        trend_path = "test_charts/trend_test.png"
        bb.create_trend_chart(months=3, save_path=trend_path)
        passed_trend = os.path.exists(trend_path)
        print_test_result("Trend Chart", passed_trend)
        
        # Test budget vs actual
        compare_path = "test_charts/compare_test.png"
        bb.create_budget_vs_actual_chart(save_path=compare_path)
        passed_compare = os.path.exists(compare_path)
        print_test_result("Budget vs Actual Chart", passed_compare)
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        if os.path.exists("test_charts"):
            shutil.rmtree("test_charts")
        
        return all([passed_pie, passed_bar, passed_trend, passed_compare])
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_budget_progress():
    """Test budget progress tracking"""
    print_test_header("Budget Progress")
    
    bb = BudgetBuddy(data_dir="test_data")
    bb.set_budget(2000)  # 50/30/20 = 1000/600/400
    
    # Add expenses in different categories
    bb.add_expense("rent", 800, "Rent")
    bb.add_expense("groceries", 150, "Groceries")
    bb.add_expense("entertainment", 200, "Entertainment")
    
    try:
        progress = bb.get_budget_progress()
        assert 'needs' in progress, "Should have needs data"
        assert 'wants' in progress, "Should have wants data"
        assert 'total' in progress, "Should have total data"
        
        assert progress['needs']['spent'] > 0, "Needs spending should be tracked"
        assert progress['needs']['percent'] <= 100, "Percent should be valid"
        print("✅ Budget progress tracking works")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multi_timeframe():
    """Test multi-timeframe analysis"""
    print_test_header("Multi-Timeframe Analysis")
    
    bb = BudgetBuddy(data_dir="test_data")
    
    # Add expenses with different dates
    today = date.today()
    bb.add_expense("groceries", 50, "Today")
    
    try:
        # Test weekly summary
        weekly = bb.get_weekly_summary()
        assert 'week_start' in weekly, "Should have week_start"
        assert 'total_spent' in weekly, "Should have total_spent"
        print("✅ Weekly summary works")
        
        # Test yearly summary
        yearly = bb.get_yearly_summary()
        assert 'year' in yearly, "Should have year"
        assert 'total_spent' in yearly, "Should have total_spent"
        assert 'average_monthly' in yearly, "Should have average_monthly"
        print("✅ Yearly summary works")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_goals():
    """Test goal management"""
    print_test_header("Goal Management")
    
    bb = BudgetBuddy(data_dir="test_data")
    
    try:
        # Test add goal
        goal = bb.add_goal("Vacation", 2000, "2024-12-31", "Trip to Europe")
        assert goal.target_amount == 2000, "Goal target should match"
        assert len(bb.goals) == 1, "Should have one goal"
        print("✅ Add goal works")
        
        # Test update goal progress
        updated = bb.update_goal_progress("Vacation", 500)
        assert updated is not None, "Update should return goal"
        assert updated.current_amount == 500, "Progress should be updated"
        print("✅ Update goal progress works")
        
        # Test get goals status
        status = bb.get_goals_status()
        assert len(status) == 1, "Should have one goal status"
        assert status[0]['progress'] == 25.0, "Progress should be 25%"
        print("✅ Get goals status works")
        
        # Test goal completion
        bb.update_goal_progress("Vacation", 1500)
        status2 = bb.get_goals_status()
        assert status2[0]['is_completed'] == True, "Goal should be completed"
        print("✅ Goal completion works")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_trend_prediction():
    """Test trend prediction"""
    print_test_header("Trend Prediction")
    
    bb = BudgetBuddy(data_dir="test_data")
    
    # Add expenses for multiple months
    # This is a simplified test - in reality you'd need expenses spanning months
    for i in range(5):
        bb.add_expense("groceries", 100 + i*10, f"Test {i}")
    
    try:
        prediction = bb.predict_next_month_spending()
        
        # If we have enough data, check prediction structure
        if 'error' not in prediction:
            assert 'predicted_total' in prediction, "Should have predicted_total"
            assert 'trend' in prediction, "Should have trend"
            print("✅ Trend prediction structure is correct")
        else:
            print(f"⚠️  {prediction['error']} (expected if insufficient data)")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_statistics():
    """Test statistics functionality"""
    print_test_header("Statistics")
    
    bb = BudgetBuddy(data_dir="test_data")
    
    # Add test expenses
    bb.add_expense("groceries", 50, "Test 1")
    bb.add_expense("groceries", 75, "Test 2")
    bb.add_expense("dining", 100, "Test 3")
    bb.add_expense("transport", 25, "Test 4")
    
    try:
        stats = bb.get_statistics()
        assert 'total_spent' in stats, "Should have total_spent"
        assert 'average_expense' in stats, "Should have average_expense"
        assert 'median_expense' in stats, "Should have median_expense"
        assert 'most_frequent_category' in stats, "Should have most_frequent_category"
        assert stats['most_frequent_category']['name'] == "groceries", "Should identify most frequent"
        print("✅ Statistics calculation works")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_basic_functionality():
    """Test basic existing functionality"""
    print_test_header("Basic Functionality")
    
    bb = BudgetBuddy(data_dir="test_data")
    
    try:
        # Test budget setup
        budget = bb.set_budget(2000)
        assert budget.total_income == 2000, "Budget should be set"
        print("✅ Budget setup works")
        
        # Test add expense
        expense = bb.add_expense("groceries", 100, "Test")
        assert expense.amount == 100, "Expense should be added"
        print("✅ Add expense works")
        
        # Test monthly summary
        summary = bb.get_monthly_summary()
        assert summary['total_spent'] == 100, "Summary should calculate correctly"
        print("✅ Monthly summary works")
        
        # Test overspending check
        suggestions = bb.check_overspending()
        assert len(suggestions) > 0, "Should have suggestions"
        print("✅ Overspending check works")
        
        # Test export
        export_path = bb.export_data('json')
        assert os.path.exists(export_path), "Export should create file"
        print("✅ Export works")
        
        # Cleanup
        if os.path.exists("test_data"):
            shutil.rmtree("test_data")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 BUDGETBUDDY COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Edit/Delete Expense", test_edit_delete_expense),
        ("Income Tracking", test_income_tracking),
        ("Category Management", test_category_management),
        ("Chart Creation", test_charts),
        ("Budget Progress", test_budget_progress),
        ("Multi-Timeframe Analysis", test_multi_timeframe),
        ("Goal Management", test_goals),
        ("Trend Prediction", test_trend_prediction),
        ("Statistics", test_statistics),
        ("Backup & Restore", test_backup_restore),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*70)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*70 + "\n")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()

