#!/usr/bin/env python3

import os, sys, requests, argparse, http, datetime, socket
from tqdm import tqdm
from prettytable import PrettyTable

def parse_args():
    # Create the arguments
    parser = argparse.ArgumentParser(prog='HTTPS Test')
    parser.add_argument("-f", "--file", help="Location to domain list. Example: -f ./domains.csv")
    parser.add_argument("-d", "--domain", help="Check a single domain. Example: -d example.com")
    return parser.parse_args()

args = parse_args()


c = 0

def run(domain):
    global c

    #print("\033[32mRunning...\033[0m")
    tqdm.write('\033[32mRunning...\033[0m')
    try:
        #print('\033[33mChecking %s:80\033[0m' % (domain))
        tqdm.write('\033[33mChecking %s:80\033[0m' % (domain))

        h1 = http.client.HTTPConnection(domain, timeout=3)
        h1.request("GET", "/")
        r1 = h1.getresponse()
        http_status = '%s %s' % (r1.status, r1.reason)
        #print('HTTP status: %s' % http_status)
        tqdm.write('HTTP status: %s' % http_status)
    except socket.timeout:
        #print('Timeout Reached for domain %s' % domain)
        tqdm.write('Timeout Reached for domain %s' % domain)
        http_status = 'Timed out'
        pass
    except Exception:
        tqdm.write('\033[31mA HTTP Error occured for domain %s\033[0m' % domain)
        http_status = 'HTTP Error'
        redirect = False
        xss_protection = False
        #result = domain, http_status, https_status, https, redirect, xss_protection
        #return result
        pass

    try:
        #print('\033[33mChecking %s:443\033[0m' % (domain))
        tqdm.write('\033[33mChecking %s:443\033[0m' % (domain))
        h2 = http.client.HTTPSConnection(domain, timeout=3)
        h2.request("GET", "/")
        r2 = h2.getresponse()
        https_status = '%s %s' % (r2.status, r2.reason)
        #print('HTTPS status: %s' % https_status)
        tqdm.write('HTTPS status: %s' % https_status)
    # HTTPS is the 2nd and final timeout error. Return results if it happends and contimue.
    except socket.timeout:
        #print('Timeout Reached for domain %s' % domain)
        tqdm.write('Timeout Reached for domain %s' % domain)
        https_status = 'Timed out'
        https = False
        redirect = False
        xss_protection = False
        result = domain, http_status, https_status, https, redirect, xss_protection
        return result
    except Exception:
        #print('\033[31mA SSL Error occured for domain %s\033[0m' % domain)
        tqdm.write('\033[31mA SSL Error occured for domain %s\033[0m' % domain)
        https_status = 'SSL Error'
        https = False
        redirect = False
        xss_protection = False
        #result = domain, http_status, https_status, https, redirect, xss_protection
        #return result
        pass

    try:
        if r1.status != 200 and r2.status != 200 and domain.startswith('www.'):
            #print("\033[33mBoth HTTP and HTTPS seem to be unreachable for %s, check the domain. Trying again, stripping www.\033[0m" % domain)
            tqdm.write("\033[33mBoth HTTP and HTTPS seem to be unreachable for %s, check the domain. Trying again, stripping www.\033[0m" % domain)
            if domain.startswith('www.'):
                try:
                    domain = domain[4:] # Strip www.
                    #print('\033[33mChecking %s:80\033[0m' % (domain))
                    tqdm.write('\033[33mChecking %s:80\033[0m' % (domain))
                    h1 = http.client.HTTPConnection(domain, timeout=3)
                    h1.request("GET", "/")
                    r1 = h1.getresponse()
                    http_status = '%s %s' % (r1.status, r1.reason)
                    #print('HTTP status: %s' % http_status)
                    tqdm.write('HTTP status: %s' % http_status)
                except socket.timeout:
                    #print('Timeout Reached for domain %s' % domain)
                    tqdm.write('Timeout Reached for domain %s' % domain)
                    http_status = 'Timed out'
                    pass

                try:
                    #print('\033[33mChecking %s:443\033[0m' % (domain))
                    tqdm.write('\033[33mChecking %s:443\033[0m' % (domain))
                    h2 = http.client.HTTPSConnection(domain, timeout=3)
                    h2.request("GET", "/")
                    r2 = h2.getresponse()
                    https_status = '%s %s' % (r2.status, r2.reason)
                    #print('HTTPS status: %s' % https_status)
                    tqdm.write('HTTPS status: %s' % https_status)
                except socket.timeout:
                    #print('Timeout Reached for domain %s' % domain)
                    tqdm.write('Timeout Reached for domain %s' % domain)
                    https_status = 'Timed out'
                    https = False
                    redirect = False
                    xss_protection = False
                    result = domain, http_status, https_status, https, redirect, xss_protection
                    return result


        elif r1.status != 200 and r2.status != 200:
            #print("\033[33mBoth HTTP and HTTPS seem to be unreachable for %s, check the domain: trying again, adding 'www.'.\033[0m" % domain)
            tqdm.write("\033[33mBoth HTTP and HTTPS seem to be unreachable for %s, check the domain: trying again, adding 'www.'.\033[0m" % domain)
            if not domain.startswith('www.'):
                try:
                    domain = 'www.' + domain
                    #print('\033[33mChecking %s:80\033[0m' % (domain))
                    tqdm.write('\033[33mChecking %s:80\033[0m' % (domain))
                    h1 = http.client.HTTPConnection(domain, timeout=3)
                    h1.request("GET", "/")
                    r1 = h1.getresponse()
                    http_status = '%s %s' % (r1.status, r1.reason)
                    #print('HTTP status: %s' % http_status)
                    tqdm.write('HTTP status: %s' % http_status)
                except socket.timeout:
                    #print('Timeout Reached for domain %s' % domain)
                    tqdm.write('Timeout Reached for domain %s' % domain)
                    http_status = 'Timed out'
                    pass

                try:
                    #print('\033[33mChecking %s:443\033[0m' % (domain))
                    tqdm.write('\033[33mChecking %s:443\033[0m' % (domain))
                    h2 = http.client.HTTPSConnection(domain, timeout=3)
                    h2.request("GET", "/")
                    r2 = h2.getresponse()
                    https_status = '%s %s' % (r2.status, r2.reason)
                    #print('HTTPS status: %s' % https_status)
                    tqdm.write('HTTPS status: %s' % https_status)
                except socket.timeout:
                    #print('Timeout Reached for domain %s' % domain)
                    tqdm.write('Timeout Reached for domain %s' % domain)
                    https_status = 'Timed out'
                    https = False
                    redirect = False
                    xss_protection = False
                    result = domain, http_status, https_status, https, redirect, xss_protection
                    return result
    except Exception as e:
        #print('\033[36m%s\033[0m' % e)
        tqdm.write('\033[36m%s\033[0m' % e)

    try:
        if r2.status == 200:
            https = True
            c+=1 # Count https domains
        else:
            https = False
    except Exception:
        https = False

    # Follow redirects
    try:
        r = requests.get('http://' + domain)

        if r.history:
            #print("Request was redirected")
            tqdm.write("Request was redirected")

            for resp in r.history:
                #print(resp.status_code, resp.url)
                tqdm.write('%s %s' % (resp.status_code, resp.url))
            #print("Final destination:")
            tqdm.write("Final destination:")
            #print(r.status_code, r.url)
            tqdm.write('%s %s' % (r.status_code, r.url))

            if r.url.startswith('https://') and r.status_code == 200:
                redirect = True
                if not https == True:
                    https = True
                    https_status = '%s %s' % (r.status_code, r.reason)
                    c+=1
            elif r.url.startswith('http://') and r.status_code == 200:
                redirect = False
                http_status = '200 OK'
            else:
                redirect = False

        else:
            #print("Request was not redirected")
            tqdm.write("Request was not redirected")
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

    #print('X-XSS-Protection: %s' % xss_protection)
    tqdm.write('X-XSS-Protection: %s' % xss_protection)

    h1.close(); h2.close() # Close connections

    result = domain, http_status, https_status, https, redirect, xss_protection
    return result

