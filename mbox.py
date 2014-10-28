#!/usr/bin/python

import mailbox
import sys
import csv
import re
import pprint

def usage():
  print ("mbox.py: Parse mbox file")
  print ("Usage: %s mboxfile outfile" % sys.argv[0])
  print ("Example: ./%s mbox_file output.csv \n" % sys.argv[0])
  exit(0)

def main():
 
  # first some sanity tests on the command-line arguments
  #sys.argv = ['mbox_to_mysql','list1.mbox','mailman','lists',] # !@!@! APS here for testing purposes only - comment out for live run
 
  if len(sys.argv) != 3:
    usage()
    exit(-2)
  mbox = sys.argv[1]
  outfile = sys.argv[2]
  ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


  f = open(sys.argv[2], 'wt')
  try:
    	writer = csv.writer(f)
  	writer.writerow( ('Date','From','Return-Path','To','X-To','Subject','Received-Last','X-IP','X-Mailer'))

	for message in mailbox.mbox(mbox):
    		From = str(message['From'])
		Return = str(message['Return-Path'])
		To = str(message['To'])
		XTo = str(message['X-Apparently-To'])
		#findIP = re.findall(ipPattern,s)
		Date = str(message['Date'])
		Subject = str(message['Subject'])

		Received = re.findall(ipPattern,str(message['Received']))
		if Received:
			print Received[-1]
		else:
			Received = "None"	
		
		XIP = message['X-Originating-IP']
		if XIP:
			XIP = str(XIP).strip('[]')
		else:
			XIP = "None"
		XMailer = str(message['X-Mailer'])
		#Attachment = message.get_filename()			
		#Body = str(message['Body'])
		
		writer.writerow((Date,From,Return,To,XTo,Subject,Received[-1],XIP,XMailer))    		
  finally:
    	f.close()

#print open(sys.argv[1], 'rt').read()



if __name__ == '__main__':
   main()
