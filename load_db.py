import pandas as pd
import sqlalchemy as sa

# Create a database engine
engine = sa.create_engine('sqlite:///db/lesson.db')

tables = ["Customers", "Categories", "Employees", "Shippers", "Suppliers", 
          "Products", "Orders", "OrderDetails"]

for table in tables:
    t_name = table.lower()
    csv_file = "./csv/" + table + ".csv"
    data = pd.read_csv(csv_file, sep='\t')
    data.to_sql(t_name, engine, if_exists='replace', index=False)
