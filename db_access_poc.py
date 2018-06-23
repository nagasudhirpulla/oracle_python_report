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

Now select data from schema. Remember to address the main schema by hr.table_name
SQL> select * from hr.employees

Use drop user command to remove a user
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