The lesson materials describe how the email and hashed_password columns can be added
to the database schema.  So, do this.  Yes, this is kind of c/p. This would all be in
a lesson5 branch.

Once that has been done, try it out.  Write a program to test that the model changes
do what we think they do.  By creating Employee records and then retrieving them,
you can check this out.  Create assignment-5-test.py.  That program should include
tests that the code complies with eachof the points in the spec.  The spec is included
in the lesson.  So, you would check, for example, that you can't create an Employee
record with a syntactically invalid email address.  Also, once the password is set,
you would test that you can validate a plaintext password for the entry.  And so
on for each of the points in the spec.

Be sure that you follow the usual pattern of writing through the ORM, not
directly to the table.  Check the cheatsheet if you are uncertain about the
difference.

Next, add two new models, Pet and Owner.  Owner would have an OwnerName column
(String), and an autoincremented Integer non-null primary key.  Pet would have
a similar primary key, but it would also have a foreign key for Owner.  So
an Owner can have many pets.  The Pet model would also have a PetName column
(String), a PetType column (String), and an Age column (Integer).  Configure
the relationship between these two tables.  Also, add validations:

- The OwnerName can't be blank or null.
- Neither can the PetName
- The Age can't be negative or greater than 100.
- The PetType must be one of "dog", "cat", "bird", and "fish".

Once this is done, use alembic to do the creation of the new tables.

Write assignment5-pets.py.  Within it,
create several Owner records, and for each of these, several Pet records.
Make sure this works, and that, for an Owner object in the
session, one can get to owner.pets and pet.owner.  Then verify that
each of the validations works.

