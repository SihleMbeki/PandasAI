import pandas as pd
import numpy as np
import warnings

def _validate_name(df, source):
    """Trim whitespace, ensure string type, and warn on missing or duplicated names."""
    if 'Name' not in df.columns:
        warnings.warn(f"{source} is missing a 'Name' column.")
        return df
    missing = df['Name'].isna()
    if missing.any():
        warnings.warn(f"{source} has {missing.sum()} missing 'Name' value(s).")
    df['Name'] = df['Name'].astype(str).str.strip()
    duplicated = df['Name'].duplicated()
    if duplicated.any():
        warnings.warn(
            f"{source} has duplicated 'Name' entries: {df.loc[duplicated, 'Name'].tolist()}"
        )
    return df

def _categorize(age):
    if pd.isna(age):
        return 'Unknown'
    if age <= 12:
        return 'Child'
    if 13 <= age <= 26:
        return 'Youth'
    if 27 <= age <= 40:
        return 'Adult'
    return 'Senior'

def main():
    users_df = pd.read_excel('Users.xlsx', sheet_name=0)
    employment_df = pd.read_excel('Employment.xlsx', sheet_name=0)

    users_df = _validate_name(users_df, 'Users.xlsx')
    employment_df = _validate_name(employment_df, 'Employment.xlsx')

    merged_df = pd.merge(users_df, employment_df, on='Name', how='left')
    merged_df['Person is'] = merged_df['Age'].apply(_categorize)

    merged_df.to_excel('Merged.xlsx', sheet_name='Merged', index=False)

    print(merged_df.head())
    print(merged_df['Person is'].value_counts())

if __name__ == '__main__':
    main()
