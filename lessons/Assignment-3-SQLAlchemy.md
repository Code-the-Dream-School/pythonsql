## Practicing SQLAlchemy from the Python3 Interpreter

You can do SQLAlchemy operations from within the interpreter.
This can lead to a lot of typing however, because you have to
do a lot of imports.  To make this easy, there is a 'console'
package in this repository.  You can do all the imports you
need using `from console import *`.  That gives you access
to the following: 
```python
__all__ = ['select', 'func', 'Product', 'Supplier', 'Order', 'OrderDetail', 'Shipper',
            'Customer', 'Employee', 'Category', 'print_record',
            'print_records', 'print_rows', 'Session', 'any_', 'all_', 
            'exists', 'and_', 'or_', 'not_']
```
`Session` is a sessionmaker, which is created for when you import the console
package.  So, after you do this import, you are ready to do SQLAlchemy database
operations on the SQLite db/lesson.db database.  For example, you could do the
following:
```python
session = Session()
stmt = select(Product).limit(5)
result = session.scalars(stmt).all()
print_records(result)
session.close()
```
Try this.  Then, referring to the cheatsheet as needed, experiment
with other more complicated select() statements, with get() statements,
with writes via session.add(), session.flush(), etc.  Each time, you
can use the print convenience routines to verify that the operation
does what you think it does.  For writes, you want to make your
changes, flush and commit them, and then select the same records
to see if they are actually there.  Spend, hmm, maybe an hour
on this, to get confident, and more time if you like.

## Assignment-3.py

Create this program.  You should import what you need.  Then
create an engine and a sessionmaker.  Then add code for the
following:
1. Create a session.
2. Read the first 5 lines of the Employee table and print them.
You are retrieving Employee objects, so you use print_records()
to print them.
3. Read all the OrderDetail records for product 2, and print
them out.
4. Close the session.
5. Create another session.
6. Read the first 5 records of OrderDetails joined with Products.
Retrieve rows with the OrderDetailID and the product name.
Print them out.
7. Close the session.
8. Create another session.
9. Create a new Order.  You do not need to specify OrderID, as
the database will assign it for you.  You do need to specify
a valid CustomerID, EmployeeID, and ShipperID.  You can find
valid values by displaying db/lesson.db in VSCode.  Use the
ORM for all write operations in this lesson. 
10. Create two OrderDetail instances for the Order you created.
11. Commit these changes to the database.  Be sure to add logic
to catch any exceptions.
12. Close the session.
13. Create a new session.
14. Create a new Order, but do not include a ShipperID.  As
a result, it will not be schema compliant.  (You can see
the constraints in models/Order.py.  ShipperID has nullable=False.)
15. Try to commit the change.  This will throw an exception.
Catch the exception, and print out a message with that exception.
16. Roll back the transaction.
17. Close the session.

Your work should be in a lesson3 branch.  Do the usual add, commit,
and push, and then open the pull request, so that you can put a link
in your homework submission.