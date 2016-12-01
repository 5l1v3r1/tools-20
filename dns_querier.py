#!/usr/bin/env python'

# A simple DNS querier which takes some inline arguments

from scapy.all import *
from scapy.layers.dns import DNSRR, DNS, DNSQR

import time
import datetime
import sys
import pickle
import sys, getopt
import argparse

parser = argparse.ArgumentParser(description='### DNS Poller 0.1 ### by Avanzo')
parser.add_argument('-q', '--query', default='google.com', required=True, help='query argument')
parser.add_argument('-s', '--server', default='8.8.8.8',required=True, help='DNS server')
parser.add_argument('-i', '--interval', default=1,help='interval between each query')
parser.add_argument('-t', '--timeout' , default=2, help='query timeout')
parser.add_argument('-f', '--logfile' , default='1', help='optional logfile')


args = parser.parse_args()
args = vars(parser.parse_args())

server_dst = args.get('server')
query_dst  = args.get('query')
interval = args.get('interval')
timeout = args.get('timeout')
logfile = args.get('logfile')

print server_dst
print query_dst
print logfile

total_no_answer = 0
total_answered = 0


#initial time
ts = time.time()
initial_st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# declare Time stamps
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


print len(logfile)

if len(logfile) > 1:
	while True:
		dns_answer = sr1(IP(dst=server_dst)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=query_dst)),verbose=0, inter=interval,timeout=timeout)
		file = open(logfile, "w")
		if dns_answer is None:
			total_no_answer = total_no_answer +1
			file.write("### script started at   "+initial_st+" ###\n")
			file.write(st +" " + "dns_total_ANSWERED=%d \n" % (total_answered))
			file.write(st +" " + "dns_total_NOT_ANSWERED=%d \n" % (total_no_answer))
			file.flush()
		else:
			total_answered = total_answered + 1
			file.write(st +" " + "dns_total_ANSWERED=%d \n" % (total_answered))
			file.write(st +" " + "dns_total_NOT_ANSWERED=%d \n" % (total_no_answer))
			file.flush()

else:
	while True:
		dns_answer = sr1(IP(dst=server_dst)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname=query_dst)),verbose=0, inter=interval,timeout=timeout)
		if dns_answer is None:
			total_no_answer = total_no_answer +1
			print  "### script started at" +initial_st+" ###\n"
			print  "dns_total_ANSWERED=%d \n" % (total_answered)
			print  st +" " + "dns_total_NOT_ANSWERED=%d \n" % (total_no_answer)
		else:
			total_answered = total_answered + 1
			print st +" " + " dns_total_ANSWERED=%d \n" % (total_answered)
			print st +" " + " dns_total_NOT_ANSWERED=%d \n" % (total_no_answer)

	dns_answer.show()

sys.exit('Error!')
