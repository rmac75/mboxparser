#!/usr/bin/python2

#--------------------------------
#Takes in mbox, spits out csv with email info and basic geolocation, plus other header fields.
#--------------------------------

#This product includes GeoLite2 data created by MaxMind, available from
#<a href="http://www.maxmind.com">http://www.maxmind.com</a>.

import mailbox
import sys
import csv
import re
from os import path
import pprint
import argparse
import geoip2.database
import geoip2.errors
import pygeoip
import email.utils

def get_iprecord(ip):
    try:
        geo = reader.city(ip)
	org = reader2.org_by_addr(ip)
    except (geoip2.errors.AddressNotFoundError, ValueError):
        return None,None,None
    if geo.city.name:
	cityname=geo.city.name.encode('ascii','ignore')
    else:
	cityname=geo.city.name

    return geo.country.iso_code, cityname, org

def main():

  # first some sanity tests on the command-line arguments
  #sys.argv = ['mbox_to_mysql','list1.mbox','mailman','lists',] # !@!@! APS here for testing purposes only - comment out for live run

  parser = argparse.ArgumentParser(description='Parse mbox file')
  parser.add_argument('mbox', help='mbox file to parse')
  parser.add_argument('outfile', help='output csv file')
  args = parser.parse_args()
  if not path.isfile(args.mbox):
      parser.error("the file %s does not exist"%args.mbox)
  mbox = args.mbox
  outfile = args.outfile
  ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

  global reader
  reader = geoip2.database.Reader('geo/GeoLite2-City.mmdb')
  global reader2
  reader2 = pygeoip.GeoIP('geo/GeoIPOrg.dat')

  f = open(outfile, 'wt')
  try:
    	writer = csv.writer(f)
  	writer.writerow( ('Date','From','From Email','Return-Path Email','To','To Email','X-To','Subject','Received-Last','Org','City', 'Country','X-IP','X-Org', 'X-City', 'X-Country','X-Mailer'))

	for message in mailbox.mbox(mbox):
    		From = str(message['From'])
		fname,femail = email.utils.parseaddr(From)
		#print fname
		Return = str(message['Return-Path'])
		rname,remail = email.utils.parseaddr(Return)
		#print remail
		To = str(message['To'])
		tname,temail = email.utils.parseaddr(To)
		XTo = str(message['X-Apparently-To'])
		#findIP = re.findall(ipPattern,s)
		Date = str(message['Date'])
		Subject = str(message['Subject'])

		Received = re.findall(ipPattern,str(message['Received']))
		if Received:
			#print Received[-1]
			country, city, org = get_iprecord(Received[-1])			
			#print get_iprecord(Received[-1])
			#print org
		else:
			Received = "None"

		XIP = message['X-Originating-IP']
		if XIP:
			XIP = str(XIP).strip('[]')
			#print ("XIP: %s." % XIP)
			Xcountry, Xcity, Xorg = get_iprecord(XIP)
		else:
			XIP = "None"
			Xcountry = "None"
			Xcity = "None"
			Xorg = "None"

		XMailer = str(message['X-Mailer'])
		#Attachment = message.get_filename()
		#Body = str(message['Body'])

		writer.writerow((Date,fname,femail,remail,tname,temail,XTo,Subject,Received[-1],org,city,country,XIP,Xorg,Xcity,Xcountry,XMailer))
  finally:
    	f.close()

#print open(sys.argv[1], 'rt').read()



if __name__ == '__main__':
   main()
