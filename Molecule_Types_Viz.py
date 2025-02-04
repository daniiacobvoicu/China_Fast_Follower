
# Import the function from Molecule_Types.py
from Molecule_Types import analyze_molecule_types

# Define the file path (update this to match your dataset location in Google Drive)
file_path = "/content/drive/My Drive/China_Analysis/Cleaned_M_A_Dataset.csv"

# Run the function to get molecule type percentages
molecule_type_percentages, molecule_type_by_year = analyze_molecule_types(file_path)

import ipywidgets as widgets
from IPython.display import display

# Get available years from the dataset
available_years = sorted(molecule_type_by_year.index.get_level_values(0).unique().astype(int))

# Create a dropdown widget for selecting a year
year_selector = widgets.Dropdown(
    options=available_years,
    description="Select Year:",
    style={'description_width': 'initial'}
)

# Function to display molecule type data for the selected year
def display_molecule_data(selected_year):
    if selected_year in available_years:
        filtered_data = molecule_type_by_year.loc[selected_year]
        display(filtered_data.to_frame().rename(columns={"Molecule_Types": "Percentage"}))
    else:
        print("No data available for the selected year.")

# Extract available molecule types for selection
available_molecule_types = sorted(molecule_type_by_year.index.get_level_values(1).unique())

# Create a dropdown widget for selecting a molecule type
molecule_selector = widgets.Dropdown(
    options=available_molecule_types,
    description="Select Molecule Type:",
    style={'description_width': 'initial'}
)

# Function to plot molecule type trends over the years
def plot_molecule_trend(selected_molecule):
    # Filter the dataset for the selected molecule type
    molecule_trend = molecule_type_by_year.xs(selected_molecule, level=1, drop_level=False)
    
    if not molecule_trend.empty:
        # Reset index to get Year as a separate column
        molecule_trend = molecule_trend.reset_index()

        # Ensure 'Year' column is properly converted to int
        molecule_trend["Year"] = molecule_trend["Year"].astype(int)
        
        # Get the correct column name for percentages
        percentage_column = molecule_trend.columns[-1]  # This will be the last column (which stores the percentages)
        
        plt.figure(figsize=(10, 5))
        plt.bar(molecule_trend["Year"], molecule_trend[percentage_column], color='skyblue')
        
        plt.xlabel("Year")
        plt.ylabel("Percentage of All Deals (%)")
        plt.title(f"Trend of {selected_molecule} Over the Years")
        plt.xticks(molecule_trend["Year"], rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.show()
    else:
        print(f"No data available for {selected_molecule}")

# Create an interactive widget
interactive_plot = widgets.interactive(plot_molecule_trend, selected_molecule=molecule_selector)

# Create an interactive widget
interactive_widget = widgets.interactive(display_molecule_data, selected_year=year_selector)

# Display the widget
display(interactive_widget, interactive_plot)

