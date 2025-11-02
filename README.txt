================================================================================
BUDGETBUDDY - STUDENT BUDGETING TOOL
================================================================================

PROGRAM DESCRIPTION:
BudgetBuddy is a Python-based budgeting tool designed for students. It helps
users track expenses, manage budgets using the 50/30/20 rule or custom
percentages, monitor income, set financial goals, and generate spending
analytics and visualizations.

================================================================================
IMPORTANT: DEPENDENCIES & RUNNING ENVIRONMENT
================================================================================

This program uses the following EXTERNAL LIBRARIES (outside Python's standard
library):

PRIMARY EXTERNAL LIBRARIES (directly imported):
1. pandas >= 1.5.0
   - Used for: Data manipulation and CSV file handling
   - Automatically installs: python-dateutil, pytz

2. matplotlib >= 3.6.0
   - Used for: Generating charts and graphs (pie charts, bar charts, 
                trend lines, budget comparisons)
   - ⚠️  IMPORTANT: This is a GRAPHICS RENDERING library
   - ⚠️  CRITICAL: This program uses matplotlib for chart generation, which
      will NOT work in Ed's environment. The tutor MUST run this program
      OUTSIDE of Ed to test the chart generation features.
   - Automatically installs: pillow, kiwisolver, pyparsing, numpy

3. numpy >= 1.24.0
   - Used for: Statistical calculations (mean, median, standard deviation)
   - Note: Also installed as a dependency of matplotlib

AUTOMATIC DEPENDENCIES (installed automatically by pip):
The following libraries are automatically installed when you install the three
packages above:
- python-dateutil (required by pandas)
- pytz (required by pandas)
- pillow (required by matplotlib for image support)
- kiwisolver (required by matplotlib)
- pyparsing (required by matplotlib)

You only need to install pandas, matplotlib, and numpy. pip will automatically
handle all their dependencies.

================================================================================
INSTALLATION INSTRUCTIONS
================================================================================

Before running the program, install the required dependencies:

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Install dependencies using pip:

   pip install -r requirements.txt

   Or install individually:
   pip install pandas>=1.5.0 matplotlib>=3.6.0 numpy>=1.24.0

================================================================================
HOW TO RUN THE PROGRAM
================================================================================

METHOD 1: Quick Setup with Demo Data (RECOMMENDED FOR TESTING)
----------------------------------------------------------------
This method automatically generates sample data so you can immediately
test all features without manual data entry.

What quick_demo_setup.py does:
-------------------------------
The quick_demo_setup.py script is a utility that automatically creates a
complete dataset for testing BudgetBuddy. It:

1. Clears any existing data in the 'data/' directory
2. Creates a new BudgetBuddy instance
3. Sets up a budget ($2000/month with 50/30/20 rule)
4. Adds 10 expense records with varied dates (simulating history)
5. Adds 2 income records
6. Creates 2 financial goals with partial progress
7. Adds 1 custom category

How to use:
-----------
1. Generate demo data:
   python3 quick_demo_setup.py
   
   This will output:
   - Progress messages for each step
   - Summary of created data
   - Total spending and remaining budget

Detailed data created by quick_demo_setup.py:
---------------------------------------------

BUDGET:
  - Monthly income: $2000.00
  - Budget allocation (50/30/20 rule):
    * Needs: $1000.00 (50%)
    * Wants: $600.00 (30%)
    * Savings: $400.00 (20%)

EXPENSES (10 records):
  Needs category expenses:
  - rent: $800.00 (Monthly apartment rent)
  - groceries: $150.00 (Weekly grocery shopping)
  - groceries: $145.00 (Weekly grocery shopping)
  - utilities: $120.00 (Electricity and water bill)
  - transport: $60.00 (Monthly bus and train passes)
  
  Wants category expenses:
  - entertainment: $80.00 (Movie tickets with friends)
  - dining: $120.00 (Restaurant meals)
  - dining: $95.00 (Lunch out)
  - shopping: $150.00 (New clothes)
  - entertainment: $65.00 (Concert tickets)
  
  Total expenses: ~$1785.00
  Remaining budget: ~$215.00

INCOMES (2 records):
  - Salary: $2000.00 (Monthly salary from company)
  - Part-time Job: $300.00 (Weekend work)
  Total income: $2300.00

GOALS (2 records):
  - Vacation to Japan: $500.00 / $3000.00 (16.7% complete)
    Deadline: 2024-12-31
    Description: Save for Japan trip
  
  - New Laptop: $200.00 / $1500.00 (13.3% complete)
    Deadline: 2025-06-30
    Description: MacBook Pro

CATEGORIES:
  - 10 default categories (rent, groceries, utilities, transport,
    insurance, entertainment, dining, shopping, hobbies, savings)
  - 1 custom category: books (purple color, 📚 icon, wants type)

