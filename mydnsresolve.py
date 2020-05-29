import dns.message
import dns.name
import dns.query
import time
import datetime
import sys


# Process the response we get back
def response(query_request, query_response, start_time, domain_list, index, domainstr, oldauthority_list, auth_index):
    # First rrset to look through
    domainstr = domain_list[index] + '.' + domainstr
    qname = dns.name.from_text(domainstr)
    answer = query_response.find_rrset(query_response.answer, qname, dns.rdataclass.IN, dns.rdatatype.A, create=True)
    cnam = query_response.find_rrset(query_response.answer, qname, dns.rdataclass.IN, dns.rdatatype.CNAME, create=True)
    # Base case: it's done resolving
    if index == 0:
        print("ANSWER SECTION: ")
        if len(answer) != 0:
            print(answer)
        else:
            print(cnam)
        print("Query Time: ")
        end_time = time.time_ns()
        print((end_time - start_time) // 1000000, end=" ")
        print("ms")
        print("When: ")
        # Get when request is made
        now = datetime.datetime.today()
        print(now.strftime("%a %b %d %H:%M:%S %Y"))
    else:
        # Parse the response to find rrset
        parse = query_response.find_rrset(query_response.authority, qname, dns.rdataclass.IN, dns.rdatatype.NS,
                                          create=True)
        for i in parse:
            oldauthority_list.append(i)
        # We have the list of authority set
        parse2 = oldauthority_list[auth_index].to_text()
        qname = dns.name.from_text(parse2)
        # Want to find ip address in additional
        add = query_response.find_rrset(query_response.additional, qname, dns.rdataclass.IN, dns.rdatatype.A,
                                        create=True)
        ipdd = add.to_text().split(" ")
        ip = ipdd[len(ipdd) - 1]
        index = index - 1
        new_response = dns.query.udp(query_request, ip, timeout=5)
        auth_index = len(oldauthority_list)
        response(query_request, new_response, start_time, domain_list, index, domainstr, oldauthority_list, auth_index)


def main():
    if len(sys.argv) != 2:
        print("Please input domain")
    else:
        domain = sys.argv[len(sys.argv) - 1]
        root = '198.41.0.4'
        domain_list = domain.split(".")
        domain_name = dns.name.from_text(domain)
        start_time = time.time_ns()
        request = dns.message.make_query(domain_name, dns.rdatatype.A)
        print("QUESTION SECTION: ")
        # Getting the question set of the request
        question = request.find_rrset(request.question, domain_name, dns.rdataclass.IN, dns.rdatatype.A, create=True)
        print(question)
        index = len(domain_list) - 1
        # Send the first request to root
        query_response = dns.query.udp(request, root, timeout=5)
        domainstr = ""
        authority_list = []
        response(request, query_response, start_time, domain_list, index, domainstr, authority_list, 0)


if __name__ == "__main__":
    main()
