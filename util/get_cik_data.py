# -*- encoding: utf-8 -*-
# Grab vote-data from CIK website
# Data will be put here: ./data.csv
# example: python get_cik_data.py

import csv
import urllib2
from bs4 import BeautifulSoup
from httplib import BadStatusLine,IncompleteRead
import socket
import sys
import os
import datetime
import time

def console_out(text):
    time_current = datetime.datetime.now()
    timestamp = time_current.strftime('%Y-%m-%d %H:%M:%S')
    
    print(timestamp + "  " + text)

def get_file(link,id):
    numtries = 5
    timeoutvalue = 40
    timeinterval = 6
    id = str(id)
    
    for i in range(1,numtries+1):
        i = str(i)
        try:
            u = urllib2.urlopen(link, timeout = timeoutvalue)
        except BadStatusLine:
            console_out('BadStatusLine for ID:' + id + '.' + ' Attempt: ' + i)
            success = False
            time.sleep(3)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                console_out('We failed to reach a server for ID:' + id + ' Reason: ' + str(e.reason) + '.' + ' Attempt: ' + i)
            elif hasattr(e, 'code'):
                console_out('The server couldn\'t fulfill the request for ID: ' + id + ' Error code: ' + str(e.code) + '.' + ' Attempt: ' + i)
            success = False
            time.sleep(3)
        except socket.timeout, e:
            console_out('Connection timed out on urlopen() for ID: ' + id + '.' + ' Attempt: ' + i)
            success = False
            time.sleep(3)
        else:
            try:
                r = u.read()
            except socket.timeout, e:
                console_out('Connection timed out on socket.read() for ID: ' + id + '.' + ' Attempt: ' + i)
                success = False
                u.close()
                time.sleep(3)
            except IncompleteRead:
                console_out('Incomplete read on socket.read() for ID: ' + id + '.' + ' Attempt: ' + i)
                success = False
                u.close()
                time.sleep(3)
            else:
                #console_out("Listing " + id + " downloaded")
                success = True
                break
    
    return success,r

def parse_endnode(link,level):
    success,res = get_file(link,1)
    soup = BeautifulSoup(''.join(res))
    tables = soup.findAll('table')

    navs = tables[2].findAll('tr')[0].findAll('a')

    up_vals = []
    for nav in navs:
        name = nav.text.encode("utf-8")
        link = nav['href']
        up_vals.append(name)

    if len(navs) < maxlevel+1:
        up_vals.extend((maxlevel+1 - len(navs))*[''])

    table = tables[2].findAll('table')[4]
    trs = table.findAll('tr')

    vals = []
    for tr in trs:
        tds = tr.findAll('td')
        if len(tds) > 2:
            val = int(tds[2].findAll('b')[0].text)
            vals.append(val)

    up_vals.append(level)
    up_vals.extend(vals)
    data_out.writerow(up_vals)
    print up_vals[1] + ", " + up_vals[2]+ ", " + up_vals[3]

def parse_middlenode(soup,level):
    form = soup.findAll('form')[0]
    options = form.findAll('option')[1:]
    level = level + 1

    for option in options:
        link = option['value']
        name = option.text

        success,res = get_file(link,1)
        soup = BeautifulSoup(''.join(res))
        forms = soup.findAll("form")
        #For middle levels, you can process it to get a list and general data
        
        if level < maxlevel:
            parse_endnode(link,level)

        if forms:
            parse_middlenode(soup,level)
        else:
            parse_endnode(link,level)


if __name__ == '__main__':
    root_link = "http://www.moscow_city.vybory.izbirkom.ru/region/region/moscow_city?action=show&root=1&tvd=27720001539818&vrn=27720001539308&region=77&global=null&sub_region=77&prver=0&pronetvd=null&vibid=27720001539818&type=426"
    success,res = get_file(root_link,1)
    soup = BeautifulSoup(''.join(res))
    f_out = open('data.csv','wb')
    data_out = csv.writer(f_out)
    
    #TODO: put out to params
    maxlevel = 3

    parse_middlenode(soup,0)

    f_out.close()