2. Run the main program:
   python3 budget_buddy.py
   
   Now you can immediately test features like:
   - View monthly summary (Option 4) - see all expenses categorized
   - Check budget progress (Option 6) - view progress bars and percentages
   - View statistics (Option 11) - see detailed spending analytics
   - Create charts (Option 10) - generate pie/bar/trend charts
   - Manage goals (Option 9) - view and update goal progress
   - Edit/Delete expenses (Option 3) - manage expense records
   - Income summary (Option 8) - view income breakdown
   - Multi-timeframe analysis (Option 12) - weekly/yearly summaries

Important notes about quick_demo_setup.py:
------------------------------------------
- The script will DELETE any existing data in the 'data/' directory
- Expense dates are set to different days (simulating transaction history)
- The budget is set for the current month automatically
- All data is saved immediately and persists between program runs
- You can run this script multiple times to reset your data

METHOD 2: Run the main program directly (empty start)
-----------------------------------------------------
python3 budget_buddy.py

This will start with an empty dataset. You'll need to set up budget and
add expenses manually to test features.

================================================================================
PROGRAM FEATURES
================================================================================

Core Features:
- Budget setup (50/30/20 rule or custom percentages)
- Expense tracking and management
- Income tracking
- Monthly, weekly, and yearly summaries
- Budget progress tracking with visual progress bars
- Overspending detection and smart suggestions
- Financial goal management
- Category management with custom colors and icons

Analytics & Visualization:
- Statistical analysis (mean, median, standard deviation, etc.)
- Spending trend predictions
- Multiple chart types:
  * Pie charts (spending by category)
  * Bar charts (spending comparison)
  * Trend line charts (spending over time)
  * Budget vs Actual comparison charts

Data Management:
- Export data (CSV and JSON formats)
- Backup and restore functionality
- Local data storage (CSV/JSON files in data/ directory)

================================================================================
IMPORTANT NOTES FOR TUTOR
================================================================================

1. CHART GENERATION (Options 10 in menu):
   - The program uses matplotlib to generate charts
   - Charts can be saved to PNG files or displayed in a window
   - If running in a headless environment (no display), charts will only
     be saved to files (use option 'y' when prompted)
   - Chart generation requires matplotlib and will NOT work in Ed

2. DATA STORAGE:
   - All data is stored locally in the 'data/' directory
   - No cloud services or external APIs are used
   - Data persists between program runs

3. PROGRAM MODES:
   - The program runs in interactive CLI mode
   - Menu-driven interface with numbered options (0-17)
   - All features are accessible through the main menu

4. TESTING:
   - RECOMMENDED: Run 'quick_demo_setup.py' first to generate sample data
   - This creates a complete dataset (budget, expenses, incomes, goals)
   - Allows immediate testing of all features without manual data entry
   - See 'DEMO_TEST_GUIDE.md' for comprehensive testing instructions
   - See 'test_all_features.py' for automated testing

================================================================================
FILE STRUCTURE
================================================================================

Main Files:
- budget_buddy.py          : Main program file (run this to start the app)
- requirements.txt         : Python dependencies (install with pip)
- quick_demo_setup.py      : Demo data generator (RECOMMENDED: run this first
                             to generate sample data for testing)
- test_all_features.py     : Automated test suite (run tests)
- README.txt              : This file (complete documentation)

Documentation:
- DEMO_TEST_GUIDE.md       : Detailed testing guide
- QUICK_DEMO_README.md     : Quick reference guide
- IMPLEMENTATION_SUMMARY.md: Feature implementation details
- FEATURES_ANALYSIS.md     : Feature analysis document

Data Directory (created automatically):
- data/
  - expenses.csv          : Expense records
  - incomes.csv           : Income records
  - budget.json           : Budget settings
  - categories.json       : Category definitions
  - goals.json            : Financial goals

Backup Directory (created when backing up):
- backups/                : Backup files with timestamps

================================================================================
SYSTEM REQUIREMENTS
================================================================================

- Python 3.7 or higher
- Terminal/Command Prompt access
- For chart display: A system with GUI capabilities (or use file saving mode)
- For chart generation: matplotlib must be installed (see above)

================================================================================
TROUBLESHOOTING
================================================================================

1. Import errors:
   - Ensure all dependencies are installed: pip install -r requirements.txt

2. Chart generation errors:
   - If running in headless mode, ensure you select 'y' to save charts to files
   - Charts require matplotlib - this will NOT work in Ed environment

3. Permission errors:
   - Ensure you have write permissions in the project directory
   - The program creates 'data/' and 'backups/' directories automatically

4. Data not persisting:
   - Check that 'data/' directory exists and is writable
   - Verify CSV/JSON files are being created in data/ directory

================================================================================
CONTACT & SUPPORT
================================================================================

For questions or issues, please refer to the documentation files included
in this project.

Program Version: 1.0
Last Updated: 2024

================================================================================

