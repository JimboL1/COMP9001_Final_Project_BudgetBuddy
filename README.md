# BudgetBuddy 🎯

A simple Python budgeting tool for students. Track your expenses, set budgets, and get smart suggestions.

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the app:**
```bash
python3 budget_buddy.py
```

3. **Try the demo:**
```bash
python3 demo.py
```

## Features

- **Budget Setup**: 50/30/20 rule or custom percentages
- **Expense Tracking**: Log daily spending by category
- **Smart Suggestions**: Get tips when you overspend
- **Local Storage**: All data stays on your device
- **Simple Charts**: Visualize your spending

## How to Use

1. Set up your monthly budget
2. Add your daily expenses
3. Check your spending summary
4. Get smart suggestions
5. Create charts to see your patterns

## Budget Categories

- **Needs (50%)**: Rent, groceries, utilities, transport
- **Wants (30%)**: Entertainment, dining, shopping
- **Savings (20%)**: Emergency fund, future goals

## Example

```python
from budget_buddy import BudgetBuddy

# Start the app
bb = BudgetBuddy()

# Set budget
bb.set_budget(total_income=2000)

# Add expense
bb.add_expense("groceries", 45.50, "Weekly shopping")

# Check suggestions
suggestions = bb.check_overspending()
```

## Requirements

- Python 3.7+
- pandas
- matplotlib
- numpy

## Data Storage

All data is saved locally in CSV/JSON files in the `data/` folder.

## Target Users

- University students
- Young adults learning budgeting
- Anyone wanting simple expense tracking

## Privacy

- No cloud storage
- No external services
- All data stays on your device

---

**Made for students, by students** 🎓
