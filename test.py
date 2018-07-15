#!/usr/bin/env python3

import os, sys, requests, argparse, http, datetime, socket
from prettytable import PrettyTable

def parse_args():
    #Create the arguments
    parser = argparse.ArgumentParser(prog='HTTPS Test')
    parser.add_argument("-f", "--file", help="Location to domain list. Example: -f ./domains.csv")
    parser.add_argument("-d", "--domain", help="Check a single domain. Example: -d example.com")
    return parser.parse_args()

args = parse_args()

def test_single_domain(domain):
    starts = datetime.datetime.now()

    table = PrettyTable(['Domain', 'HTTP status', 'HTTPS status', 'HTTPS', 'Auto redirected', 'X-XSS-Protection']) # Table header
    table.align = 'l' # Align left

    try:
        try:
            print('\033[33mChecking %s:80\033[0m' % (domain))
            h1 = http.client.HTTPConnection(domain, timeout=10)
            h1.request("GET", "/")
            r1 = h1.getresponse()
            http_status = '%s %s' % (r1.status, r1.reason)
            print('HTTP status: %s' % http_status)
        except socket.timeout:
            print('Timeout Reached for domain %s' % domain)
            http_status = 'Timed out'
            pass

        try:
            print('\033[33mChecking %s:443\033[0m' % (domain))
            h2 = http.client.HTTPSConnection(domain, timeout=10)
            h2.request("GET", "/")
            r2 = h2.getresponse()
            https_status = '%s %s' % (r2.status, r2.reason)
            print('HTTPS status: %s' % https_status)
        except socket.timeout:
            print('Timeout Reached for domain %s' % domain)
            https_status = 'Timed out'

        try:
            if r2.status == 200:
                https = True
            else:
                https = False
        except Exception:
            https = False

        # ToDo: Fix redirect test
        try:
            if not r1.status == 200:
                redirect = True
            else:
                redirect = False
        except Exception:
            redirect = False

        if not http_status.startswith('200'):
            try:
                if r2.getheader('X-XSS-Protection') == '1; mode=block':
                    xss_protection = True
                else:
                    xss_protection = False
            except Exception:
                xss_protection = False
        else:
            if r1.getheader('X-XSS-Protection') == '1; mode=block':
                xss_protection = True
            else:
                xss_protection = False

        print('X-XSS-Protection: %s' % xss_protection)

        h1.close(); h2.close() # Close connections

        result = domain, http_status, https_status, https, redirect, xss_protection
        table.add_row([result[0], result[1], result[2], result[3], result[4], result[5]])
        print(table) # Show result

    except Exception as e:
        print(e)
        pass

    except KeyboardInterrupt:
        print('\nCanceled...')

def test_domains(file):
    start = datetime.datetime.now()
    c = 0

    table = PrettyTable(['Domain', 'HTTP status', 'HTTPS status', 'HTTPS', 'Auto redirected', 'X-XSS-Protection']) # Table header
    table.align = 'l' # Align left
    try:
        f = open(file).readlines()

        for domain in f:
            domain = domain.strip() # Strip \n and b' and stuff

            try:
                print('\033[33mChecking %s:80\033[0m' % (domain))
                h1 = http.client.HTTPConnection(domain, timeout=10)
                h1.request("GET", "/")
                r1 = h1.getresponse()
                http_status = '%s %s' % (r1.status, r1.reason)
                print('HTTP status: %s' % http_status)
            except socket.timeout:
                print('Timeout Reached for domain %s' % domain)
                http_status = 'Timed out'
                continue

            try:
                print('\033[33mChecking %s:443\033[0m' % (domain))
                h2 = http.client.HTTPSConnection(domain, timeout=10)
                h2.request("GET", "/")
                r2 = h2.getresponse()
                https_status = '%s %s' % (r2.status, r2.reason)
                print('HTTPS status: %s' % https_status)
            except socket.timeout:
                print('Timeout Reached for domain %s' % domain)
                https_status = 'Timed out'
                continue


            if r1.status != 200 and r2.status != 200 and domain.startswith('www.'):
                print("\033[33mBoth HTTP and HTTPS seem to be unreachable for %s, check the domain. Trying again, stripping www.\033[0m" % domain)
                if domain.startswith('www.'):
                    domain = domain[4:] # Strip www.
                    print('\033[33mChecking %s:80\033[0m' % (domain))
                    h1 = http.client.HTTPConnection(domain, timeout=10)
                    h1.request("GET", "/")
                    r1 = h1.getresponse()
                    http_status = '%s %s' % (r1.status, r1.reason)
                    print('HTTP status: %s' % http_status)


                    print('\033[33mChecking %s:443\033[0m' % (domain))
                    h2 = http.client.HTTPSConnection(domain, timeout=10)
                    h2.request("GET", "/")
                    r2 = h2.getresponse()
                    https_status = '%s %s' % (r2.status, r2.reason)
                    print('HTTPS status: %s' % https_status)

            elif r1.status != 200 and r2.status != 200:
                print("\033[33mBoth HTTP and HTTPS seem to be unreachable for %s, check the domain: trying again, adding 'www.'.\033[0m" % domain)
                if not domain.startswith('www.'):
                    domain = 'www.' + domain
                    print('\033[33mChecking %s:80\033[0m' % (domain))
                    h1 = http.client.HTTPConnection(domain)
                    h1.request("GET", "/")
                    r1 = h1.getresponse()
                    http_status = '%s %s' % (r1.status, r1.reason)
                    print('HTTP status: %s' % http_status)


                    print('\033[33mChecking %s:443\033[0m' % (domain))
                    h2 = http.client.HTTPSConnection(domain)
                    h2.request("GET", "/")
                    r2 = h2.getresponse()
                    https_status = '%s %s' % (r2.status, r2.reason)
                    print('HTTPS status: %s' % https_status)


            try:
                if r2.status == 200:
                    https = True
                    c+=1 # Count https domains
                else:
                    https = False
            except Exception:
                https = False

            # ToDo: Fix redirect test
            try:
                if not r1.status == 200:
                    redirect = True
                else:
                    redirect = False
            except Exception:
                redirect = False

            if not http_status.startswith('200'):
                try:
                    if r2.getheader('X-XSS-Protection') == '1; mode=block':
                        xss_protection = True
                    else:
                        xss_protection = False
                except Exception:
                    xss_protection = False
            else:
                if r1.getheader('X-XSS-Protection') == '1; mode=block':
                    xss_protection = True
                else:
                    xss_protection = False

            print('X-XSS-Protection: %s' % xss_protection)

            h1.close(); h2.close() # Close connections

            result = domain, http_status, https_status, https, redirect, xss_protection
            table.add_row([result[0], result[1], result[2], result[3], result[4], result[5]])

        # Calculate how much % is HTTPS
        one = 100 / len(f)
        secure = c*int(one)

        print(table) # Show result

        print("\033[32mFinished checking {} domains in {} of which {}% has HTTPS.\033[0m".format(len(f), datetime.datetime.now()-start, secure))


    except Exception as e:
        print(e)
        pass

    except KeyboardInterrupt:
        print('\nCanceled...')

if args.domain:
    test_single_domain(args.domain)
elif args.file:
    if os.path.isfile(args.file):
        test_domains(args.file)
    else:
        print('\033[31m[ERROR]\033[0m File does not exist')
