from device import Device
import xmltodict
import json
import sys
import os.path

#This function takes the list of IP address and uses that to log into each switch
#The IP addresses from the host file and the mac address fromt the arguments are passed.
#If the mac address is found on a port that starts with "Ethernet", then it will print the
#port that that mac was learned on as well as the VLAN it was learned on.
#The name of the switch is actually pulled from show_hardware()
def show_mac_addr(sw,mac):
	getdata = sw.show('show mac address-table')
	show_mac_dict = xmltodict.parse(getdata[1])
	data = show_mac_dict['ins_api']['outputs']['output']['body']['TABLE_mac_address']['ROW_mac_address']
	mac_addr_list = {}
	for each in data:
		if 'disp_mac_addr' in each.keys():
			key = each['disp_mac_addr']
			mac_addr_list[key] = each['disp_mac_addr']
			if each['disp_mac_addr'] == mac and each['disp_port'].find('port') == -1:
				print "PORT: ", each['disp_port']
				print "VLAN: ", each['disp_vlan']			
	print "=" *50
	return each['disp_vlan']

#This functon calls the cli command 'show hardware' and prints the hostname of the switch.
def show_hardware(sw):
	getdata = sw.show('show hardware')
	show_hw_dict = xmltodict.parse(getdata[1])
	data = show_hw_dict['ins_api']['outputs']['output']['body']
	print "Searching in HOSTNAME: ",data['host_name']
	return data

def main():
	args = sys.argv
	
	if len(args) == 5:

		#This section will check to see if the file pass to Python in a argument actually exists
		if os.path.exists(args[2]):
			switch_ips = open(args[2]).read().splitlines()
			#print switch_ips
		else:
			print 'File ', os.path.realpath(args[2]), 'does not exist.  Please try again'
			sys.exit(1)
		
		for switch_ip in switch_ips:	
			switch = Device(ip=switch_ip,username=args[3],password=args[4])
			switch.open()
			hw = show_hardware(switch)
			show_mac_addr(switch,args[1])			
	else:
		print 'ERROR: Invalid syntax\n'\
		'Example: \"python findMac.py xxxx.xxxx.xxxx file.txt username password\"'
		sys.exit(1)

if __name__ == "__main__":
	main()

