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
OUTPUT_FILE = OUTPUT_DIR / "02_Satisfaction_by_Ticket_Type.png"

# LOAD DATA
df = pd.read_csv(DATA_FILE)
print("Dataset loaded successfully.")
print(f"Total tickets: {len(df):,}")

# VALIDATE REQUIRED COLUMNS
required_columns = [
    "ticket_type",
    "customer_satisfaction_rating",
    "satisfaction_available"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# SATISFACTION ANALYSIS
satisfaction_data = df[
    df["customer_satisfaction_rating"].notna()
].copy()

satisfaction_by_type = (
    satisfaction_data
    .groupby("ticket_type")["customer_satisfaction_rating"]
    .agg(
        rated_tickets="count",
        average_satisfaction="mean"
    )
    .reset_index()
)

satisfaction_by_type["average_satisfaction"] = (
    satisfaction_by_type["average_satisfaction"].round(2)
)

satisfaction_by_type = satisfaction_by_type.sort_values(
    "average_satisfaction",
    ascending=True
)

# CREATE VISUAL
plt.figure(figsize=(10, 6))

plt.barh(
    satisfaction_by_type["ticket_type"],
    satisfaction_by_type["average_satisfaction"]
)

plt.xlabel("Average Customer Satisfaction Rating")
plt.ylabel("Ticket Type")
plt.title("Customer Satisfaction by Ticket Type")

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# DISPLAY SIMPLE INSIGHTS
lowest_satisfaction = satisfaction_by_type.iloc[0]
highest_satisfaction = satisfaction_by_type.iloc[-1]

print("\n--- Key Findings ---")

print(
    f"Lowest average satisfaction: "
    f"{lowest_satisfaction['ticket_type']} "
    f"({lowest_satisfaction['average_satisfaction']:.2f})"
)

print(
    f"Highest average satisfaction: "
    f"{highest_satisfaction['ticket_type']} "
    f"({highest_satisfaction['average_satisfaction']:.2f})"
)

print(
    f"Total rated tickets: "
    f"{len(satisfaction_data):,}"
)

print(
    f"Overall average satisfaction: "
    f"{satisfaction_data['customer_satisfaction_rating'].mean():.2f}"
)

print(f"\nVisual saved to: {OUTPUT_FILE}")