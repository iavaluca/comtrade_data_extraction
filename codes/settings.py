import comtradeapicall

# Define set of countries of interest
df_countries = comtradeapicall.getReference("partner")[["PartnerCode", "PartnerDesc"]]
countries = df_countries.set_index("PartnerDesc")["PartnerCode"].to_dict()

# Define configuration as a dictionary
config = {
    # API key (must be provided by the user)
    # "api_key": "",  # Replace with your actual API key
    # Choose between 'bulk' or 'batch'
    "method": "bulk",
    # Choose between 'A' (Annual) and 'M' (Monthly)
    "frequency": "M",
    # 'X' for exports, 'M' for imports
    "flows": "X",
    # Dynamically fetch countries
    "countries": countries,
    # TODO: change param
    "partners": countries,
    # Generate years dynamically
    "years": list(range(2013, 2025 + 1)),
    # Generate months dynamically
    "months": list(range(1, 12 + 1)),
    # Choose between 2 and 4 (6 to be implemented)
    "hscode": 2,
}
