In this lesson, you will learn how to define models for your
database schema.  You will also learn how to update the database
schema from the model.  You will also learn how to augment 
the schema with validators and additional class methods.  These
help to make sure the data is valid.  They also can transform
the data on both input and output.

## Understanding the Existing Schema

Have a look at `models/Employee.py`.  Here, not only the
class of Employee objects is defined, but also the related
table is described.  So, you know which columns exist, what the
datatype is for each, some other properties associated with the
column such as autoincrement and nullable, and which
are primary and foreigh keys.  That's all conveyed into the
database at schema load/update time.  However, there's more information in the model.
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
from sqlalchemy.orm import validates, reconstructor
... 
    @validates('email')
    def validate_email(self, key, email)
        email = email.strip().lower()
        email_regex = email_regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9" + \
        "!#$%&'*+/=?^_`{|}~-]+)*|\"(?:" + \
        "[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c" + \
        "\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:" + \
        "[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)" + \
        "{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:" + \
        "(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\" + \
        "[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])" 
        if !bool(re.match(email_regex,email))
            raise ValueError("That email address is not valid.")
        return email
```
This makes sure that the email address is 'valid'.  I put that word in quotes, because
even though the regex looks hairy,
it's not quite complicated enough to be a complete check.  The email
address is stored in lower case without whitespace at the ends.

## Password Validation and Hashing

When creating an Employee object in the session, we want to set the `password` attribute,
which would have the plaintext password.  There is no corresponding column in the model,
because what is to be stored is a hash of that password.  So instead we create a setter.
The setter validates the password for password strength rules before storing the
hashed_passsword, and raises a ValueException if it doesn't comply. If it does comply,
it is hashed and stored in hashed_password.
```python
import bcrypt
...
   @password.setter
   def password(self, password):
      if not password:
         return
      password_regex = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
      # this says we want at least 8 characters, at least 1 upper case, at least
      # one lower case, at least one digit, and at least one special character
      if not bool(re.match(password_regex,password)):
         raise ValueError("That password is too simple.")
      hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      self.hashed_password = hashed_pw.decode('utf-8')

   @property
   def password(self):
      raise AttributeError("Password is write-only.")

      def verify_password(self, password):
      if not self.hashed_password:
         return False
      return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

   @reconstructor
   def init_on_load(self):
      self.hashed_password = None
```
The password strength regex is not really adequate to ensure a strong password of course.

There are a couple more methods to discuss:
- The method with the `@property` decorator ensures that
one can't read the plaintext password back out of the Employee object.  
- At logon time,
the employee provides an email address and a plain text password.  The code then does a select() to
find the corresponding Employee record.  The Employee object, say `employee` returned by this retrieval
does not contain the hashed_password, because the `@reconstructor` decorated method runs after loading
stuff from the database and strips that out.
Of course it does not contain the plain text
password either.
- You can call employee.verify_password(plain_text_password).  The hashing is
done again, and the return value tells whether it is the right password.

You have to handle ValueError exceptions in the code.  If you are instantiating
an employee object as follows:
```python
    employee = Employee(first_name="Paul", last_name="Sanders", email="nonsense")
```
then that line will raise a ValueError, because the email is not syntactically
valid.  Ditto if you create an employee with a weak password. And, if you create
an employee object and then try to do:
```python
    employee.password="password"
```
that will also raise a ValueError.  So such operations must be done in try/except blocks.

So, for example, you could do:
```python
    try:
        employee = Employee(first_name="Paul", last_name="Sanders", 
        email="paul@sample.com", password="P4$sword")
        session.add(employee) # adds the employee object to the session
        session.flush() # writes to the database
        session.commit() # commits the write so that it is lasting
    except Exception as e:
        print(f"An exception occurred while attempting to create an employee record: {e}")
```
Well ... that's what we wanted to do.  You could add additional validation logic, 
so that, for example, every new user created has to have an email address and a password --
but you have to check that processing is different for updates than for inserts.
And you could make sure that FirstName and LastName both have values that are neither
null nor blank.

## Adding the Columns to the Table

Database schema management is complicated, because the schema evolves over time.
You want to be sure that schema changes don't break anything, and also that one
developer's schema changes don't conflict with those of a different developer.

The schema management package used in this project is Alembic. Several steps
were done when the repository was set up. First this command:
```shell
alembic init alembic
```
Then, this entry within the alembic.ini was set:
```
sqlalchemy.url = sqlite:///db/lesson.db
```
Then, this line was added to alembic/env.py, below the comment
about adding your model's metadata:
```python
    from models import target_metadata
```
The value of target_metadata is initialized in models/__init__.py.
All of this was done
was done as the repository was set up, so you don't need to do that
for this project, but you'd have to do it for projects you create.

Now, we have changed the model.  Alembic can identify what has changed, 
and can autogenerate schema changes.  This is done with the following command:
```shell
alembic revision --autogenerate -m "Add email and hashed_password"
```
The migration file is created in alembic/versions, with some random name ending
in "_add_email_and_hashed_password.py".  Well, the autogenerate is pretty good, but
in this case, it's not good enough.  We are creating a unique constraint on the
email field, and we are also using SQLite.  So the migration file has to be modified,
as follows:
```python
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employees', sa.Column('email', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('hashed_password', sa.String(), nullable=True))
    # op.create_unique_constraint(None, 'employees', ['email'])
    # ### end Alembic commands ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        # Add a unique constraint on the 'email' column
        batch_op.create_unique_constraint('uq_employees_email', ['email'])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'employees', type_='unique')
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint('uq_employees_email', type_='unique')
    op.drop_column('employees', 'hashed_password')
    op.drop_column('employees', 'email')
    # ### end Alembic commands ###
```
There are other cases in which you have to tweak the migration files, so
it is a good idea to examine them to understand what they do.  The migration
is applied with this command:
```shell
alembic upgrade head
```
Alembic keeps track of which migrations have already been applied, so it only
applies the new ones.  If the database is deleted, it runs all the migrations.
You can also roll back the last migration, via:
```shell
alembic downgrade -1
```
Or, you can do the `alembic history` command to get the list of migrations that
have been applied, and rollback to a particular one.

## What's Next

This is currently the last lesson in this package.  So, what else is there
to learn about data engineering using SQLAlchemy? Plenty!

- Practice, practice, practice!
- Then, learn how to combine SQLAlchemy with other tools, such as Pandas and Numpy.
