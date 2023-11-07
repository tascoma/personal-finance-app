import logging.config
import pandas as pd
import sqlite3
import os
import statement_processor
import database_operations
import accounting_cycle

# Load logging configuration from logging.ini file
logging.config.fileConfig('logging.ini')

# Get logger object for the application
logger = logging.getLogger(__name__)

pd.set_option('display.max_rows', None)

# User will be able to upload files to the application
credit_card_jan = r"C:\Users\tasco\OneDrive\Desktop\Test\01_creditcard_jan.csv"
credit_card_feb = r"C:\Users\tasco\OneDrive\Desktop\Test\02_creditcard_feb.csv"

bank_jan = r"C:\Users\tasco\OneDrive\Desktop\Test\01_bank_jan.csv"
bank_feb = r"C:\Users\tasco\OneDrive\Desktop\Test\02_bank_feb.csv"

paystub_jan1 = r"C:\Users\tasco\OneDrive\Desktop\Test\paystub_2023-01-05.pdf"
paystub_jan2 = r"C:\Users\tasco\OneDrive\Desktop\Test\paystub_2023-01-19.pdf"
paystub_feb1 = r"C:\Users\tasco\OneDrive\Desktop\Test\paystub_2023-02-02.pdf"
paystub_feb2 = r"C:\Users\tasco\OneDrive\Desktop\Test\paystub_2023-02-16.pdf"


def main():
    try:
        connection = sqlite3.connect(os.path.join("data","personal-finance.db"))

        # Application will loop through all files and process them
        logger.info("Processing files...")
        # file_jan = [credit_card_jan, bank_jan, paystub_jan1, paystub_jan2]
        # df = statement_processor.parsing_statements(file_jan, connection)

        files_feb = [credit_card_feb, bank_feb, paystub_feb1, paystub_feb2]
        df = statement_processor.parsing_statements(files_feb, connection)
        
        # Application will preview data for user to review
        logger.info("Previewing data...")
        print(df)

        # Application will ask user to confirm data is correct before posting to database
        logger.info("Posting data to database...")
        respone = input("Is the data correct? (y/n): ")
        if respone == "y":
            statement_processor.posting_to_database(df, connection, "general_ledger", if_exists='append')
        else:
            pass

        # Application will remove duplicate data
        logger.info("Removing duplicate data...")
        num_of_dups, num_of_dups_drop = database_operations.remove_duplicates(connection, "general_ledger")
        logger.debug(f"Number of duplicate rows before removal: {num_of_dups}")
        logger.debug(f"Number of duplicate rows after removal: {num_of_dups_drop}")

        # Application will identify missing data
        logger.info("Identifying missing data...")
        missing_data = database_operations.identify_missing_data(connection, "general_ledger")
        print(missing_data)

        # Application will allow user to create data in database
        # logger.info("Creating data in database...")
        # num = input("Enter number of rows to create: ")
        # table = "general_ledger"
        # database_operations.create_row(connection, table, int(num))

        # Application will allow user to read data in database
        # logger.info("Reading data in database...")
        # new_row_df = database_operations.read_general_ledger(connection, transaction_id="test-2023-10-30-1")
        # logger.debug(new_row_df)

        # Application will allow user to update data in database
        # logger.info("Updating data in database...")
        # table = "general_ledger"
        # transaction_id = 'bank-2023-01-03-1'
        # database_operations.update_row(connection, table_name=table, transaction_id=transaction_id, column_name="account_code", new_value=600502)
        # database_operations.update_row(connection, table_name=table, transaction_id=transaction_id, column_name="account", new_value="Food - Restaurants")
        # updated_df = database_operations.read_general_ledger(connection, transaction_id=transaction_id)
        # print(updated_df)

        # Application will allow user to delete data in database
        # logger.info("Deleting data in database...")
        # table = "general_ledger"
        # deleted_row_df = database_operations.delete_row(connection, table, "test-2023-11-01-1")
        # logger.debug(deleted_row_df)

        # Application will create an undajusted trial balance
        logger.info("Creating unadjusted trial balance...")
        unadjusted_trial_balance_df = accounting_cycle.create_unadjusted_trial_balance_df(connection, "February")
        print(unadjusted_trial_balance_df)
        accounting_cycle.check_debits_credits_equal(unadjusted_trial_balance_df)

        # Application will create closing entries
        logger.info("Creating closing entries...")
        closing_entries_df = accounting_cycle.create_closing_entries(unadjusted_trial_balance_df, '2023-02-28')
        print(closing_entries_df)
        respone = input("Is the data correct? (y/n): ")
        if respone == "y":
            statement_processor.posting_to_database(closing_entries_df, connection, "general_ledger", if_exists='append')
        else:
            pass

        # Application will create an adjusted trial balance
        logger.info("Creating adjusted trial balance...")
        adjusted_trial_balance_df = accounting_cycle.create_adjusted_trial_balance_df(connection, "February")
        print(adjusted_trial_balance_df)
        accounting_cycle.check_debits_credits_equal(adjusted_trial_balance_df)

        # Application will update the account_balance_history table
        logger.info("Updating account_balance_history table...")
        account_balance_history_df = accounting_cycle.create_account_balance_history_table(unadjusted_trial_balance_df, adjusted_trial_balance_df)
        print(account_balance_history_df)
        respone = input("Is the data correct? (y/n): ")
        if respone == "y":
            statement_processor.posting_to_database(account_balance_history_df, connection, "account_balance_history", if_exists='append')
        else:
            pass

        # Application will update the chart_of_accounts table
        logger.info("Updating chart_of_accounts table...")
        chart_of_accounts_df = accounting_cycle.update_chart_of_accounts_table(connection, adjusted_trial_balance_df)
        print(chart_of_accounts_df)
        respone = input("Is the data correct? (y/n): ")
        if respone == "y":
            statement_processor.posting_to_database(chart_of_accounts_df, connection, "chart_of_accounts", if_exists='replace')
        else:
            pass

        connection.close()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    
if __name__ == "__main__":
    main()