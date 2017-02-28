#Automation for Health Check Query (Queryig Database and compare the result and sending the status as email).

import os
import cx_Oracle
import csv
import win32com.client as win32
from email.mime.text import MIMEText

#Sending Success Mail

def Success_Mail():
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = 'xxxxxxxx@gmail.com;yyyyyyy@gmail.com;zzzzzzz@gmail.com'
	mail.CC = 'xyz@gmail.com'
	mail.Subject = 'ADHOC Invoice Health Check Query Status'
	mail.body = """Hi All,"""+ '\n' '\n' + """Today, there is NO incorrect mapping in the Adhoc Invoices.""" + '\n' '\n' '\n' + """Regards,""" + '\n' + """Maheshkrishna A G""" + '\n' '\n' + """***The above mail is auto generated as part of COR4043 Automation!***"""
	mail.send();
	outlook.Quit();
	
#Sending Failure Mail

def Failure_Mail():
	fp=open('C:\\Users\\XXXXXXXX\\Desktop\\Health_Check\\Health_Check_Issue.txt','r');
	records=fp.read();
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = 'xxxxxxxx@gmail.com;yyyyyyy@gmail.com;zzzzzzz@gmail.com'
	mail.CC = 'xyz@gmail.com'
	mail.Subject = 'ADHOC Invoice Health Check Query Status - Incorrect Mapping'
	mail.body = """Hi All,""" + '\n' '\n' + """Today there are ADHOC invoice incorrect mapping. Please find the details below. """ '\n' '\n' + str(records) + '\n' '\n' '\n' + """Regards,""" + '\n' + """Maheshkrishna A G""" + '\n' '\n' + """***The above mail is auto generated as part of COR4043 Automation!***"""
	mail.send();
	fp.close();
	outlook.Quit();
	
#Deleting the content of the issue file everytime	
	
def deleteContent(fName):
    with open(fName, "w"):
        pass
	
	
#Creating Query_Output file

def query_database():
	filename='C:\\Users\\XXXXXXXX\\Desktop\\Health_Check\\Health_Check_Query.csv';
	FILE=open(filename,"w");
	output=csv.writer(FILE, dialect='unix')

	#Connecting to Database
	IP='your ip address';
	PORT=<port number>;
	SID='<server name>';
	DSN_TNS=cx_Oracle.makedsn(IP,PORT,SID);
	DB=cx_Oracle.connect('<u-name>','<password>',DSN_TNS);
	cursor=DB.cursor();
	query="select * from (<your complete query to be queried in the database>)";
	cursor.execute(query);
	for row in cursor:
		output.writerow(row);
	cursor.close()
	DB.close()
	FILE.close()
	print("Query_Output File Created Successfully");

#Actual Program Starts

query_database();

input_file='C:\\Users\\XXXXXXXX\\Desktop\\Health_Check\\Health_Check_Query.csv';
issue_file='C:\\Users\\XXXXXXXX\\Desktop\\Health_Check\\Health_Check_Issue.txt';

deleteContent(issue_file);

with open(input_file,'r') as fp:
	root=csv.reader(fp);
#Output Query validation (Private functional part. Please omit.)		
	for row in root:
		if row[4]=="AA" or row[4]=="VR" or row[4]=="SA" or (row[2]=='NTS' and row[3]=='LDZ'):
			NEW_FILE=open(issue_file,"a");
			issue_output=NEW_FILE.write(','.join(row)+'\n');
fp.close();

if (os.stat("C:\\Users\\XXXXXXXX\\Desktop\\Health_Check\\Health_Check_Issue.txt").st_size==0):
	Success_Mail();
else:
	Failure_Mail();
	
print("Mail sent Successfully!");
