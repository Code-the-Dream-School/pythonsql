In this lesson, you will learn how to define models for your
database schema.  You will also learn how to update the database
schema from the model.  You will also learn how to augment 
the schema with validators and additional class methods.  These
help to make sure the data is valid.  They also can transform
the data on both input and output.

## Understanding the Existing Schema

Have a look at `models/Employee.py'.  Here, not only the
class of Employee objects is defined, but also the related
table is described.  So, you know which columns exist, what the
datatype is for each, some other properties associated with the
column such as autoincrement and nullable, and which
are primary and foreigh keys.  That's all conveyed into the
database at schema load/update time.  However, there's more.
The database does not know anything about @hybrid_property or
relationships.  Those are only present to let the ORM represent
the object fully.

While we're at it, take a look at `models\Order.py`.  Here we
are setting up several relationships, some of which are one-to-many.
A Customer may have many orders, for example.  And, when an instance
of Customer called customer is loaded into the session, you can use
customer.orders to get the list of Order objects associated with
that customer.  Take a careful look at the Product relationship
for Order.  Here we have a many-to-many relationship, because a
customer may order many different products, and many different
customers may order a given product.  One must have an association
table in the middle to make this work.  In this case, the 
association table is the one from the OrderDetails model.  This
is really a many-to-many-through relationship, because the OrderDetails
model has its own attribute, Quantity.  You may want to keep this
example handy, as the SQLAlchemy doesn't explain it well.  In particular,
note the use of `overlaps=`.

## Goals for the Schema Change

Suppose the use case for this database has evolved. We want:

- To allow employees to have email addresses and passwords.
- To make sure that the
email addresses are syntactically valid and unique within the database,
and that they are stored in lower case.  
- To guarantee that the password is sufficiently complex.  
- To store a hash of the password, not the password itself.
- To be able to validate the password the employee enters at logon time.
- Not to include the password hash on retrieval of the record via the ORM.

Of course, we'll also need to add the corresponding columns to the
database schema.  We can do all of this using the database model.

Let's start with the columns.  We can edit models/Employee.py
to add two new columns.

```python
    email = Column(String, unique=True)
    hashed_password = Column(String)
```
We don't set nullable=False, because that would make all
existing records invalid.

## Email Address

To make sure that the email is syntactically valid and lower case,
we need a validator.  A validator is a method with the `@validator`
prefix.  Here is our validator for the email column:

```python
import re
from sqlalchemy_filters.exceptions import FieldValidationError
... 
    @validates(email)
    def validate_email(self, email)
        email = email.strip().lower()
        email_regex = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?: \[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?" 
        if !bool(re.match(email_regex,email))
            raise FieldValidationError("That email address is not valid.")
        return email
```
This makes sure that the email address is 'valid'.  I put that word in quotes, because
even though the regex looks hairy,
it's not quite complicated enough to be a complete check.  The email
address is stored in lower case without whitespace at the ends.

## Password Validation and Hashing

When creating an Employee object in the session, we want to set the `password` attribute.
We then validate this for our password rules.  If it doesn't pass, we raise an exception.
```python
import bcrypt
...

    @validates(password)
    def hash_password(self, password)
        password_regex = '*[! @#$%^&*])[a-zA-Z0-9! @#$%^&*]{8,16}$'
        # this says we want between 8 and 16 characters with at least one special character.
        # Of course, this wouldn't suffice to guarantee strong passwords.
        if !(bool(password_regex,password))
            raise FieldValidationError("That password is too simple.")
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.hashed_password = hashed_pw.decode('utf-8')
        return password # This line doesn't really do anything.

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    @reconstructor
    def init_on_load(self):
        self.hashed_password = None

```
Let's unpack this.  Before the entry is written to the database, the validators run.
When creating/modifying an Employee object, the calling code sets the password attribute
with a plain text value,
but only if the user has a password.  The password isn't written to the database, because
there is no corresponding column.  The method with the `@property` decorator ensures that
one can't read the plaintext password back out of the Employee object.  At logon time,
the employee provides an email address and a plain text password.  The code then does a select() to
find the corresponding Employee record.  The Employee object, say `employee` returned by this retrieval
does not contain the hashed_password, because the `@reconstructor` decorated method runs after loading
stuff from the database and strips that out.
Of course it does not contain the plain text
password either.  
Now one can call employee.verify_password(plain_text_password).  The hashing is
done again, and the return value tells whether it is the right password.

Well ... that's what we wanted to do.  You could add additional validation logic, 
so that, for example, every new user created has to have an email address and a password --
but you have to check that processing is different for updates than for inserts.
And you could make sure that FirstName and LastName both have values that are neither
null nor blank.

## Adding the Columns to the Table

Database schema management is complicated, because the schema evolves over time.
You want to be sure that schema changes don't break anything, and also that one
developer's schema changes don't conflict with those of a different developer.

The schema management package used in this project is Alembic. One step,
```shell
alembic init alembic
```
was done as the repository was set up, so you don't need to do that.
We also set the database URL in alembic.ini.
Now, we have changed the model.  Alembic can identify what has changed, 
and can autogenerate schema changes.  We then apply as follows:
```shell
alembic revision --autogenerate -m "Add email and hashed_password"
alembic upgrade head
```
The first command generates a migration file, and stores it in alembic/versions.  The
name reflects the message on the revision command above.  Take a look in that 
directory for the previous migration files, and have a look at one to see what it
does.  Alembic can do various other things, such as rolling back a schema change.

## What's Next

This is currently the last lesson in this package.  So, what else is there
to learn about data engineering using SQLAlchemy? Plenty!

- Practice, practice, practice!
- Then, learn Pandas and Numby!  These provide capabilities to manage and
analyze the data.
