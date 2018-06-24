# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 18:28:29 2018

@author: Nagasudhir

Create a readonly user to an oracle db using sql shell
https://dba.stackexchange.com/questions/147957/creating-a-read-only-user-in-oracle

first login as sysdba
SQL> connect hr/password as sysdba
SQL> create user user_read_only identified by password;
SQL> grant create session to user_read_only;
SQL> grant select any table to user_read_only;

# create user with all privileges - https://stackoverflow.com/questions/22386976/create-a-user-with-all-privileges-in-oracle
create user REPORTING_WEB_UI_UAT identified by 123;
grant create session to REPORTING_WEB_UI_UAT;
grant all privileges to REPORTING_WEB_UI_UAT;

# drop a user with all the associated schemas
DROP USER sidney CASCADE;

# grant particular privileges to particular user - https://chartio.com/resources/tutorials/how-to-create-a-user-and-grant-permissions-in-oracle/
GRANT
  SELECT,
  INSERT,
  UPDATE,
  DELETE
ON
  schema.books
TO
  books_admin;

# revoke all privileges from user - https://stackoverflow.com/questions/30313462/how-to-revoke-all-privileges-for-a-user-in-sqlplus
revoke all privileges from user_name

# grant permissions to only tables of a particular owner to a user - https://stackoverflow.com/questions/187886/grant-select-on-all-tables-owned-by-specific-user
BEGIN
   FOR R IN (SELECT owner, table_name FROM all_tables WHERE owner='TheOwner') LOOP
      EXECUTE IMMEDIATE 'grant select on '||R.owner||'.'||R.table_name||' to TheUser';
   END LOOP;
END; 

# Now select data from schema. Remember to address the main schema by hr.table_name
SQL> select * from hr.employees

Use drop user command to just remove a user
SQL> drop user user_read_only

using python cx_Oracle post - http://www.oracle.com/technetwork/articles/dsl/python-091105.html
"""

import cx_Oracle
import sys

# Connect as user "hr" with password "welcome" to the "oraclepdb" service running on this computer.
connection = cx_Oracle.connect("hr", "123", "localhost/xe")

cursor = connection.cursor()

try:
    cursor.execute("""
        SELECT first_name, last_name
        FROM hr.employees
        WHERE department_id = :did AND employee_id > :eid""",
        did = 50,
        eid = 190)
    
    rows = []
    for fname, lname in cursor:
        rows.append([fname, lname])
        print("Values:", fname, lname)
except:
    print("Unexpected error:", sys.exc_info()[0])
finally:
    print("closing connections...")
    cursor.close()
    connection.close()