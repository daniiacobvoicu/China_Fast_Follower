
import pandas as pd

# Load the cleaned dataset
file_path = "/content/drive/My Drive/China_Analysis/Cleaned_M_A_Dataset.csv"
df = pd.read_csv(file_path)

# Drop the unnamed index column if present
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# Convert Announced_Date_x to datetime
df["Announced_Date_x"] = pd.to_datetime(df["Announced_Date_x"], errors="coerce")

# Extract year
df["Year"] = df["Announced_Date_x"].dt.year

# Get counts and percentages of Molecule Types overall
molecule_type_counts = df["Molecule_Types"].value_counts(dropna=False)
molecule_type_percentages = (molecule_type_counts / len(df)) * 100

# Compute molecule type percentages per year
molecule_type_by_year = df.groupby("Year")["Molecule_Types"].value_counts(normalize=True) * 100

# Display results
print("Overall Molecule Type Percentages:")
print(molecule_type_percentages)

print("\nMolecule Type Percentages by Year:")
print(molecule_type_by_year)
