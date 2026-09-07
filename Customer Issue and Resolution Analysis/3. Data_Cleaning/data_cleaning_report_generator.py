from pathlib import Path
import pandas as pd

# FILE PATHS
cleaning_folder = Path(__file__).parent
project_folder = cleaning_folder.parent
raw_file = project_folder / "2. Sample_Dataset" / "customer_tickets.csv"
generated_folder = cleaning_folder / "Generated_Files"
generated_folder.mkdir(exist_ok=True)
report_file = generated_folder / "data_cleaning_generated_report.txt"

# LOAD RAW DATA
print("Loading raw dataset...")

try:
    df = pd.read_csv(raw_file)
except FileNotFoundError:
    print("ERROR: customer_tickets.csv was not found.")
    print(f"Expected location: {raw_file}")
    raise
except Exception as e:
    print(f"ERROR while reading the dataset: {e}")
    raise

# START REPORT
report = []

report.append("=" * 75)
report.append("CUSTOMER ISSUE & RESOLUTION ANALYSIS")
report.append("MODULE 3 - DATA CLEANING & PREPARATION")
report.append("=" * 75)

# BASIC DATASET INFORMATION
report.append("\n1. BASIC DATASET INFORMATION")
report.append("-" * 75)
report.append(f"Number of rows    : {df.shape[0]}")
report.append(f"Number of columns : {df.shape[1]}")
report.append("\nColumn Names:")

for i, column in enumerate(df.columns, start=1):
    report.append(f"{i}. {column}")

# DATA TYPES
report.append("\n\n2. DATA TYPES")
report.append("-" * 75)

for column in df.columns:
    report.append(f"{column}: {df[column].dtype}")

# MISSING VALUES
report.append("\n\n3. MISSING VALUES")
report.append("-" * 75)

missing_count = df.isnull().sum()
missing_percentage = (missing_count / len(df)) * 100

missing_table = pd.DataFrame({
    "Missing Values": missing_count,
    "Missing Percentage": missing_percentage.round(2)
})

report.append(missing_table.to_string())

# DUPLICATE CHECK
report.append("\n\n4. DUPLICATE CHECK")
report.append("-" * 75)

duplicate_rows = df.duplicated().sum()
report.append(f"Duplicate rows: {duplicate_rows}")

if "Ticket ID" in df.columns:
    duplicate_ticket_ids = df["Ticket ID"].duplicated().sum()
    report.append(f"Duplicate Ticket IDs: {duplicate_ticket_ids}")

# UNIQUE VALUES FOR CATEGORICAL COLUMNS
report.append("\n\n5. CATEGORICAL VALUE VALIDATION")
report.append("-" * 75)

categorical_columns = [
    "Customer Gender",
    "Product Purchased",
    "Ticket Type",
    "Ticket Subject",
    "Ticket Status",
    "Ticket Priority",
    "Ticket Channel"
]

for column in categorical_columns:
    if column not in df.columns:
        continue

    report.append(f"\n{column}")
    report.append(f"Number of unique values: {df[column].nunique()}")

    values = df[column].dropna().unique()

    for value in sorted(values, key=str):
        report.append(f"  - {value}")

# NUMERICAL VALIDATION
report.append("\n\n6. NUMERICAL DATA VALIDATION")
report.append("-" * 75)

numerical_columns = [
    "Customer Age",
    "Customer Satisfaction Rating"
]

for column in numerical_columns:
    if column not in df.columns:
        continue

    report.append(f"\n{column}")
    report.append(f"Minimum : {df[column].min()}")
    report.append(f"Maximum : {df[column].max()}")
    report.append(f"Mean    : {df[column].mean():.2f}")
    report.append(f"Median  : {df[column].median()}")

# DATE AND TIME VALIDATION
report.append("\n\n7. DATE / TIME VALIDATION")
report.append("-" * 75)

datetime_columns = [
    "Date of Purchase",
    "First Response Time",
    "Time to Resolution"
]

converted_dates = {}

for column in datetime_columns:
    if column not in df.columns:
        continue

    converted = pd.to_datetime(df[column], errors="coerce")
    converted_dates[column] = converted

    valid_values = converted.notna().sum()
    invalid_values = converted.isna().sum()

    report.append(f"\n{column}")
    report.append(f"Valid date/time values   : {valid_values}")
    report.append(f"Invalid/blank values     : {invalid_values}")

    if valid_values > 0:
        report.append(f"Earliest value           : {converted.min()}")
        report.append(f"Latest value             : {converted.max()}")

# STATUS DISTRIBUTION
report.append("\n\n8. TICKET STATUS DISTRIBUTION")
report.append("-" * 75)

if "Ticket Status" in df.columns:
    status_counts = df["Ticket Status"].value_counts(dropna=False)
    report.append(status_counts.to_string())

# PRIORITY DISTRIBUTION
report.append("\n\n9. TICKET PRIORITY DISTRIBUTION")
report.append("-" * 75)

