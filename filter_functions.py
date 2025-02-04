
import pandas as pd
import pycountry_convert as pc

def filter_by_deal_subtype(df, subtype):
    """Filters deals by Deal Subtype Level 3"""
    return df[df["Deal_Subtype_Level_3"].str.contains(subtype, na=False, case=False)]

def get_asset_distribution(df, category, year=None):
    """Counts percentage of assets in a given category (Indications, Molecule Types, Development Stage)"""
    if year:
        df = df[df["Announced_Date"].str.contains(str(year), na=False)]
    return df[category].value_counts(normalize=True) * 100  # Convert to percentages

def count_issuers(df):
    """Counts the number of times an Issuer appears in the dataset."""
    return df["IssuerLicensorTargetVendorGranteeService_Provider"].value_counts()

def get_continent(country_name):
    """Maps a country to its continent using pycountry_convert."""
    try:
        country_code = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continents = {"NA": "North America", "SA": "South America", "EU": "Europe", "AF": "Africa", "AS": "Asia", "OC": "Oceania"}
        return continents.get(continent_code, "Unknown")
    except:
        return "Unknown"

def count_acquirers(df):
    """Counts the number of times an Acquirer appears in the dataset and maps to continent."""
    acquirer_counts = df["AcquirersInvestorsSurviving_EntityLicenseePartnersGrantorClient"].value_counts().reset_index()
    acquirer_counts.columns = ["Acquirer", "Count"]
    acquirer_counts["Continent"] = acquirer_counts["Acquirer"].map(lambda x: get_continent(df.loc[df["AcquirersInvestorsSurviving_EntityLicenseePartnersGrantorClient"] == x, "Company_Geography"].values[0] if not df.loc[df["AcquirersInvestorsSurviving_EntityLicenseePartnersGrantorClient"] == x, "Company_Geography"].empty else "Unknown"))
    return acquirer_counts
