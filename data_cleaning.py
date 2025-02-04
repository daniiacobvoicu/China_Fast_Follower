# Cleaning Script Below
import pandas as pd

# Load Excel file
file_path = "/content/drive/My Drive/China_Analysis/03022025_DealsAdvExportData.xlsx"
xls = pd.ExcelFile(file_path)

# Load both sheets (adjusting the skiprows for correct headers)
deal_attributes_df = pd.read_excel(xls, sheet_name="Deal Attributes", skiprows=14)
drug_details_df = pd.read_excel(xls, sheet_name="Drug Details", skiprows=14)

# Set proper column names from the first row and drop it
deal_attributes_df.columns = deal_attributes_df.iloc[0].astype(str)
deal_attributes_df = deal_attributes_df[1:].reset_index(drop=True)

drug_details_df.columns = drug_details_df.iloc[0].astype(str)
drug_details_df = drug_details_df[1:].reset_index(drop=True)

# Clean column names
def clean_column_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace(r"[^\w\s]", "", regex=True)
    )
    return df

deal_attributes_df = clean_column_names(deal_attributes_df)
drug_details_df = clean_column_names(drug_details_df)

# Drop unnecessary "nan" columns
deal_attributes_df = deal_attributes_df.loc[:, ~deal_attributes_df.columns.str.lower().str.contains("nan")]
drug_details_df = drug_details_df.loc[:, ~drug_details_df.columns.str.lower().str.contains("nan")]

# Merge datasets on GD_Deal_ID if present
if "GD_Deal_ID" in deal_attributes_df.columns and "GD_Deal_ID" in drug_details_df.columns:
    merged_df = pd.merge(deal_attributes_df, drug_details_df, on="GD_Deal_ID", how="left")
else:
    merged_df = deal_attributes_df

# Show dataset info
print("Merged dataset shape:", merged_df.shape)
merged_df.head()

