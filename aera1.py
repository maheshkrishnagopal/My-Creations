'''
Simple Python implementation to connect to the AD with the help of LDAP3 and
then querying for "objectclass=person", which will give the person objects from
AD.
'''

import sys
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES
from ldap3 import ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError
import json
import shutil
import mysql.connector as mariadb


server_name = '172.30.37.12'
domain_name = 'aeratech.local'
user_name = 'jegan'
password = 'mASTER#123'

mariadb_connection = mariadb.connect(user='root', password='mASTER#123', database='aera_tech_auto')
cursor = mariadb_connection.cursor()

format_string = '{:25} {:>6} {:19} {:19} {}'
# print("User\t\t", "Group\t\t", "Expires\t\t", "Description\t\t")

server = Server(server_name, get_info=ALL)
conn = Connection(server, user='{}\\{}'.format(domain_name, user_name), password=password,
                  authentication=NTLM, auto_bind=True)
conn.search('dc=aeratech,dc=local'.format(domain_name), '(objectclass=person)',
            attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
from_ad = list()
for e in conn.entries:
    try:
        desc = e.description
    except LDAPCursorError:
        desc = ""
    try:
        group = e.memberOf
    except LDAPCursorError:
        group = "No-Group"
    if str(group)[0] == '[':
        group = str(group)
    else:
        group = str(group)
    print(str(e.name), group, str(e.accountExpires)[:10], desc)

    if 'CN=Msys' in group or 'Msys' in group:
        from_ad.append([str(e.name), 'Msys', str(e.accountExpires)[:10], str(desc)])
    if 'CN=PROD' in group or 'PROD' in group:
	from_ad.append([str(e.name), 'PROD', str(e.accountExpires)[:10], str(desc)])
    if 'CN=DEV' in group or 'DEV' in group:
	from_ad.append([str(e.name), 'DEV', str(e.accountExpires)[:10], str(desc)])
print('---------------------TEMP--------------------------')
for i in from_ad:
    print(i)


def grant_access(user):

    # Code to modify and initiate the Ansible files.

    pass


def revoke_access(row):

   # Code to modify and initiate the Ansible files to revoke access.
    pass

def create_db_record(record):

    grant_access(record)
    cursor.execute("INSERT INTO users VALUES (%s,%s,%s,%s)",(record[0],record[1],record[2],record[3]))
    mariadb_connection.commit()
    print("Record created")


def delete_db_record(row):

    revoke_access(row)
    cursor.execute("DELETE FROM users WHERE NAME=%s and GROUPs=%s",(row[0],row[1]))
    mariadb_connection.commit()

def compare_db(from_ad):
    # cursor.execute("DELETE FROM users")
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print('from database --------------------')
    for i in result:
        print(i)
    print('--------------------------------------')

    # Compare AD to DB for insertion
    if len(result) != 0:
	for rec in from_ad:
	    write_flag = 'Yes'
	    for row in result:
	    	if rec[0] == row[0] and rec[1] == row[1]:
	            write_flag = 'No'
	    if write_flag == 'Yes':
	        create_db_record(rec)

    # Compare DB to AD for deletion
    if len(result) != 0:
        for row in result:
	    delete_flag = 'Yes'
	    for rec in from_ad:
	        if row[0] == rec[0] and row[1] == rec[1]:
		    delete_flag = 'No'
	    if delete_flag == 'Yes':
		print(row)
	        delete_db_record(row)
		

compare_db(from_ad)