def test_single_domain(domain):
    starts = datetime.datetime.now()

    table = PrettyTable(['Domain', 'HTTP status', 'HTTPS status', 'HTTPS', 'Redirected', 'X-XSS-Protection']) # Table header
    table.align = 'l' # Align left

    try:
        result = run(domain)
        table.add_row([result[0], result[1], result[2], result[3], result[4], result[5]])
        print(table) # Show result

    except Exception as e:
        print(e)
        pass

    except KeyboardInterrupt:
        print('\nCanceled...')

def test_domains(file):
    start = datetime.datetime.now()

    table = PrettyTable(['Domain', 'HTTP status', 'HTTPS status', 'HTTPS', 'Redirected', 'X-XSS-Protection']) # Table header
    table.align = 'l' # Align left

    try:
        f = open(file).readlines()

        with tqdm(total=(len(f)), desc='Progress') as bar:
            for domain in f:
                domain = domain.strip() # Strip \n and b' and stuff
                result = run(domain) # Run test
                bar.update(1)
                table.add_row([result[0], result[1], result[2], result[3], result[4], result[5]])

            # Calculate how much percentage is HTTPS and error.
            secure = 100 / len(f) * c
            print('\n')
            print(table) # Show result

            print("\033[32mFinished checking {} domains in {} of which {} ({}%) has HTTPS.\033[0m".format(len(f), datetime.datetime.now()-start, c, secure))
            sys.exit(0) # Done, exit script.


    except Exception as e:
        print(e)
        pass

    except KeyboardInterrupt:
        print('\n')
        print(table) # Show result
        print('\nCanceled...')

def banner():
    logo = '''
     .--------.
    / .------. \\
   / /        \ \\
   | |        | |
  _| |________| |_
.' |_|        |_| '.
'._____ ____ _____.'
|     .'____'.     |
'.__.'.'    '.'.__.'
'.__  |      |  __.'
|   '.'.____.'.'   |
'.____'.____.'____.'
'.________________.'
    '''
    return logo

if args.domain:
    print(banner())
    test_single_domain(args.domain)
elif args.file:
    print(banner())
    if os.path.isfile(args.file):
        test_domains(args.file)
    else:
        print('\033[31m[ERROR]\033[0m File does not exist')
