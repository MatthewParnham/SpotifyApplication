#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
first_name = form.getvalue('username1')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Python Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s</h2>" % (first_name)
print "<h2>This is a python program</h2>"
print "</body>"
print "</html>"
