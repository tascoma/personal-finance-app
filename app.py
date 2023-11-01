import logging.config
import pandas as pd
import sqlite3
import os
import statement_processor
import database_operations

# Load logging configuration from logging.ini file
logging.config.fileConfig('logging.ini')

# Get logger object for the application
logger = logging.getLogger(__name__)

pd.set_option('display.max_rows', None)

# User will be able to upload files to the application
credit_card_jan = r"C:\Users\Tony\OneDrive\Desktop\Test\01_creditcard_jan.csv"
credit_card_feb = r"C:\Users\Tony\OneDrive\Desktop\Test\02_creditcard_feb.csv"

bank_jan = r"C:\Users\Tony\OneDrive\Desktop\Test\01_bank_jan.csv"
bank_feb = r"C:\Users\Tony\OneDrive\Desktop\Test\02_bank_feb.csv"

paystub_jan1 = r"C:\Users\Tony\OneDrive\Desktop\Test\paystub_2023-01-05.pdf"
paystub_jan2 = r"C:\Users\Tony\OneDrive\Desktop\Test\paystub_2023-01-19.pdf"
paystub_feb1 = r"C:\Users\Tony\OneDrive\Desktop\Test\paystub_2023-02-02.pdf"
paystub_feb2 = r"C:\Users\Tony\OneDrive\Desktop\Test\paystub_2023-02-16.pdf"


def main():
    try:
        connection = sqlite3.connect(os.path.join("data","personal-finance.db"))

        # Application will loop through all files and process them
        logger.info("Processing files...")
        files = [credit_card_jan, credit_card_feb, bank_jan, bank_feb, paystub_jan1, paystub_jan2, paystub_feb1, paystub_feb2]
        df = statement_processor.parsing_statements(files, connection)

        # Application will preview data for user to review
        logger.info("Previewing data...")
        logger.debug(df)

        # Application will ask user to confirm data is correct before posting to database
        logger.info("Posting data to database...")
        respone = input("Is the data correct? (y/n): ")
        if respone == "y":
            statement_processor.posting_to_gl(df, connection, "general_ledger")
        else:
            pass

        # Application will  remove duplicate data
        logger.info("Removing duplicate data...")
        num_of_dups, num_of_dups_drop = database_operations.remove_duplicates(connection, "general_ledger")
        logger.debug(f"Number of duplicate rows before removal: {num_of_dups}")
        logger.debug(f"Number of duplicate rows after removal: {num_of_dups_drop}")

        # Application will identify missing data
        logger.info("Identifying missing data...")
        missing_data = database_operations.identify_missing_data(connection, "general_ledger")
        logger.debug(missing_data)

        # Application will allow user to create data in database
        logger.info("Creating data in database...")
        num = input("Enter number of rows to create: ")
        table = "general_ledger"
        database_operations.create_row(connection, table, int(num))

        # Application will allow user to read data in database
        logger.info("Reading data in database...")
        new_row_df = database_operations.read_general_ledger(connection, transaction_id="test-2023-10-30-1")
        logger.debug(new_row_df)

        # Application will allow user to update data in database
        logger.info("Updating data in database...")
        table = "general_ledger"
        database_operations.update_row(connection, table_name=table, transaction_id="test-2023-10-30-1", column_name="amount", new_value=1000)
        new_row_df = database_operations.read_general_ledger(connection, transaction_id="test-2023-10-30-1")
        logger.debug(new_row_df)

        # Application will allow user to delete data in database
        logger.info("Deleting data in database...")
        table = "general_ledger"
        deleted_row_df = database_operations.delete_row(connection, table, "test-2023-10-30-1")
        logger.debug(deleted_row_df)

        # Application will create P/L statement
        # Application will create balance sheet
        # Application will create visualizations of the data

        connection.close()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    
if __name__ == "__main__":
    main()