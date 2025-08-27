import pandas as pd
import re

# Regex pattern to detect phone-like strings
phone_pattern = re.compile(
    r'(\(?\+?\d{1,3}\)?[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{2,6})'
)

def extract_numbers(text):
    """Find all phone-like numbers in a text field."""
    if pd.isna(text):
        return []
    return phone_pattern.findall(str(text))

def process_row(row):
    numbers = []

    # Collect numbers from PHONE column
    numbers.extend(extract_numbers(row['PHONE']))

    # Collect numbers from Email column (sometimes contains numbers)
    numbers.extend(extract_numbers(row['Email']))

    # Deduplicate and keep order
    numbers = list(dict.fromkeys(numbers))

    # Assign cleaned numbers back
    row['PHONE'] = numbers[0] if numbers else ''
    row['PHONE2'] = numbers[1] if len(numbers) > 1 else ''

    # If email was a phone number, clear it
    if extract_numbers(row['Email']):
        row['Email'] = ''

    return row

def clean_csv(input_file, output_file):
    df = pd.read_csv(input_file, dtype=str)

    if 'PHONE2' not in df.columns:
        df['PHONE2'] = ''

    df = df.apply(process_row, axis=1)

    df.to_csv(output_file, index=False)
    print(f"Cleaned CSV written to {output_file}")

if __name__ == "__main__":
    clean_csv("FBO.csv", "FBO_clean.csv")
