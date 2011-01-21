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

ISI_EMAIL_FIELD_NAME = "EM"
ISI_JOURNAL_FIELD_NAME = "JI"
ISI_YEAR_FIELD_NAME = "PY"
ISI_MONTH_FIELD_NAME = "PD"



def get_journal(row):
	journal = row[ISI_JOURNAL_FIELD_NAME]
	return(journal)

def get_year(row):
	year = row[ISI_YEAR_FIELD_NAME]
	return(year)

def get_month(row):
    try:
        month = row[ISI_MONTH_FIELD_NAME][0:3]
    except IndexError:
        month = ""
    return(month)

def get_emails(row):
	emails = row[ISI_EMAIL_FIELD_NAME].split("; ")
	return(emails)

def get_journal_year_month_email(filename):
	reader = csv.DictReader(open(filename, "r"), delimiter="\t", quoting=csv.QUOTE_NONE)
	tuples = [(get_journal(row), get_year(row), get_month(row), get_emails(row)) for row in reader]
	return(tuples)

def get_all_journal_year_month_email(dir):
    tuples = []
    for filename in glob.glob(os.path.join(dir, "*", "*.txt")):
        tuples += get_journal_year_month_email(filename)
    return(tuples)    
    
def get_email_text(text, contact_dict):
    email_template = Template(text)
    email_text = email_template.substitute(contact_dict)
    return(email_text)

def send_email(html_body, subject, to_address, from_address):
    # Based on code from http://docs.python.org/library/email-examples.html
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['To'] = to_address
    msg['From'] = from_address

    # Create the body of the message (a plain-text and an HTML version).
    text = html_body
    html = """\
    <html>
      <head></head>
      <body>
        <p>""" + html_body + """\
        </p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # gmail authentication steps from here:  http://kutuma.blogspot.com/2007/08/sending-emails-via-gmail-with-python.html
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    #password = input('please enter password')
    password = None
    mailServer.login("hpiwowar@gmail.com", password)
   
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    mailServer.sendmail(from_address, [to_address], msg.as_string())
    mailServer.quit()  
    #mailServer.close()  
    return("success")
