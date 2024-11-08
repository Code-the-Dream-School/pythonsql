### Using SQLAlchemy to Perform SQL Operations from Python

There are a number of reasons to use SQLAlchemy instead of making SQL calls directly to
the database.

- SQLAlchemy will limit exposure to SQL syntax differences between
database implementations
- SQLAlchemy makes it possible to write very compact and understandable code
- There are hordes of data engineers using SQLAlchemy for this purpose
- It is a ready bridge to higher level tools such as Pandas and Numby

On the other hand, there is a significant learning curve for SQLAlchemy.
The documentation is organized in a complicated way, and as SQLAlchemy has
evolved, it has acquired many different ways to do the same things.  You
can study the tutorial and the documentation, and over time, you will
definitely want to do so.  You find it [here.](https://docs.sqlalchemy.org/en/20/)

The purpose of the following lessons is to introduce you to the basics.
We will use the SQLAlchemy ORM (Object Relational Mapper).  With the ORM,
operations are on objects representing the records, rather than records, giving
many of the advantages of OOP.

The database operations you do rely on an engine and a session.  The engine
is configured with the URL for the database itself, and possibly with additional
configuration.  The session is used for a group of related operations, which
may involve any CRUD operations.

Relational operations are grouped in
transactions.  The idea is that one can perform a series of operations with
consistency.  For example, suppose one is doing a withdrawal from a bank
account.  One can retrieve the current balance, and then if there is sufficient
funds, one can change the balance, with a guarantee that the operation does
not complete if the balance has changed in the meantime.  Or, suppose
someone wants to transfer money from one account to another.  They wouldn't
be happy if the withdrawal part succeeded but the deposit part failed
for some reason.  The transaction
boundaries ensure that either both operations succeed or both fail.

The session provides boundaries for the transaction.  When a session
is created, a transaction is automatically begun at the time
of the first database access within the session. If a commit succeeds,
the next database access within the session
starts a new transaction.  If writes have occurred but have
not been comitted, they are rolled back when the session is closed,
but a better approach is to rollback explicitly before closing the session.

In SQLAlchemy, data objects within the session acts as proxies for data in the database,
representing its current state. Once you have completed the group of related operations,
you should close the session, and then you would create a new session for
subsequent work.  The data objects within the session can in some cases be
stale.  For example, they are retrieved, and then there is a rollback that
releases any locks, and then some other process writes to the corresponding
record.  In this case, one can do a `session.refresh()` of the object, which
retrieves it from the database, and which may also lock it, depending on
the isolation level.

Be conscious of the fact that operations, particularly write operations,
may fail.  So, such operations should occur in a try block, with appropriate
exception handling.

Here's a tip.  The SQLAlchemy documentation is basically user hostile.
But, you can ask ChatGPT or perhaps another AI to explain things to you.
This approach is often the fastest way to find out what you need to know
if you are stuck.  **Use it cautiously however.**  Do not let ChatGPT
write the code you want to write.  If you do that, you won't learn how to
write it yourself.  You may end up submitting, either in a class or even on the job,
code you don't understand.  You can't succeed in the software development
profession if you submit code you don't understand.  For one thing, ChatGPT often
makes mistakes or misunderstands what you need to do.  But you could ask, 
for example, "How do I

### Setting up the Session and the Engine, with some Reads

You can check out sqla_example.py.  You will see that it starts
with some imports, as follows:

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Product
from utils.nice_print import print_record, print_records, print_rows # Provided for your convenience
```

Now you need an engine, and something to create sessions:

```python
engine = create_engine('sqlite:///db/lesson.db', echo=True, echo_pool="debug")  
Session = sessionmaker(bind=engine)
```

When setting up the engine, we give the URL for the database, including, if needed, any credentials.
Of course, credentials would be in an environment variable or something like that, not in the code.
In this case, we don't need credentials, as we are using SQLite.  The `echo=True, echo_pool="debug"`
is not necessary, but what it does is cause the actual SQL executed by SQLAlchemy to be echoed to
the terminal, so that we can see what is really going on.

Now we use a session.  We can do that in a with block, which will contain a few related operations.
Then we'll do our first query.

```python
with Session() as session:
    product = session.query(Product).first()
    print_record(product)
```

Ok, that's a start.  We get the first product and print it out.  We make sure to
close the session.  The object we get returned
is an instance of the Product class.  Our print routine can inspect that to figure
out the column names, and in this way, we can print it out.

### Select

Query still works, but it is kind of the old way of doing things.  From now on, for
read operations, we'll use Select.  Select in the SQLAlchemy ORM is more expressive
than Query.  We'll add the following statements.

```python
    stmt = select(Product).limit(3) # This just builds the statement.
    products = session.scalars(stmt).all() # Here the statement is executed and the results obtained
    print_records(products)
```

Now, as you might expect, one can qualify the select statement with where(), limit(), order_by(), and
the like.  But, in all these cases, one just gets an iterable collection of instances of Product objects.
What about just getting a couple of columns? That is done as follows:

```python
    stmt = select(Product.ProductName, Product.Price).limit(5)
    result = session.execute(stmt)
    product_attributes = result.fetchall()
    print_rows(product_attributes)
```

In this case, one gets back an iterable collection of Row objects, not Customer
objects.  These are tuples, but each has a `_mapping` attribute, and that gives
the row as a Python dict object, where the keys are the column names and
the values are the actual row values. Ok, now suppose in our output, we want
the name of the Supplier as well as the name of the product.  As we need information
from two tables, that's a join.

```python
    stmt = select(Product.ProductName, Supplier.SupplierName).join(Product.supplier).limit(5)
    result = session.execute(stmt)
    products_suppliers = result.fetchall()
    print_rows(products_suppliers)
    session.close()
```

There's a bit of magic here.  In the Product model, there is a relationship statement that
connects the product to a single supplier, which is why one can use `Product.supplier`.  One
can do joins where there is no such relationship statement, but then it is typically
necessary to do an `on()` to specify the keys that tie the tables together.  Well, that`s
enough for this session, so we do a `session.close()`.  The close is important, or you
get a lot of lingering crap in your process.

## Relationships and Insert

Let's see what we can learn about the first order.  We'll do this in a new `with` block,
one that eventually will end with a session close:

```python
    stmt = select(Order).limit(1)
    order = session.scalars(stmt).first()
    print_record(order)
    print_record(order.customer)
    print_record(order.shipper)
    print_record(order.employee)
    print_records(order.orderdetails)
    print_records(order.products)
```

Here we are making heavy use of the relationships defined in the model.  We see
that there are one-to-many relationships between each customer and their orders,
each shipper and their orders, each employee and their orders, and each order
and its orderdetails.  All of this is spelled out in the relationship statements
in each of these models.  Finally there is a many-to-many relationship between
orders and products, where the orderdetails table is the association table in the
middle.  This is why the relationship statement for products in the Order class
gives that table as the secondary.

## Write Operations

Ok, now we determine that there is something wrong with the order.  It is missing
one OrderDetail.  We need 26 of product 1.  How do we add this?  Actually, there
are two models for write operations (insert, delete, update) in the SQLAlchemy ORM.
The first method writes to the database, followed by a subsequent commit:

```python
    ...
    stmt=insert(OrderDetail, [{"ProductID": 1, "Quantity": 26, "OrderID": 12}])
    # Note that you pass a list, so you can do bulk inserts
    try: 
        session.execute(stmt)
    except Exception as e:
        session.rollback()
        print("Error on insert {e}")
    else:
        session.commit()
    ...

    stmt = update(OrderDetail, [{"OrderDetailID": 7, "Quantity": OrderDetail.Quantity + 2}])
    # adds 2 to the quantity.  Again, one can do bulk updates.
    ...

    stmt = update(Order).where({"EmployeeID": 14}).values(EmployeeID=23)
    # reassigns all these orders to a different employee
    ...
    
    stmt = delete(OrderDetail).where({"OrderID": 12})
    # delete all the OrderDetail records for this order
```
In each case, when the statement is executed, the corresponding writes are
done to the database, but they are not finalized until the commit.  We are,
in this case, basically bypassing the ORM to do direct Also, when each
statement is executed, an exception may be thrown, for schema violations, foreign
key violations, and perhaps other reasons.  As we'll learn, one can add validation
and pre and post operation functions to a model.  But, when the ORM is bypassed
for write operations, the model is not used and the validations and pre and post
operations declared in the model do not run, which can lead to the creation of
invalid data.

So, we will use the ORM.  This is a little less efficient in the case of updates and deletes
because the existing record must be retrieved to bring it into the session before
it can be changed.

```python
    ...
    od=OrderDetail(ProductID=1,Quantity=5,order=order)
    session.add(od)
    # This creates the object in the session, but does no writes to the
    # database.  A session.flush() first performs validation and other
    # stuff as declared in the model, and then if all that succeeds,
    # it writes it to the database, to be finalized with a commit.
    # If there are changes to the session that have not been flushed
    # at the time of commit, they are first flushed and then committed.
    # Both the flush and the commit may throw execeptions.

    # Suppose the od object is not being created, but was instead
    # retrieved from the database with a select or similar function.
    # Then one can update it as follows:

    od.Quantity += 7

    # or one can delete it as follows

    od.delete()

    # Again, these changes are not written to the database until the
    # session.flush()
```
In sqla_example.py, you will see code to add a new OrderDetail to the
existing order, and then to update it, and then to delete it.

## A Little Cheatsheet

Please review 

