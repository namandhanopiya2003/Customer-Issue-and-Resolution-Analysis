from pathlib import Path
import pandas as pd
import re

# FILE PATHS
cleaning_folder = Path(__file__).parent
project_folder = cleaning_folder.parent
raw_file = project_folder / "2. Sample_Dataset" / "customer_tickets.csv"
generated_folder = cleaning_folder / "Generated_Files"
generated_folder.mkdir(exist_ok=True)
cleaned_file = generated_folder / "customer_tickets_cleaned.csv"

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

print("Raw dataset loaded successfully.")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# STANDARDIZE COLUMN NAMES
column_mapping = {
    "Ticket ID": "ticket_id",
    "Customer Name": "customer_name",
    "Customer Email": "customer_email",
    "Customer Age": "customer_age",
    "Customer Gender": "customer_gender",
    "Product Purchased": "product_purchased",
    "Date of Purchase": "date_of_purchase",
    "Ticket Type": "ticket_type",
    "Ticket Subject": "ticket_subject",
    "Ticket Description": "ticket_description",
    "Ticket Status": "ticket_status",
    "Resolution": "resolution",
    "Ticket Priority": "ticket_priority",
    "Ticket Channel": "ticket_channel",
    "First Response Time": "first_response_time",
    "Time to Resolution": "time_to_resolution",
    "Customer Satisfaction Rating": "customer_satisfaction_rating"
}

df.rename(columns=column_mapping, inplace=True)

# REMOVE EXACT DUPLICATE ROWS
initial_rows = len(df)
df.drop_duplicates(inplace=True)
removed_duplicates = initial_rows - len(df)

print(f"Duplicate rows removed: {removed_duplicates}")

# STANDARDIZE TEXT FIELDS
text_columns = [
    "customer_name",
    "customer_email",
    "customer_gender",
    "product_purchased",
    "ticket_type",
    "ticket_subject",
    "ticket_description",
    "ticket_status",
    "resolution",
    "ticket_priority",
    "ticket_channel"
]

for column in text_columns:
    if column not in df.columns:
        continue

    df[column] = df[column].apply(
        lambda x: str(x).strip() if pd.notna(x) else x
    )

# STANDARDIZE CATEGORICAL VALUES
if "customer_gender" in df.columns:
    df["customer_gender"] = (
        df["customer_gender"]
        .str.strip()
        .str.title()
    )

if "product_purchased" in df.columns:
    df["product_purchased"] = (
        df["product_purchased"]
        .str.strip()
    )

if "ticket_type" in df.columns:
    df["ticket_type"] = (
        df["ticket_type"]
        .str.strip()
        .str.title()
    )

if "ticket_subject" in df.columns:
    df["ticket_subject"] = (
        df["ticket_subject"]
        .str.strip()
        .str.title()
    )

if "ticket_status" in df.columns:
    df["ticket_status"] = (
        df["ticket_status"]
        .str.strip()
        .str.title()
    )

if "ticket_priority" in df.columns:
    df["ticket_priority"] = (
        df["ticket_priority"]
        .str.strip()
        .str.title()
    )

if "ticket_channel" in df.columns:
    df["ticket_channel"] = (
        df["ticket_channel"]
        .str.strip()
        .str.title()
    )

