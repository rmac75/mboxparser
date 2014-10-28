#!/usr/bin/python

import mailbox
import sys
import csv

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

  f = open(sys.argv[2], 'wt')
  try:
    	writer = csv.writer(f)
  	writer.writerow( ('Date','From', 'To', 'Subject', 'Received-Last','X-Mailer'))

	for message in mailbox.mbox(mbox):
    		From = str(message['From'])
		To = str(message['To'])
		Date = str(message['Date'])
		Subject = str(message['Subject'])
		Received = str(message['Received'])
		XMailer = str(message['X-Mailer'])			
		#Body = str(message['Body'])
		
		writer.writerow((Date,From,To,Subject,Received,XMailer))    		
		        
  finally:
    	f.close()

#print open(sys.argv[1], 'rt').read()



if __name__ == '__main__':
   main()
