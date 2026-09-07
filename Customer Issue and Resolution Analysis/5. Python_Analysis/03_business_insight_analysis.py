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
OUTPUT_FILE = OUTPUT_DIR / "03_Volume_vs_Satisfaction.png"

# LOAD DATA
df = pd.read_csv(DATA_FILE)
print("Dataset loaded successfully.")
print(f"Total tickets: {len(df):,}")

# VALIDATE REQUIRED COLUMNS
required_columns = [
    "product_purchased",
    "ticket_subject",
    "customer_satisfaction_rating"
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
    .agg(
        ticket_volume=("ticket_subject", "size"),
        average_satisfaction=(
            "customer_satisfaction_rating",
            "mean"
        )
    )
    .reset_index()
)

product_issue["average_satisfaction"] = (
    product_issue["average_satisfaction"].round(2)
)

# REMOVE COMBINATIONS WITHOUT A SATISFACTION RATING
product_issue = product_issue[
    product_issue["average_satisfaction"].notna()
].copy()

# SELECT IMPORTANT COMBINATIONS
# Keep combinations with at least 20 tickets
# to avoid highlighting very small groups.
analysis_data = product_issue[
    product_issue["ticket_volume"] >= 20
].copy()

# CREATE VISUAL
plt.figure(figsize=(10, 7))

plt.scatter(
    analysis_data["ticket_volume"],
    analysis_data["average_satisfaction"]
)

plt.xlabel("Ticket Volume")
plt.ylabel("Average Customer Satisfaction")
plt.title("Ticket Volume vs Customer Satisfaction")

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# DISPLAY SIMPLE BUSINESS INSIGHTS
highest_volume = analysis_data.loc[
    analysis_data["ticket_volume"].idxmax()
]

lowest_satisfaction = analysis_data.loc[
    analysis_data["average_satisfaction"].idxmin()
]

print("\n--- Key Findings ---")

print(
    f"Highest-volume product-issue combination: "
    f"{highest_volume['product_purchased']} - "
    f"{highest_volume['ticket_subject']}"
)

print(
    f"Ticket volume: "
    f"{int(highest_volume['ticket_volume']):,}"
)

print(
    f"Lowest-satisfaction product-issue combination "
    f"(among groups with at least 20 tickets): "
    f"{lowest_satisfaction['product_purchased']} - "
    f"{lowest_satisfaction['ticket_subject']}"
)

print(
    f"Average satisfaction: "
    f"{lowest_satisfaction['average_satisfaction']:.2f}"
)

print(
    f"Product-issue combinations analyzed: "
    f"{len(analysis_data):,}"
)

print(f"\nVisual saved to: {OUTPUT_FILE}")