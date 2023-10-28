import pandas as pd
import data_processor
import sqlite3
import os

def main():
    # pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df1 = pd.read_csv(r"C:\Users\tasco\OneDrive\Desktop\Test\01_creditcard_jan.csv")
    df2 = pd.read_csv(r"C:\Users\tasco\OneDrive\Desktop\Test\02_creditcard_feb.csv")

    df3 = pd.read_csv(r"C:\Users\tasco\OneDrive\Desktop\Test\01_bank_jan.csv")
    df4 = pd.read_csv(r"C:\Users\tasco\OneDrive\Desktop\Test\02_bank_feb.csv")

    pdf1 = r"C:\Users\tasco\OneDrive\Desktop\Test\paystub_2023-01-05.pdf"
    pdf2 = r"C:\Users\tasco\OneDrive\Desktop\Test\paystub_2023-01-19.pdf"
    connection = sqlite3.connect(os.path.join("data","personal-finance.db"))

    credit_card_df = pd.concat([df1, df2]).reset_index(drop=True)
    credit_card_df = data_processor.process_creditcard_statements(credit_card_df, connection)

    bank_df = pd.concat([df3, df4]).reset_index(drop=True)
    bank_df = data_processor.process_bank_statements(bank_df)

    pdf_df1 = data_processor.process_paystub(pdf1, connection)
    pdf_df2 = data_processor.process_paystub(pdf2, connection)
    paystub_df = pd.concat([pdf_df1, pdf_df2]).reset_index(drop=True)


    print(credit_card_df)
    print(bank_df)
    print(paystub_df)

if __name__ == "__main__":
    main()