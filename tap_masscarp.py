# Original Author == @avicoder
# Modified and remixed == @avanzo
#
# This script aims to automate the burder when masscanning connected hosts on a local network via a virtual interface like tun or tap.
# Performs a masscan on the provided port, port-range for each host ARP'd on the LAN.

import sys,getopt,subprocess

r = '\033[31m' #red
b = '\033[34m' #blue
g = '\033[32m' #green
y = '\033[33m' #yellow
m = '\033[34m' #magenta
c = '\033[36m' #cyan


def main(argv):
	if len(sys.argv) < 6:
		print m+"\nInvalid Arguments"
		print b+ 'arp_masscan_virtual.py -i <virtual interface> -r <ip range> -p <masscan ports>'
		sys.exit()

	arp_table_dic = {}

	interface=''
	ip_range=''
	ports=''

	try:
		opts, args = getopt.getopt(argv,"hi:r:p:",["iface=","ips=","ports="])
	except KeyInterrupt:
		print 'arp.py -i <interface> -r <ip range>'
		sys.exit(1)
	for opt,arg in opts:
		if opt=='-h':
			print b+ 'arp_masscan_virtual.py -i <virtual interface> -r <ip range> -p <masscan ports>'
			sys.exit()
		elif opt in ("-i","--iface"):
			interface=arg
		elif opt in ("-r","--ips"):
			ip_range=arg
		elif opt in ("-p","--ports"):
			ports=arg


	print y+"\nScanning ..."
	from scapy.all import srp,Ether,ARP,conf
	conf.verb=0
	ans,uans=srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip_range),timeout=2,iface=interface,inter=0.1)
	for snd,rcv in ans:
	        print c+rcv.sprintf(r"%Ether.src% - %ARP.psrc%")
		arp_table_dic[rcv.sprintf("%ARP.psrc%")] = rcv.sprintf("%Ether.src%")
	print m+"\n ARP Scan complete"

	print m+"\nARP table saved in the following dictionary"
	print arp_table_dic

	for key, value in arp_table_dic.iteritems():
		subprocess.call(["masscan", "-p", ports ,key ,"--interface", interface , "--router-mac", value, "---wait=0"])



if __name__ == "__main__":
	main(sys.argv[1:])
