SQL is a powerful language for accessing data.  The data in an SQL database is organized in tables, like a spreadsheet, where each row has a number of columns, each with a column name.

All back end developers should learn SQL, as it is a skill expected and required by employers.  No-SQL databases, such as MongoDB, also exist, and they are valuable for many kinds of applications, but they do not support the rich relationships between tables that is supported in SQL.

Within Python, we use SQL indirectly.  The actual code we write uses the SQLAlchemy Python package,
which includes an object relational mapper (ORM).  But, that package is just making SQL calls under
the covers.

Read the Odin Project introduction to SQL [here.](https://www.theodinproject.com/lessons/databases-databases-and-sql)  Then do SQLBolt Lessons 1-9 [here.](https://sqlbolt.com/)

Another useful reference is the W3Schools tutorial [here.](https://www.w3schools.com/sql/default.asp)  However, the SQL TryIt editor provided with the tutorial does not work correctly, because of recent browser changes.

### Here are some additional points:

Once you have completed the tutorial, read through the following section.  You will need to understand this additional content in order to complete the assignment.  The assignment includes a database with a number of tables, including a table for customers, one for orders, one for products, and one for line_items.  

The SQLBolt tutorial does not talk about *ambiguous column names*, but sometimes you will have them
when doing joins.  Suppose you want to join a customers table with an orders table, and both contain
a column called customer_id.  The join statement you want is:
```
SELECT customers.customer_id, customer_name, order_id FROM customers JOIN orders ON customers.customer_id = orders.customer_id;
```
Because you have customer_id in both tables, you have to qualify any reference to customer_id with the table name.  You can do this more succinctly by using an alias, specified with AS, as follows:
```
SELECT c.customer_id, customer_name, order_id FROM customers AS c JOIN orders AS o ON c.customer_id = o.customer_id;
```
And, you can even leave out the AS:
```
SELECT c.customer_id, customer_name, order_id FROM customers c JOIN orders o ON c.customer_id = o.customer_id;
```
### Compound Joins

Sometimes you want to join more than one table.  You do that by having multiple JOINs in a single SQL statement.  For example, suppose for each order, you want to get the line items, which are the 
list of products and quantities, plus the product name.  You need to access the orders, line_items, and products tables, as follows:
```
SELECT o.order_id, quantity, product_name FROM orders o JOIN line_items l_i ON o.order_id = l_i.order_id JOIN
products p ON l_i.product_id = p.product_id;
```

### One to Many Associations

The database included with the repository has various tables with relationships.
In this database, an example of a one to many association is the association between
customers and orders.  A customer will have many orders.  The way this works is that each entry in the orders table has a foreign key, customer_id, that is also the primary key for the customer that made that order.  In the database we will use, both have the name CustomerID.  (This sometimes not the case -- the column names may be different.)  You can find out how many orders each customer has with the following query:

```
SELECT customer_name, COUNT(order_id) AS order_count FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id;
```

### Many to Many Associations

There may be many orders for a given product, and there may be many products for a given order.  To make this work, we have a table in the middle, called a join table.  The join table, in this case the line_items table, has two foreign keys, one being the order_id, one being the product_id.  Let's walk this through.

For each order, there are a records in the line_items table that say which product was ordered, and how many of that product were ordered.  You'll have a few different products in the order, so you need a few different records in the line_items table.  But the line_items table does not have the information describing the product, such as the product name.  Information about the product is in the products table.  You could put all of the product information into the line_items table -- but then you would have to repeat it for each other order that includes that product.  That would be inefficient.  So, to get the product name and other information into a full description of the order, you have to join the orders table with both the line_items table and the product table.

In this case, the line_items table is the join table.  We can then see, for example, the products and quantity for each order:
```sql
SELECT o.order_id, product_name, quantity FROM orders o JOIN line_items od ON o.order_id = od.order_id JOIN products p ON od.product_id = p.product_id ORDER BY o.order_id;
```

## Included with the Lesson Repository

It may be helpful, before you start the assignment, to understand some of what is
provided in the project repository.  Via the instructions in the README, you created
and populated a database.  The database has a schema.  The schema is described in the
files in the models directory.  Have a look at `models/Employee.py`.  This describes,
in Python syntax, the various columns and the datatypes for each.  You also see
a relationship, which is not a column, but instead a way of describing to SQLAlchemy
the associations between tables.  In this case an Employee may have many orders.
You see also a Fullname function, with a `@hybrid_property` decorator.  This
allows you, when you use SQLAlchemy, to get the Fullname for an employee, even though
there is no such column in the database.  You see the primary key, which is
autoincremented, meaning that if a new record is created, the primary key is
automatically assigned.  Have a look at `models/Order.py`.  This is similar, but
now you have foreign keys specified.  This is how you get a one to many association
between employees and orders.

The actual data is loaded from csv files in the csv directory.  You can have
a look at that if you like ... but it is easier to look directly at the database.
There is a plugin for VSCode to do this.  You add the SQLite extension to VSCode.
Then you can open `db/lesson.db`, which is the actual database, to see what it
contains.  That's probably enough about the repository contents for now.