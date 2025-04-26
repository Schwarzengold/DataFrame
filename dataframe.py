import pandas as pd
from colorama import init, Fore, Style

init(autoreset=True)

def print_title(text):
    border = "-" * len(text)
    print(Style.BRIGHT + Fore.CYAN + f"\n{text}\n{border}")

def print_table(df):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    cols = list(df.columns)
    widths = [max(len(str(x)) for x in df[col].tolist() + [col]) for col in cols]
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    header = "|" + "|".join(
        f" {Style.BRIGHT + Fore.WHITE + col.ljust(w)} "
        for col, w in zip(cols, widths)
    ) + "|"
    print(Fore.CYAN + border)
    print(header)
    print(Fore.CYAN + border)
    for _, row in df.iterrows():
        line = "|" + "|".join(
            f" {Fore.YELLOW + str(row[col]).ljust(w)} "
            for col, w in zip(cols, widths)
        ) + "|"
        print(line)
    print(Fore.CYAN + border)

df = pd.read_csv('orders100.csv')
print_table(df.head(100))
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

print_title("1. Datatime modify")
print_table(df.head(100))

print_title("2. Added TotalAmount")
df['TotalAmount'] = df['Quantity'] * df['Price']
print_table(df.head(100))

total_revenue = df['TotalAmount'].sum()
average_total = df['TotalAmount'].mean()
orders_per_customer = df.groupby('Customer').size().reset_index(name='OrderCount')

print_title("3.a Total Store Revenue")
print(Fore.GREEN + f"{total_revenue:.2f}")

print_title("3.b Average TotalAmount")
print(Fore.GREEN + f"{average_total:.2f}")

print_title("3.c Orders per Customer")
print_table(orders_per_customer)

orders_over_500 = df[df['TotalAmount'] > 500]
print_title("4. Orders > 500")
print_table(orders_over_500)

sorted_desc = df.sort_values(by='OrderDate', ascending=False)
print_title("5. Sorted by Date Desc")
print_table(sorted_desc.head(10))

date_filtered = df[
    (df['OrderDate'] >= '2023-06-05') &
    (df['OrderDate'] <= '2023-06-10')
]
print_title("6. Orders 2023-06-05 to 2023-06-10")
print_table(date_filtered)

grouped_category = df.groupby('Category').agg(
    Count=('Product','count'),
    TotalSales=('TotalAmount','sum')
).reset_index()
print_title("7. Sales by Category")
print_table(grouped_category)

top3 = df.groupby('Customer')['TotalAmount'].sum() \
         .sort_values(ascending=False) \
         .head(3) \
         .reset_index(name='Sum')
print_title("8. Top 3 Customers")
print_table(top3)
