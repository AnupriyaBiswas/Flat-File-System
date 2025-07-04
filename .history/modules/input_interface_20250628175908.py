import pandas as pd

def manual_input_to_df(columns):
    data = []
    print(f"Enter data row-by-row (type 'exit' to stop):")
    while True:
        row = input(f"Enter values for {columns} (comma-separated): ")
        if row.lower() == 'exit':
            break
        values = row.split(',')
        data.append(values)
    return pd.DataFrame(data, columns=columns)
