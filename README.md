# BudgetBuddy 🎯

A lightweight, Python-based monthly budgeting tool designed specifically for students. BudgetBuddy helps you manage your finances with smart allocation rules, expense tracking, and intelligent spending suggestions.

## 🚀 Features

- **Flexible Budget Allocation**: Support for 50/30/20 rule or custom percentage allocation
- **Expense Tracking**: Log daily expenses with categories and descriptions
- **Smart Suggestions**: Get personalized "shrink suggestions" when overspending occurs
- **Data Privacy**: All data stored locally in CSV/JSON format
- **Visualization**: Interactive charts using matplotlib to visualize spending patterns
- **Export Options**: Export your data in CSV or JSON format
- **Student-Friendly**: Simple CLI interface designed for beginners

## 📦 Installation

1. Clone this repository:
```bash
git clone https://github.com/JimboL1/COMP9001_Final_Project_BudgetBuddy.git
cd COMP9001_Final_Project_BudgetBuddy
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

Run the main application:
```bash
python3 budget_buddy.py
```

Or run the demo to see all features:
```bash
python3 demo.py
```

### Main Features

1. **Set up Budget**: Choose between 50/30/20 rule or custom allocation percentages
2. **Add Expenses**: Log your daily spending with categories
3. **View Summary**: See your monthly spending breakdown
4. **Get Suggestions**: Receive smart tips when you're overspending
5. **Create Charts**: Visualize your spending patterns
6. **Export Data**: Save your data for backup or analysis

### Budget Categories

- **Needs (50%)**: Rent, groceries, utilities, transport, insurance
- **Wants (30%)**: Entertainment, dining, shopping, hobbies
- **Savings (20%)**: Emergency fund, investments, future goals

## 💾 Data Storage

All data is stored locally in the `data/` directory:
- `expenses.csv`: Your expense records
- `budget.json`: Your budget configuration
- Export files: Generated when you export data

## 💻 Example Usage

```python
from budget_buddy import BudgetBuddy

# Initialize the app
bb = BudgetBuddy()

# Set up a budget with 50/30/20 rule
bb.set_budget(total_income=2000)

# Add an expense
bb.add_expense("groceries", 45.50, "Weekly grocery shopping")

# Check for overspending and get suggestions
suggestions = bb.check_overspending()
for suggestion in suggestions:
    print(suggestion)

# Create a spending chart
bb.create_chart(save_path="my_spending.png")
```

## 🧠 Smart Suggestions

BudgetBuddy analyzes your spending patterns and provides personalized suggestions:

- **Overspending Alerts**: Warns when you exceed budget limits
- **Category Analysis**: Identifies high-spending categories
- **Practical Tips**: Suggests specific ways to reduce spending
- **Pattern Recognition**: Learns from your spending history

## 📊 Screenshots

### Main Interface
![BudgetBuddy Interface](budgetbuddy_clean_screenshot.png)

### Workflow Diagram
![BudgetBuddy Workflow](budgetbuddy_flowchart.png)

### Sample Chart
![Spending Chart](demo_spending_chart.png)

## 🛠️ Requirements

- Python 3.7+
- pandas >= 1.5.0
- matplotlib >= 3.6.0
- numpy >= 1.24.0

## 🎯 Target Audience

This tool is specifically designed for:
- University students
- Recent graduates
- Young adults learning financial management
- Anyone looking for a simple, privacy-focused budgeting solution

## 🔒 Privacy & Security

- **Local Storage Only**: All data stays on your device
- **No Cloud Dependencies**: No external services required
- **Data Export**: Easy backup and migration options
- **Open Source**: Transparent code for security review

## 📈 Project Impact

- 🎓 **Educational**: Teaches students financial management
- 🔒 **Privacy**: No external data sharing
- 💡 **Smart**: Personalized suggestions based on spending patterns
- 📊 **Visual**: Charts help understand spending habits
- 🎯 **Practical**: Solves real student budgeting problems

## 🚀 Getting Started

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the application**: `python3 budget_buddy.py`
4. **Set up your budget** using the 50/30/20 rule or custom percentages
5. **Start tracking expenses** and get smart suggestions!

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve BudgetBuddy!

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for students learning financial management**
