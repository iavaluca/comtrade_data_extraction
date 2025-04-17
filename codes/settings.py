import comtradeapicall
from pathlib import Path
from dotenv import load_dotenv
import os


def load_environment_variables():
    """
    Load environment variables from the .env file.
    Raises a ValueError if the COMTRADE_API_KEY is missing.
    """
    # Use pathlib to construct the path
    dotenv_path = Path(__file__).resolve().parent.parent / ".env.txt"
    print(f"DEBUG: Attempting to load .env file from: {dotenv_path}")  # Debug statement

    if not dotenv_path.exists():
        raise FileNotFoundError(f".env file not found at: {dotenv_path}")

    load_dotenv(dotenv_path=dotenv_path)

    api_key = os.getenv("COMTRADE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key is missing. Please set the COMTRADE_API_KEY environment variable in the .env file."
        )

    return api_key


# Load environment variables
api_key = load_environment_variables()
print("Environment variables loaded successfully.")

# Define set of countries of interest
df_countries = comtradeapicall.getReference("partner")[["PartnerCode", "PartnerDesc"]]
countries = df_countries.set_index("PartnerDesc")["PartnerCode"].to_dict()

# Define configuration as a dictionary
config = {
    # API key (must be provided via environment variable)
    "api_key": api_key,  # Fetch API key from environment variable
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
    # Choose whether to write stata files or not (True/False)
    "stata_files": True,
}
