import sys
import requests
import dns.resolver
from dns.resolver import NXDOMAIN
from dns.exception import DNSException

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = [sys.argv[1]]
resolver.timeout = 0.5
feeds = [
    'https://isc.sans.edu/feeds/suspiciousdomains_High.txt',
    'https://isc.sans.edu/feeds/suspiciousdomains_Medium.txt',
    #'https://isc.sans.edu/feeds/suspiciousdomains_Low.txt',
    'https://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt'
]

def domain_checker(domain):
    try:
        answers = resolver.query(domain)
        # print(answers)
        # for rdata in answers:
        #     print(rdata)
        return 0
    except NXDOMAIN:
        #print('NXDOMAIN:'+ domain)
        return 1
    except DNSException:
        #print('Other exception:'+domain)
        return 2

def feed_processor(url):
    feed = requests.get(url)
    lines = feed.iter_lines()
    pass_count = 0
    nx_count = 0
    fail_count =0
    for line in lines:
        if line.decode('UTF-8').startswith('#'):
            continue
        elif line.decode('UTF-8') == 'Site':
            continue
        else:
            #print(line.decode('UTF-8'))
            result = domain_checker(line.decode('UTF-8'))
            if result== 0:
                pass_count +=1
            elif result ==1:
                nx_count +=1
            elif result ==2:
                fail_count +=1

    print('Feed source: '+ url)
    print('Pass: '+str(pass_count))
    print('NXDOMAIN: '+str(nx_count))
    print('FAIL: '+str(fail_count))

for feed in feeds:
    feed_processor(feed)
