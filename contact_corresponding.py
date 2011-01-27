#!/usr/bin/env python
# encoding: utf-8
"""
@author: Heather Piwowar
@contact:  hpiwowar@gmail.com
"""

import sys
import os
import csv
import glob
from string import Template
import html2text

ISI_EMAIL_FIELD_NAME = "EM"
ISI_JOURNAL_FIELD_NAME = "JI"
ISI_YEAR_FIELD_NAME = "PY"
ISI_MONTH_FIELD_NAME = "PD"
ISI_VOLUME_FIELD_NAME = "VL"
ISI_ISSUE_FIELD_NAME = "IS"
ISI_ARTICLE_TYPE_FIELD_NAME = "DT"

SCOPUS_EMAIL_FIELD_NAME = "Correspondence Address"
SCOPUS_JOURNAL_FIELD_NAME = "Source title"
SCOPUS_YEAR_FIELD_NAME = "Year"
SCOPUS_ISSUE_FIELD_NAME = "Issue"
SCOPUS_VOLUME_FIELD_NAME = "Volume"

def get_scopus_journal(row):
	journal = row[SCOPUS_JOURNAL_FIELD_NAME]
	return(journal)

def get_scopus_year(row):
	year = row[SCOPUS_YEAR_FIELD_NAME]
	return(year)

def get_scopus_month(row):
    return("")

def get_scopus_volume_issue(row):
	volume_issue = row[SCOPUS_VOLUME_FIELD_NAME] + "_" + row[SCOPUS_ISSUE_FIELD_NAME]
	return(volume_issue)

def get_scopus_emails(row):
	emails = [row[SCOPUS_EMAIL_FIELD_NAME].split(" ")[-1]]
	return(emails)

def get_scopus_fields(filename):
	reader = csv.DictReader(open(filename, "r"), delimiter=",")
	tuples = [(get_scopus_journal(row), get_scopus_year(row), get_scopus_month(row), get_scopus_emails(row), get_scopus_volume_issue(row)) for row in reader]
	return(tuples)

def get_scopus_all_fields(dir):
    tuples = []
    for filename in glob.glob(os.path.join(dir, "*", "*.csv")):
        tuples += get_scopus_fields(filename)
    return(tuples)    

def get_isi_article_type(row):
	article_type = row[ISI_ARTICLE_TYPE_FIELD_NAME]
	return(article_type)

def get_isi_journal(row):
	journal = row[ISI_JOURNAL_FIELD_NAME]
	return(journal)

def get_isi_year(row):
	year = row[ISI_YEAR_FIELD_NAME]
	return(year)

def get_isi_volume_issue(row):
	volume_issue = row[ISI_VOLUME_FIELD_NAME] + "_" + row[ISI_ISSUE_FIELD_NAME]
	return(volume_issue)

def get_isi_month(row):
    try:
        month = row[ISI_MONTH_FIELD_NAME][0:3]
    except IndexError:
        month = ""
    if (len(month) < 1):
        month = get_isi_journal(row) + "-" + get_isi_volume_issue(row)       
    return(month)

def get_isi_emails(row):
	emails = row[ISI_EMAIL_FIELD_NAME].split("; ")
	return(emails)

def get_isi_fields(filename):
	reader = csv.DictReader(open(filename, "r"), delimiter="\t", quoting=csv.QUOTE_NONE)
	tuples = [(get_isi_journal(row), get_isi_year(row), get_isi_month(row), get_isi_emails(row), get_isi_volume_issue(row), get_isi_article_type(row)) for row in reader]
	return(tuples)

def get_isi_all_fields(dir):
    tuples = []
    for filename in glob.glob(os.path.join(dir, "*", "*.txt")):
        tuples += get_isi_fields(filename)
    return(tuples)    
    
def get_email_text(text, contact_dict):
    email_template = Template(text)
    email_text = email_template.substitute(contact_dict)
    return(email_text)

def send_email(html_body, subject, to_addresses, cc_addresses, bcc_addresses, from_address):
    # Based on code from http://docs.python.org/library/email-examples.html
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = ', '.join(to_addresses)
    msg['Cc'] = ', '.join(cc_addresses)
    msg['From'] = from_address

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head></head>
      <body>
        <p>""" + html_body + """\
        </p>
      </body>
    </html>
    """
    text = html2text.html2text(html_body)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # gmail authentication here, but do not allow a customized From address:  http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html
    #mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    #mailServer.ehlo()
    #mailServer.starttls()
    #mailServer.ehlo()
    #password = ""  #password = input('please enter password')
    #mailServer.login("impactofjournaldatapolicies@gmail.com", password)
   
    mailServer = smtplib.SMTP("shawmail.vc.shawcable.net")

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    mailServer.sendmail(from_address, to_addresses + cc_addresses + bcc_addresses, msg.as_string())
    mailServer.quit()  
    #mailServer.close()  
    return("success")


# Reading email from gmail
# Based on code from http://bitsofpy.blogspot.com/2010/05/python-and-gmail-with-imap.html

def get_imap_server():
    import imaplib
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
    username = "impactofjournaldatapolicies"
    #password = ""
    imap_server.login(username, password)
    imap_server.select('unsubscribe')
    return(imap_server)

def get_unsubscribe_emails():
    imap_server = get_imap_server()
    
    # Count the unread emails
    status, response = imap_server.status('INBOX', "(UNSEEN)")
    unreadcount = int(response[0].split()[2].strip(').,]'))
    print "Number of unread:", unreadcount

    status, [email_id_string] = imap_server.search(None, 'ALL')
    email_ids = email_id_string.split()
    email_addresses = get_emails(email_ids)
    return(email_addresses)

def get_emails(email_ids):
    imap_server = get_imap_server()
    
    data = []
    for e_id in email_ids:
        _, response = imap_server.fetch(e_id, '(BODY[HEADER.FIELDS (FROM)])')
        print response
        from_line = response[0][1]
        email_address = from_line[5:].strip()
        data.append(email_address)
    return data
    
