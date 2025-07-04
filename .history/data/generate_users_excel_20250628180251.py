# generate_users_excel.py (temporary script to create file)
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 22],
    "Email": ["alice@example.com", "bob@example.com", "charlie@example.com"]
})
df.to_excel("data/users.xlsx", index=False)