if "Ticket Priority" in df.columns:
    priority_counts = df["Ticket Priority"].value_counts(dropna=False)
    report.append(priority_counts.to_string())

# CHANNEL DISTRIBUTION
report.append("\n\n10. TICKET CHANNEL DISTRIBUTION")
report.append("-" * 75)

if "Ticket Channel" in df.columns:
    channel_counts = df["Ticket Channel"].value_counts(dropna=False)
    report.append(channel_counts.to_string())

# TICKET TYPE DISTRIBUTION
report.append("\n\n11. TICKET TYPE DISTRIBUTION")
report.append("-" * 75)

if "Ticket Type" in df.columns:
    type_counts = df["Ticket Type"].value_counts(dropna=False)
    report.append(type_counts.to_string())

# PRODUCT DISTRIBUTION
report.append("\n\n12. PRODUCT DISTRIBUTION")
report.append("-" * 75)

if "Product Purchased" in df.columns:
    product_counts = df["Product Purchased"].value_counts(dropna=False)
    report.append(product_counts.to_string())

# SATISFACTION DISTRIBUTION
report.append("\n\n13. CUSTOMER SATISFACTION DISTRIBUTION")
report.append("-" * 75)

if "Customer Satisfaction Rating" in df.columns:
    satisfaction_counts = (
        df["Customer Satisfaction Rating"]
        .value_counts(dropna=False)
        .sort_index()
    )

    report.append(satisfaction_counts.to_string())

# LOGICAL DATA QUALITY CHECKS
report.append("\n\n14. LOGICAL DATA QUALITY CHECKS")
report.append("-" * 75)

# CUSTOMER AGE
if "Customer Age" in df.columns:
    invalid_age = (
        (df["Customer Age"] < 18)
        | (df["Customer Age"] > 100)
    ).sum()

    report.append(f"Invalid customer ages: {invalid_age}")

# SATISFACTION
if "Customer Satisfaction Rating" in df.columns:
    invalid_satisfaction = (
        df["Customer Satisfaction Rating"].notna()
        & ~df["Customer Satisfaction Rating"].between(1, 5)
    ).sum()

    report.append(
        f"Invalid satisfaction ratings (outside 1-5): "
        f"{invalid_satisfaction}"
    )

# STATUS VS MISSINGNESS CHECK
report.append("\n\n15. STATUS VS MISSING VALUES")
report.append("-" * 75)

if "Ticket Status" in df.columns:
    columns_to_check = [
        "Resolution",
        "Time to Resolution",
        "Customer Satisfaction Rating",
        "First Response Time"
    ]

    for column in columns_to_check:
        if column not in df.columns:
            continue

        report.append(f"\n{column} missing values by Ticket Status:")

        status_missing = (
            df.groupby("Ticket Status")[column]
            .apply(lambda x: x.isna().sum())
        )

        report.append(status_missing.to_string())

# TICKET ID VALIDATION
report.append("\n\n16. TICKET ID VALIDATION")
report.append("-" * 75)

if "Ticket ID" in df.columns:
    report.append(f"Minimum Ticket ID: {df['Ticket ID'].min()}")
    report.append(f"Maximum Ticket ID: {df['Ticket ID'].max()}")
    report.append(f"Unique Ticket IDs : {df['Ticket ID'].nunique()}")
    report.append(f"Total records     : {len(df)}")

# TEXT FIELD INSPECTION
report.append("\n\n17. TEXT FIELD QUALITY CHECK")
report.append("-" * 75)

text_columns = [
    "Ticket Description",
    "Resolution"
]

for column in text_columns:
    if column not in df.columns:
        continue

    text_data = df[column].dropna().astype(str)
    empty_strings = (text_data.str.strip() == "").sum()

    report.append(f"\n{column}")
    report.append(f"Non-missing values : {len(text_data)}")
    report.append(f"Empty/blank strings: {empty_strings}")

    if len(text_data) > 0:
        text_lengths = text_data.str.len()

        report.append(f"Minimum text length: {text_lengths.min()}")
        report.append(f"Maximum text length: {text_lengths.max()}")
        report.append(f"Average text length: {text_lengths.mean():.2f}")

# DATE CONSISTENCY CHECK
report.append("\n\n18. DATE CONSISTENCY CHECK")
report.append("-" * 75)

if "Date of Purchase" in df.columns:
    purchase_dates = pd.to_datetime(
        df["Date of Purchase"],
        errors="coerce"
    )

    report.append(
        f"Purchase dates before 2022: "
        f"{(purchase_dates < '2022-01-01').sum()}"
    )

    report.append(
        f"Purchase dates from 2022 onward: "
        f"{(purchase_dates >= '2022-01-01').sum()}"
    )

# FINAL REPORT
report.append("\n\n" + "=" * 75)
report.append("DATA CLEANING INSPECTION COMPLETE")
report.append("=" * 75)

# WRITE REPORT TO FILE
with open(report_file, "w", encoding="utf-8") as file:
    file.write("\n".join(report))

print("\nInspection completed successfully.")
print(f"Report created at:\n{report_file}")