# CLEAN TEXT FIELDS
def clean_text(text):
    """
    Clean obvious formatting noise while preserving
    the original meaning of the text.
    """
    if pd.isna(text):
        return text

    text = str(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text

if "ticket_description" in df.columns:
    df["ticket_description"] = (
        df["ticket_description"]
        .apply(clean_text)
    )

if "resolution" in df.columns:
    df["resolution"] = (
        df["resolution"]
        .apply(clean_text)
    )

# STANDARDIZE EMAIL VALUES
if "customer_email" in df.columns:
    df["customer_email"] = (
        df["customer_email"]
        .str.strip()
        .str.lower()
    )

# CONVERT NUMERICAL COLUMNS
if "ticket_id" in df.columns:
    df["ticket_id"] = pd.to_numeric(
        df["ticket_id"],
        errors="coerce"
    ).astype("Int64")

if "customer_age" in df.columns:
    df["customer_age"] = pd.to_numeric(
        df["customer_age"],
        errors="coerce"
    )

if "customer_satisfaction_rating" in df.columns:
    df["customer_satisfaction_rating"] = pd.to_numeric(
        df["customer_satisfaction_rating"],
        errors="coerce"
    )

# VALIDATE CUSTOMER AGE
if "customer_age" in df.columns:
    invalid_age = (
        (df["customer_age"] < 18) |
        (df["customer_age"] > 100)
    )

    invalid_age_count = invalid_age.sum()

    if invalid_age_count > 0:
        print(
            f"Invalid customer ages found: "
            f"{invalid_age_count}"
        )

        df.loc[invalid_age, "customer_age"] = pd.NA

# VALIDATE SATISFACTION RATING
if "customer_satisfaction_rating" in df.columns:
    invalid_rating = (
        df["customer_satisfaction_rating"].notna() &
        ~df["customer_satisfaction_rating"].between(1, 5)
    )

    invalid_rating_count = invalid_rating.sum()

    if invalid_rating_count > 0:
        print(
            f"Invalid satisfaction ratings found: "
            f"{invalid_rating_count}"
        )

        df.loc[
            invalid_rating,
            "customer_satisfaction_rating"
        ] = pd.NA

# CONVERT DATE OF PURCHASE
if "date_of_purchase" in df.columns:
    df["date_of_purchase"] = pd.to_datetime(
        df["date_of_purchase"],
        errors="coerce"
    )

# CONVERT RESPONSE AND RESOLUTION TIMESTAMPS
if "first_response_time" in df.columns:
    df["first_response_time"] = pd.to_datetime(
        df["first_response_time"],
        errors="coerce"
    )

if "time_to_resolution" in df.columns:
    df["time_to_resolution"] = pd.to_datetime(
        df["time_to_resolution"],
        errors="coerce"
    )

# PRESERVE EXPECTED MISSING VALUES
# Resolution, Time to Resolution, and Satisfaction Rating
# are missing for Open and Pending tickets.
# First Response Time is missing for Open tickets.
# These values are not automatically treated as errors.
# No values are filled with 0, mean, median, or arbitrary text.

# ADD BASIC ANALYTICAL FLAGS
if "ticket_status" in df.columns:
    df["is_closed"] = (
        df["ticket_status"] == "Closed"
    )

if "customer_satisfaction_rating" in df.columns:
    df["satisfaction_available"] = (
        df["customer_satisfaction_rating"].notna()
    )

if "resolution" in df.columns:
    df["resolution_available"] = (
        df["resolution"].notna()
    )

# REORDER COLUMNS
preferred_order = [
    "ticket_id",
    "customer_name",
    "customer_email",
    "customer_age",
    "customer_gender",
    "product_purchased",
    "date_of_purchase",
    "ticket_type",
    "ticket_subject",
    "ticket_description",
    "ticket_status",
    "resolution",
    "ticket_priority",
    "ticket_channel",
    "first_response_time",
    "time_to_resolution",
    "customer_satisfaction_rating",
    "is_closed",
    "satisfaction_available",
    "resolution_available"
]

existing_columns = [
    column for column in preferred_order
    if column in df.columns
]

remaining_columns = [
    column for column in df.columns
    if column not in existing_columns
]

df = df[existing_columns + remaining_columns]

# FINAL VALIDATION
print("\nRunning final validation...")
print(f"Final rows    : {df.shape[0]}")
print(f"Final columns : {df.shape[1]}")
print(
    f"Duplicate rows remaining: "
    f"{df.duplicated().sum()}"
)

if "ticket_id" in df.columns:
    print(
        f"Duplicate Ticket IDs remaining: "
        f"{df['ticket_id'].duplicated().sum()}"
    )

if "customer_age" in df.columns:
    print(
        f"Customer Age missing values: "
        f"{df['customer_age'].isna().sum()}"
    )

if "customer_satisfaction_rating" in df.columns:
    print(
        f"Satisfaction missing values: "
        f"{df['customer_satisfaction_rating'].isna().sum()}"
    )

# SAVE CLEANED DATASET
df.to_csv(
    cleaned_file,
    index=False
)

print("\nCleaning completed successfully.")
print("Cleaned dataset saved at:")
print(cleaned_file)