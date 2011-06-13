#TODO: reuse TCP connection, as in httplib snippet at http://stackoverflow.com/questions/4855810/python-downloading-files-from-http-server

import urllib2
from urllib2 import HTTPError
import os
import sys
from time import sleep

output_dir = os.environ['HOME'] + '/Projects/topicalguide/datasets/palin_emails/files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
#Ranges (inclusive): 5082-5389, 5910-6629, 10109-16423, 17231-21932

total_emails = 24199
emails_fetched = 6579#0

for email_num in range(15660, 30000):
    if email_num % 100 == 0 and email_num > 0:
            print
            print email_num,
            sleep(5)
    
    try:
        url = 'http://palinemail.msnbc.msn.com/palin2011/pdf/{0}.pdf'.format(email_num)
        output_filename = '{0}/{1}.pdf'.format(output_dir, email_num)
        
        r = urllib2.urlopen(url)
        w = open(output_filename, 'w')
        w.write(r.read())
        w.close()
        r.close()
        
        print '{0} -> {1}'.format(url, output_filename)
        emails_fetched += 1
    except HTTPError as e:
        if e.code != 404: print e
        else: sys.stdout.write('.')
    
    
    if emails_fetched == total_emails: break
