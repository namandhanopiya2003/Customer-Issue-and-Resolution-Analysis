import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# FILE PATHS
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = (
    BASE_DIR.parent
    / "3. Data_Cleaning"
    / "Generated_Files"
    / "customer_tickets_cleaned.csv"
)

OUTPUT_DIR = BASE_DIR / "Generated_Files"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "01_Top_Product_Issue_Combinations.png"

# LOAD DATA
df = pd.read_csv(DATA_FILE)
print("Dataset loaded successfully.")
print(f"Total tickets: {len(df):,}")

# VALIDATE REQUIRED COLUMNS
required_columns = [
    "product_purchased",
    "ticket_subject"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# PRODUCT + ISSUE ANALYSIS
product_issue = (
    df.groupby(
        ["product_purchased", "ticket_subject"]
    )
    .size()
    .reset_index(name="ticket_count")
    .sort_values("ticket_count", ascending=False)
)

top_product_issue = product_issue.head(10).copy()

top_product_issue["label"] = (
    top_product_issue["product_purchased"]
    + " - "
    + top_product_issue["ticket_subject"]
)

# CREATE VISUAL
plt.figure(figsize=(10, 6))

plt.barh(
    top_product_issue["label"],
    top_product_issue["ticket_count"]
)

plt.xlabel("Number of Tickets")
plt.ylabel("Product - Issue")
plt.title("Top 10 Product- Issue Combinations by Ticket Volume")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# DISPLAY SIMPLE INSIGHTS
top_combination = top_product_issue.iloc[0]

print("\n--- Key Findings ---")

print(
    f"Most common product-issue combination: "
    f"{top_combination['product_purchased']} - "
    f"{top_combination['ticket_subject']}"
)

print(
    f"Ticket volume for this combination: "
    f"{int(top_combination['ticket_count']):,}"
)

print(
    f"Unique product-issue combinations: "
    f"{len(product_issue):,}"
)

print(f"\nVisual saved to: {OUTPUT_FILE}")