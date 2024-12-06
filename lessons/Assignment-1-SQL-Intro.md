Before you start the assignment, be sure that you have completed all the setup steps in the README
for the repository.

For each of the assignments in this repository, you use a different git branch.  For
assignment 1, you create a branch called assignment1, using the command:
```shell
git checkout -b assignment1
```
When you do any work in the VSCode terminal, be sure that your virtual environment (.venv)
is active.  You should see it in the terminal prompt.

## SQL Practice with sqlcommand.py

Enter the command:
```shell
python sqlcommand.rb
```
You can then enter SQL commands, such as:
```
SELECT * FROM Products;
```
To exit the program, just type ctrl-c.  The following tables are present:

- customers
- products
- orders
- line_items
- employees

You have to end each SQL command with a semicolon.  Foreign key constraints are enforced.
If you need to restore the database to the starting state, quit the sqlcommand program and follow the instructions in the README to restore the database. Ctrl-C exits the program.

`sqlcommand.py`  does not use SQLAlchemy.
Have a look at the source  if you are curious.  You are using an implementation of SQL called
SQLite, and this program calls SQLite directly.

In your repository, there is a file sql1.txt.  It directs you to compose various SELECT statements.  Compose the SQL statements and try them out against the database using the sqlcommand program.
Once you have them working, paste them in as answers into sql1.txt.

## Submitting Your Work

To submit your work, do the following:
```bash
git add -A
git commit -m "assignment1 commit"
git push origin assignment1
```
Then, on github, within your `pythonsql` repository, create a pull request for your changes.  The pull request should be for the assignment branch, and the target (base) of the pull request should be the main branch of YOUR repository.  **Be careful here!** It is very easy to make the target of the pull request to be the main branch of the Code the Dream Repository, but this is NOT correct.  Click on the base, and choose the main branch of *your* repository, before creating the pull request.  Submit a link to your pull request with your homework submission.  Do NOT merge the pull request until your reviewer has approved it!.

**Please ensure that the target of the pull request is your own github repository!!**  This is NOT the default. The default is the original repository you forked from.  You can't merge your PR into that repository. If you create a PR for that repository, we just close it, and you have to create a new one.  
**This is the number 1 mistake that students make in submitting their work!**

You include a link to your pull request when you make your homework sumbmission.
Your reviewer may request changes.  If that happens, be sure you are on the assignment1 branch (a ```git status``` will tell you, and ```git checkout assignment``` will switch to that branch.)  Make your changes, and then add, commit, and push them as before.  Your changes will be applied to your previous pull request.

This is the procedure you will follow to submit each of the class assignments.