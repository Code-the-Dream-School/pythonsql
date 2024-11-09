# Cheat Sheet for the SQL Alchemy ORM

## Writes

Inserts are done with session.add() and, for inserting a collection of entries,
session.add_all().  For example, an Employee record would be created as follows:
```python
from models import Employee
employee = Employee({Employee.FirstName: 'Hima', Employe.LastName: ...})
```
This step just adds the object to the session, but it is then written to
the database with session.flush() and committed with session.commit().  If
you don't do a flush() before the commit(), the flush() is done automatically
by the commit.  The flush() can throw an exception in case of ORM validation
failures or database schema violations.  The commit() may also throw exceptions
that should be handled.

For updates and deletes, one first gets the object into the session, and then
one modifies or deletes it.  Again, the writes to the database don't actually
occur until session.flush().  So, for update, one could do:
```python
from models import Employee
employee = session.get(Employee,{'EmployeeID': 273})
employee.LastName = 'Fujimoto' # this updates the object within the session
```
Or, to update a group of entries, one might do:
```python
from models import Product
stmt = select(Product).where(Product.price < 2.00)
products = session.scalars(stmt).all()
for product in products:
    product.Price += 0.50
```
For delete, having retrieved the Product object product, one does:
```python
product.delete() # takes effect with session.flush()
```
## Be Careful to Finish the Transaction!

You can write to the database using the ORM with a session.flush().
You can also bypass the ORM with insert(), update(), or delete(). If
you do session.flush() or any of these latter operations, 
it is important to do either session.commit() or
session.rollback() before closing the session (and of course, you always
need to call session.close() for every session).  If changes exist in session
objects that haven't been committed or rolled back at session.close(),
the session.close() triggers a rollback automatically, but this is
bad style.  You should do the session.rollback() explicitly.  If
you have done writes that bypass the ORM it is all the more important
to do the session.rollback(), as it does not occur automatically.

## Be Careful of Stale References!

If you get an object in the session, other processes may write to the
corresponding database record, so the object as stored in the session may
be stale.  One can lock the record explicitly by including a with_for_update()
if the database isolation level is
Serializable 
(as it is in our exercises) for the period of the transaction. (We'll have
an aside on SQL database isolation levels.)
Session.rollback() and session.commit()
release all such locks, so then the object in the session could be stale.
If you have such an object, say `product`, one can do `session.refresh(product)`
to get the latest version.  If the isolation level is Serializable, the
refresh locks the record, but if not, one can use with_for_update() on the
refresh.  Another approach for refreshing the object or objects
is to repeat the select() or get() that retrieves it/them.

## Get() and Two Forms of Select()

You can retrieve a single object from the database by primary key using
```python
session.get(Product,5)
```

You can create a select() statement that gets a list of model objects,
or one that gets a list of `row` objects.  This sequence:

```python
from models import Product
stmt = select(Product).where(...)...
products = session.scalars(stmt).all()
```
gets an iterable collection of Product objects.  This sequence:
```
stmt = select(Order.OrderID, OrderDetails.ProductID) \
.select_from(Order).join(OrderDetails).where(...)...
results = session.execute(stmt).fetchall()
```
returns a list of rows, and for each, the row._mapping gives
a `dict` with the keys and values for that row.

As always, in this series of lessons, there are other ways
to accomplish the same ends.  This form of select() is used if
you want to do a join, if you want a subset of attributes, or
if you want to select particular columns, you specify a list of attributes as follows:
```python
stmt = select(Employee.FirstName, Employee.LastName).select_from(Employee)
```
And, further, one can also set the column name, if something different from the
default is needed, using label() as follows:
```python
stmt = select(Employee.FirstName.label('first'), Employee.LastName.label('last')).select_from(Employee)
```

## Joins

The select_from() can have a join(), which by default, is an inner join.  If you do:
```python
from models import OrderDetail, Product
... select().select_from(OrderDetail).join(Product, isouter=True) ...
```
You get a left join.  You can't do a right join directly, but
you can do 
```python
... select().select_from(Product).join(OrderDetail, isouter=True) ...
```
to accomplish the same end.  You can also do a full join using `full=True`.

You notice that there is no ON in these joins.  We are relying on the
relationships defined in the models.  But, if the relationship is not
present, or if there are other reasons to customize the ON clause, one
can specify it in the join statement:
```python
...select_from(OrderDetail).join(Product, OrderDetail.ProductID == Product.ProductID)...
```

## Filtering Conditions in Where Clauses

You can use the standard collection of SQL operators:

```python
...where(OrderDetail.Quantity > 7) ...
...where(Employee.EmployeeName.like('a%'))...
```
The comparison operators include `== != < > <= >=`  The methods include, `like`, `in`, and `between`.
One can test for null values with `.is_(None)` or `.isnot(None)`  One can add logic
with `and_`, `or_` and `not_`, and one can specify conditions also with boolean operators:
```python
...where(and_((Product.Price > 5.00),(Product.SupplierID == 27)))...
...where((p.Price > 5.00) & (Product.SupplierID == 27))
```
And you can also specify one or several HAVING conditions, as in this example:
```python
from sqlalchemy import func
stmt = select(Employee.FirstName, Employee.LastName, func.count() \ 
.label("OrderCount")).select_from(Employee).join(Order) \
.group_by(Employee.EmployeeID).having(func.count() > 10)
```

Note the use of func.  This provides access to various aggregation functions, such as
count(), min(), max(), avg(), sum(), and distinct().

## Organizing the Result Set

After the where clause, you can specify additional handling of the result set with limit(), offset(),
order_by(), and group_by().  For order_by(), if you want descending order, you would do
```python
... .order_by(Product.Price.desc())
```

## Subqueries

You need to experiment with subqueries to get the syntax right.  Suppose you want to
find the average price of an order.  The subquery would find the price of each order, and 
having that, func.avg() can be used to figure out the average.

First, get the right select statement working.  In this case, we have:
```python
stmt = select(func.sum(OrderDetail.Quantity * Product.Price).label('OrderTotal')) \
.select_from(OrderDetail) \
.join(Product) \
.group_by(OrderDetail.OrderID)
print_rows(session.execute(stmt).fetchall()) # just to check
```
Having verified this statement, one can make it into a subquery:
```python
subq = ( select(func.sum(OrderDetail.Quantity * Product.Price).label('OrderTotal')) \
.select_from(OrderDetail) \
.join(Product) \
.group_by(OrderDetail.OrderID)).subquery()
```
Now one can use the subquery in combination with a select(). For some reason,
the column names are prefixed, in this case with `subq.c.`, so that one has, as
in this case, `subq.c.OrderTotal`.  The prefix is always the name of the subquery
object plus `.c.`  You can pass the result to select_from() and get
the final result:
```python
stmt = select(func.avg(subq.c.OrderTotal).label('Average Order Price')).select_from(subq)
rows = session.execute(stmt)
print_rows(rows)
```
The results of a subquery can be passed to select_from(), any_(), all_(), or exists().

If you need any the following, you import func, any_, all_, and_, or_, not_
or exists from sqlalchemy.