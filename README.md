# Learning SQL for Use in Python

This repository contains Code the Dream lessons for students who
want to develop skill in SQL, and in particular, skill in using the
SQLAlchemy package and the SQLAlchemy ORM (Object Relational Mapper).
Students should have a basic understanding of Python in order to complete
the included exercises.

## Setup: Please Read this part carefully!

Several steps are required to make this repository work.  Be sure to
follow the instructions below.

1. You should have a current version of Python installed before doing any
configuration of this repository.  You also need a current version of Pip and Venv.
Venv, if you haven't used it, sets up a virtual Python environment for the installation
of the packages required for the included programs.  If you haven't installed Python and Pip and Venv, please do so before you do anything else.  There are instructions on the Internet,
depending on your OS platform.
2. When you do the exercises, you will add code to this repository, which you will
then push to github.  You should first fork this repository, then clone your fork, and then
change to the directory created by the clone.
3. Next, set up your virtual environment.  This is done with the commands
    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. Now, from that directory, start VSCode with `code .`  The next step is important.  You need
to set the default python instance to be used by VSCode, and you want the one for your
virtual environment.  Open the command palette (Ctrl-Shift-P)
and enter Python:Select Interpreter. Choose the one that includes `.venv`.
5. Start a terminal session.  You should see `(.venv)` in the command line prompt.  Always
check for this before doing any work on the project.
6. Get the project required packages.  These include SQLAlchemy, Alembic, and Pandas.  Alembic
is used for database schema management.  You won't use Pandas, but it is used by the
provided program that loads the database.  To get these packages into your virtual
environment, enter
    ```shell
    pip install -r requirements.txt
    ```
7. Create the database schema.  Migration files are provided in the repository, and you run them
with this command:
    ```shell
    alembic upgrade head
    ```
8. Populate the database, with this command:
    ```shell
    python3 load_db.py
    ```

If all these steps complete correctly, your environment is ready.  If, as you do the assignments,
the database becomes corrupted, you delete `./db/lesson.db` and repeat steps 7 and 8 to recreate it.

This is all just setup.  Before you actually write code, you will learn about relational
databases and SQL using online exercises.

## Lesson materials and assignments

[Lesson 1:SQL Intro](./lessons/Lesson-1-SQL-Intro.md)

[Assignment 1: SQL Intro](./lessons/Assignment-1-SQL-Intro.md)

[Lesson 2: More SQL](./lessons/Lesson-2-More-SQL.md)

[Assignment 2: More SQL](./lessons/Assignment-2-More-SQL.md)

[Lesson 3: SQLAlchemy Intro](./lessons/Lesson-3-SQLAlchemy-Intro.md)

[Assignment 3: SQLAlchemy Intro](./lessons/Assignment-3-SQLAlchemy-Intro.md)

[Lesson 4: More SQLAlchemy](./lessons/Lesson-4-More-SQLAlchemy.md)

[Assignment 4: More SQLAlchemy](./lessons/Assignment-4-More-SQLAlchemy.md)

[Lesson 5: Schema Management with Alembic](./lessons/Lesson-5-Alembic.md)

[Assignment 5: Schema Management with Alembic](./lessons/Assignment-5-Alembic.md)

## Lesson 1 Learning Objectives

- Understand what relational databases are
- Learn what SQL is
- Understand why this is important to the back-end developer
- Know the CRUD operations
- Learn the SQL used in query operations: SELECT, constraints, ordering
- Understand primary and foreign keys
- Learn the SQL needed for joins

## Lesson 2 Learning Objectives

- Learn to do SELECT queries that aggregate data: sums, averages, etc.
- Learn how the SELECT query is processed: order of operations
- SQL for adding, modifying, and deleting entries
- SQL for managing database schema: creating and modifying tables

## Lesson 3 Learning Objectives

- Understand what an ORM is
- Understand the use of the SQLAlchemy ORM
- Do some basic CRUD operations using the ORM
- Understand about sessions within the ORM
- Understand about transactions and transaction boundaries
- Practice the use of session.commit() and session.rollback()
- Understand the difference between data objects within the session,
data written to the database, and data committed in the database
- Understand relationships within the models

## Lesson 4 Learning Objectives

- Practice the concepts of Lesson 3
- Use more complicated operations, such as subquery, having, etc.

## Lesson 5 Learning Objectives

- Understand how to change a model
- Use validations
- Use Alembic to manage the database schema
- Write a test program that verifies compliance with the spec
- Add new models with relationships and validation
- Write another test program for the new models
