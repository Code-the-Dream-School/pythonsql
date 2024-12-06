import pandas as pd
import sqlalchemy as sa

# Create a database engine
engine = sa.create_engine('sqlite:///db/lesson.db')

tables = ["customers", "employees", 
          "products", "orders", "line_items"]

for table in tables:
    t_name = table.lower()
    csv_file = "./csv/" + table + ".csv"
    data = pd.read_csv(csv_file, sep=',')
    data.to_sql(t_name, engine, if_exists='append', index=False)
