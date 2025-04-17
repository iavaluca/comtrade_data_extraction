import logging
import os
from codes.classes.makingLog import makingLog
from codes.classes.dataAPI import dataAPI
from codes.settings import config


def main():
    """
    Main workflow for data extraction and processing.
    """
    # Setup logging
    makingLog.setup()
    logger = logging.getLogger(__name__)
    logger.info("Starting data extraction process...")

    try:
        # Initialize dataAPI instance
        api_key = config.get("api_key")  # Fetch API key from settings
        if not api_key:
            raise ValueError(
                "API key is missing. Please set the COMTRADE_API_KEY environment variable."
            )
        api_instance = dataAPI(key=api_key, config=config)

        # Fetch data with detailed logging
        logging.info("Fetching data from the API...")
        data = api_instance.fetch_data()
        logging.info("Data fetching completed successfully.")

    except Exception as e:
        # Log any errors that occur during data fetching
        logging.error(f"An error occurred during data fetching: {e}", exc_info=True)
    finally:
        # Close the logging system
        logging.shutdown()
        logger.info("Data extraction process completed.")


if __name__ == "__main__":
    main()
