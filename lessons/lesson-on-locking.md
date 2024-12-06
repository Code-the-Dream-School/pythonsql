Many concurrent processes may access a database.  This can create various problems,
in that some processes may change data while others are attempting to read or
change the same data.  Consider the following case:

```python
with Session() as session:
    account = session.get(Account, {"account_id": 55})
    stmt = update(Account).where({"account_id": 55}).values(balance=account.balance - 1000.00)
    try:
        account = session.execute(stmt)
    except Exception as e:
        print("Exception on update {e}")
        session.rollback()
    else
        try:
            session.commit()
        except Exception as e:
            print("Exception on commit {e}")
    session.close()
```

The user is able to withdraw 1000.  But what happens if another process has updated the user's
balance after the first process does the read, but before it does the update?
The new value won't be correct.  Sometimes one can just avoid
the read, as follows:

```python
with Session() as session:
    stmt = update(Account).where({"account_id": 55}).values(balance=Account.balance - 1000.00)
    # ...
```

Now there is no race condition with other processes. But we are allowing the user
to go overdrawn.  There is no check to see whether they have enough money.
To prevent this, we need to do the read and perfornm some logic, like:
```python
    account = session.get(Account, {"account_id": 55})
    if account.balance >= 1000.00:
        # here we continue to do the update.  We still use
        # the second form of the update statement to make sure
        # that the new value in the account is correct, in case there
        # is a concurrent process that has changed the value
```

But the user could
still go overdrawn!  Suppose there is a concurrent withdrawal after the read, but
before the update.  The user might not have enough money in the account.

To address this problem, databases have isolation levels.

1. Uncommitted Read.  Read operations return the latest data value from the database,
even if it hasn't been committed.  This isolation level is rarely used, and it does not address the
problem described above.  You can have "dirty reads", reads of values that will never
be persisted.
2. Committed Read.  Read operations return the latest committed value from the database.
This gets rid of the dirty reads, but the balance might still change between the read
and the update, so the user might still go overdrawn.  Also, even within the a single transaction,
one might get different values returned for the same table rows.
3. Repeatable Read.  When the Account record is read from the database, any subsequent
reads that occur in the process of the same transaction will return the same row values.
But that doesn't mean that other processes haven't changed the data.  This doesn't really
help either.  Also, Repeatable Read does not mean that selects will always return the
same result set within a given transaction.  If inserts or deletes have occurred, the result
set could change.  These changes are called "phantom reads".
4. Serializable.  With this level of isolation, any rows that are read are locked for
the period of the transaction.  Also, updates and deletes that would change a select
result set are blocked at the table level.  Other processes still have read access to
the locked data, but they can't change it.  Changes to the database occur exactly as
if each transaction was performed serially, without any concurrency.  This doesn't mean
that there isn't concurrency, but it does mean that damaging effects of concurrency
are prevented.  In this case, one can have neither dirty reads,
nor reads where the value in the database may change during the transaction, nor phantom reads.

In our exercises, we use an isolation level of serializable.

## Alternate Approaches to Locking

Each of these isolation levels adds additional cost, which can slow the database and
therefore the application.  There are alternative approaches.

First, one can explicitly get a lock on a given record, using `FOR UPDATE` in the select
statement that retrieves the record.  This is pessimistic locking.  The lock is put in place
to guarantee no changes after the retrieval, until the transaction completes.

Second, one can have a column in the record with the record version.
The record is read, followed by application
logic to determine how or whether the record should be updated.  Then, in the update statement,
the where clause includes the old version number, so that it
only finds the record if the version number hasn't changed.  Also, the values clause
of the update statement increments the version number.  This is optimistic locking.  There
isn't really a lock, just protection from race conditions.

## Other Problems

There is another concern, which is deadlock.  Suppose there are two processes that read
and make changes, as follows:

```
Process 1:
read record A
read record B
update record A

Process 2:
read record A
read record B
update record B
```
Now suppose that each process completes its reads before either does updates.  Then,
process 1 will wait for write access to record A, but it is locked by process 2.  And,
process 2 will wait for write access to record B, but it is locked by process 1.  This
is a deadlock.  The database will recognize the problem, one of the transactions
will fail, and an error will be returned to that process, which may retry the
transaction.  Big transactions that change or depend on many records can make the
cost of frequent retries a significant factor in the performance of the application.

A final concern is the effect of ill behaved applications.  Suppose one process
acquires a lock on something, and the process either crashes or dithers so that the lock is
held for a long time.  If the process crashes, the database or socket connection
ends, so that the database can release the lock.  But if the process holds the
lock, that problem must be fixed within the application itself.  Other
processes will get errors indicating lock timeouts.  Sometimes, as for bulk changes,
this might be necessary and inherent.