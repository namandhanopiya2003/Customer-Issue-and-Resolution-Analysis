import pandas as pd
from pathlib import Path

# FILE LOCATIONS
folder = Path(__file__).parent
csv_file = folder / "customer_tickets.csv"
generated_folder = folder / "Generated_Files"
generated_folder.mkdir(exist_ok=True)
report_file = generated_folder / "dataset_inspection_report.txt"

# LOAD DATASET
df = pd.read_csv(csv_file)

# CREATE REPORT
with open(report_file, "w", encoding="utf-8") as report:

    def write(text=""):
        report.write(text + "\n")

    write("=" * 70)
    write("CUSTOMER TICKETS - DATASET INSPECTION REPORT")
    write("=" * 70)

    # BASIC INFORMATION
    write("\n1. BASIC INFORMATION")
    write("-" * 70)
    write(f"Number of rows    : {df.shape[0]}")
    write(f"Number of columns : {df.shape[1]}")
    write("\nColumn Names:")

    for i, column in enumerate(df.columns, start=1):
        write(f"{i}. {column}")

    # DATA TYPES
    write("\n\n2. DATA TYPES")
    write("-" * 70)

    for column in df.columns:
        write(f"{column}: {df[column].dtype}")

    # MISSING VALUES
    write("\n\n3. MISSING VALUES")
    write("-" * 70)

    missing = df.isnull().sum()
    missing_percentage = (missing / len(df)) * 100

    missing_report = pd.DataFrame({
        "Missing Values": missing,
        "Missing Percentage": missing_percentage.round(2)
    })

    write(missing_report.to_string())

    # DUPLICATE RECORDS
    write("\n\n4. DUPLICATE RECORDS")
    write("-" * 70)

    duplicate_rows = df.duplicated().sum()
    write(f"Duplicate rows: {duplicate_rows}")

    if "Ticket ID" in df.columns:
        duplicate_ticket_ids = df["Ticket ID"].duplicated().sum()
        write(f"Duplicate Ticket IDs: {duplicate_ticket_ids}")

    # UNIQUE VALUES
    write("\n\n5. UNIQUE VALUES")
    write("-" * 70)

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
        if column in df.columns:
            write(f"\n{column}")
            write(
                f"Number of unique values: "
                f"{df[column].nunique(dropna=True)}"
            )

            values = df[column].dropna().unique()
            write("Values:")

            for value in values:
                write(f"  - {value}")

    # NUMERICAL COLUMNS
    write("\n\n6. NUMERICAL COLUMNS")
    write("-" * 70)

    numerical_columns = [
        "Customer Age",
        "Customer Satisfaction Rating"
    ]

    for column in numerical_columns:
        if column in df.columns:
            write(f"\n{column}")
            write(f"Minimum : {df[column].min()}")
            write(f"Maximum : {df[column].max()}")
            write(f"Mean    : {df[column].mean():.2f}")
            write(f"Median  : {df[column].median()}")

    # DATE AND TIME COLUMNS
    write("\n\n7. DATE / TIME COLUMNS")
    write("-" * 70)

    date_columns = [
        "Date of Purchase",
        "First Response Time",
        "Time to Resolution"
    ]

    for column in date_columns:
        if column in df.columns:
            converted_dates = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_dates = converted_dates.dropna()

            write(f"\n{column}")
            write(
                f"Valid date/time values : "
                f"{len(valid_dates)}"
            )
            write(
                f"Invalid/blank values   : "
                f"{len(df) - len(valid_dates)}"
            )

            if len(valid_dates) > 0:
                write(
                    f"Earliest value         : "
                    f"{valid_dates.min()}"
                )
                write(
                    f"Latest value           : "
                    f"{valid_dates.max()}"
                )

    # TICKET STATUS
    write("\n\n8. TICKET STATUS DISTRIBUTION")
    write("-" * 70)

    if "Ticket Status" in df.columns:
        write(
            df["Ticket Status"]
            .value_counts(dropna=False)
            .to_string()
        )

    # TICKET PRIORITY
    write("\n\n9. TICKET PRIORITY DISTRIBUTION")
    write("-" * 70)

    if "Ticket Priority" in df.columns:
        write(
            df["Ticket Priority"]
            .value_counts(dropna=False)
            .to_string()
        )

    # TICKET CHANNEL
    write("\n\n10. TICKET CHANNEL DISTRIBUTION")
    write("-" * 70)

    if "Ticket Channel" in df.columns:
        write(
            df["Ticket Channel"]
            .value_counts(dropna=False)
            .to_string()
        )

    # TICKET TYPE
    write("\n\n11. TICKET TYPE DISTRIBUTION")
    write("-" * 70)

    if "Ticket Type" in df.columns:
        write(
            df["Ticket Type"]
            .value_counts(dropna=False)
            .to_string()
        )

    # PRODUCT DISTRIBUTION
    write("\n\n12. PRODUCT DISTRIBUTION")
    write("-" * 70)

    if "Product Purchased" in df.columns:
        write(
            df["Product Purchased"]
            .value_counts(dropna=False)
            .to_string()
        )

    # CUSTOMER SATISFACTION
    write("\n\n13. CUSTOMER SATISFACTION DISTRIBUTION")
    write("-" * 70)

    if "Customer Satisfaction Rating" in df.columns:
        write(
            df["Customer Satisfaction Rating"]
            .value_counts(dropna=False)
            .sort_index()
            .to_string()
        )

    # DATA QUALITY CHECKS
    write("\n\n14. BASIC DATA QUALITY CHECKS")
    write("-" * 70)

    if "Customer Age" in df.columns:
        invalid_age = (
            df["Customer Age"].notna()
            & (
                (df["Customer Age"] < 0)
                | (df["Customer Age"] > 120)
            )
        ).sum()

        write(f"Invalid customer ages: {invalid_age}")

    if "Customer Satisfaction Rating" in df.columns:
        invalid_rating = (
            df["Customer Satisfaction Rating"].notna()
            & (
                (df["Customer Satisfaction Rating"] < 1)
                | (df["Customer Satisfaction Rating"] > 5)
            )
        ).sum()

        write(
            f"Invalid satisfaction ratings "
            f"(outside 1-5): {invalid_rating}"
        )

    # END OF REPORT
    write("\n" + "=" * 70)
    write("DATASET INSPECTION COMPLETE")
    write("=" * 70)

print("Dataset inspection completed successfully.")
print(f"Report saved to: {report_file}")