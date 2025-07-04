from modules.excel_handler import read_excel
from modules.metadata_handler import read_json_metadata
from modules.sql_dump_parser import parse_sql_dump
from modules.input_interface import manual_input_to_df

def main():
    print("=== FLAT FILE SYSTEM DEMO ===\n")

    # Excel demo
    df = read_excel('data/users.xlsx')
    print("Excel Data:\n", df.head())

    # Metadata demo
    meta = read_json_metadata('data/music_metadata.json')
    print("\nMusic Metadata Sample:\n", meta)

    # SQL dump demo
    inserts = parse_sql_dump('data/sales_dump.sql')
    print("\nParsed SQL Inserts:\n", inserts[:3])  # show only first 3

    # Manual input
    df_input = manual_input_to_df(['Name', 'Age', 'Email'])
    print("\nUser-entered DataFrame:\n", df_input)

if __name__ == '__main__':
    main()
