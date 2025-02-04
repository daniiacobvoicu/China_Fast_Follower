
import pandas as pd

def analyze_molecule_types(file_path):
    """
    Loads the dataset, filters out blank Molecule_Types, and calculates the overall and per-year percentages.
    
    :param file_path: str, path to the dataset file
    :return: tuple of (overall_percentages, per_year_percentages)
    """
    # Load dataset
    file_path = "/content/drive/My Drive/China_Analysis/Cleaned_M_A_Dataset.csv"
    df = pd.read_csv(file_path)

    # Drop the unnamed index column if present
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")

    # Convert Announced_Date_x to datetime
    df["Announced_Date_x"] = pd.to_datetime(df["Announced_Date_x"], errors="coerce")

    # Extract year
    df["Year"] = df["Announced_Date_x"].dt.year

    # Drop rows where Molecule_Types is missing
    df_filtered = df.dropna(subset=["Molecule_Types"])

    # Compute overall molecule type percentages
    molecule_type_counts = df_filtered["Molecule_Types"].value_counts()
    total_count = len(df_filtered)
    molecule_type_percentages = (molecule_type_counts / total_count) * 100

    # Compute molecule type percentages per year
    molecule_type_by_year = df_filtered.groupby("Year")["Molecule_Types"].value_counts(normalize=True) * 100

    return molecule_type_percentages, molecule_type_by_year


