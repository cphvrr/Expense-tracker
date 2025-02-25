import pandas as pd
import csv

# Define categories (You can customize this)
CATEGORIES = {
    "Groceries": ["coles", "woolworth", "grocery"],
    "Rent": ["rent", "landlord"],
    "Utilities": ["electric", "water", "gas"],
    "Entertainment": ["netflix", "spotify", "cinema"],
    "Salary": ["payroll", "salary", "deposit"],
    "Dining Out": ["restaurant", "mcdonalds", "starbucks"]
}


def categorize_transaction(description):
    description = description.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in description for keyword in keywords):
            return category
    return "Other"


def process_bank_statement(file_path):
    try:
        df = pd.read_csv(file_path)

        # Ensure the file has necessary columns
        required_columns = {"Date", "Description", "Amount"}
        if not required_columns.issubset(df.columns):
            raise ValueError("CSV file must contain Date, Description, and Amount columns")

        # Categorize transactions
        df["Category"] = df["Description"].apply(categorize_transaction)

        # Separate income and expenses
        df["Type"] = df["Amount"].apply(lambda x: "Income" if x > 0 else "Expense")

        # Summary Report
        summary = df.groupby(["Category", "Type"])['Amount'].sum().reset_index()
        print("Transaction Summary:")
        print(summary)

        # Save categorized transactions
        output_file = "categorized_transactions.csv"
        df.to_csv(output_file, index=False)
        print(f"Categorized transactions saved to {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")


# Example usage
if __name__ == "__main__":
    file_path = "bank_statement.csv"  # Replace with actual file path
    process_bank_statement(file_path)
