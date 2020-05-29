# DNS-Resolver

This program is an implementation of a DNS resolver.  The resolver takes a domain name as an input.  The resolver will resolves this query by first contacting the root server, the top-level domain, all the way down until the authoritative name server.  In the mydig_output.txt, some dns resolution outputs can be found on sample domain names that were run using the program.  The attached pdf file consist of a graph that compares this program's output speed to Google's dns resolver and a local dns resolver.

# API used
The program is written in Python3 and it imports the following external libraries: dns.message, dns.name, dns.query, time, datetime, and sys.

The dns.message, dns.name, and dns.query libraries are all from the dnspython library.  These APIs are used to create a DNS request to each individual server.  The dns.message API is used to make a query request in dns.message.make_query. The dns.query API is used to actually send the query over UDP in dns.query.udp.  The dns.name API is used to convert string objects into dns name objects that can be used by dnspython.  The time library is used to calculate the query time of the program in the form of time.time().  The datetime library is used to print the data and time of request. Finally, the sys library is used so the program can be run in the command line.

# How to run
To run the mydnsresolve.py file, use the command prompt.  On the command line, type 'python' followed by a space and then the
path name of the directory.  Next, (on the same line),  type in the domain name you wish to resolve. <br />
Example: <br />
python mydnsresolve.py www.cnn.com
