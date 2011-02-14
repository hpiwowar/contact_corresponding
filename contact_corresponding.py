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
import email.utils 
from string import Template
import random
import html2text
from mylog import log

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
	reader = csv.DictReader(open(filename, "rU"), delimiter=",")
	tuples = [(get_scopus_journal(row), get_scopus_year(row), get_scopus_month(row), get_scopus_emails(row), get_scopus_volume_issue(row)) for row in reader]
	mykeys = ["journal", "year", "month", "emails", "volume_issue"]
	mydict = [dict(zip(mykeys, myvalues)) for myvalues in tuples]
	return(mydict)

def get_scopus_all_fields(dir):
    tuples = []
    for filename in glob.glob(os.path.join(dir, "*.csv")):
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
    volume = row[ISI_VOLUME_FIELD_NAME]
    issue = row[ISI_ISSUE_FIELD_NAME]
    volume_issue = volume + "_" + issue
    return(volume_issue)

def get_isi_data_month(row):
    try:
        month = row[ISI_MONTH_FIELD_NAME][0:3]
    except IndexError:
        month = ""
    if (len(month) < 1):
        month = get_isi_journal(row) + "-" + get_isi_volume_issue(row)       
    return(month)

def get_isi_pretty_month(row):
    try:
        month = row[ISI_MONTH_FIELD_NAME][0:3]
    except IndexError:
        month = ""
    if (len(month) < 1):
        volume = row[ISI_VOLUME_FIELD_NAME]
        issue = row[ISI_ISSUE_FIELD_NAME]
        month = "vol. " + volume + ", issue " + issue
    return(month)
    
def get_isi_emails(row):
	emails = row[ISI_EMAIL_FIELD_NAME].split("; ")
	# set to lower to make comparisons easy later
	emails = [email.lower() for email in emails]
	return(emails)

def get_isi_fields(filename):
	reader = csv.DictReader(open(filename, "rU"), delimiter="\t", quoting=csv.QUOTE_NONE)
	rows = [row for row in reader]
	tuples = [(get_isi_journal(row), get_isi_year(row), get_isi_data_month(row), get_isi_pretty_month(row), get_isi_emails(row), get_isi_volume_issue(row), get_isi_article_type(row)) for row in rows]
	mykeys = ["journal", "year", "data_month", "pretty_month", "emails", "volume_issue", "type"]
	mydict = [dict(zip(mykeys, myvalues)) for myvalues in tuples]
	return(mydict)

def get_isi_all_fields(mydir):
    tuples = []
    for filename in glob.glob(os.path.join(mydir, "*.txt")):
        tuples += get_isi_fields(filename)
    return(tuples)    
    
def get_email_text(text, contact_dict):
    email_template = Template(text)
    print(contact_dict)
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
   
    try:
        mailServer = smtplib.SMTP("shawmail.vc.shawcable.net")
        #mailServer = smtplib.SMTP("smtp.zoology.ubc.ca", 465)  # I think this also needs a login
        log.info("set smtp server")
    except:
        log.info("failed to set smtp server")

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    try:
        mailServer.sendmail(from_address, to_addresses + cc_addresses + bcc_addresses, msg.as_string())
        log.info("wrote an email:  \nFROM {0}, \nTO {1}, \nCC {2}, \nBCC {3} \n{4}".format(from_address, ",".join(to_addresses),",".join(cc_addresses), ",".join(bcc_addresses), msg.as_string()))
    except:
        log.info("EMAIL NOT SENT OR RECEIVED PROPERLY:  \nFROM {0}, \nTO {1}, \nCC {2}, \nBCC {3} \n{4}".format(from_address, ",".join(to_addresses), ",".join(cc_addresses), ",".join(bcc_addresses), msg.as_string()))
        
    mailServer.quit()  
    return("success")


# Reading email from gmail
# Based on code from http://bitsofpy.blogspot.com/2010/05/python-and-gmail-with-imap.html

def get_imap_server(mailbox):
    import imaplib
    imap_server = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    username = "impactofjournaldatapolicies"
    password = open("password.txt", "r").read().strip()
    imap_server.login(username, password)
    
    imap_server.select('INBOX')
    
    # Count the unread emails
    status, response = imap_server.status('INBOX', "(UNSEEN)")
    unreadcount = int(response[0].split()[2].strip(').,]'))
    print "Number of unread:", unreadcount    
 
    imap_server.select(mailbox)
    
    return(imap_server)

def get_unsubscribe_emails():
    imap_server = get_imap_server('unsubscribe')

    status, [email_id_string] = imap_server.search(None, 'ALL')  # 'ALL'
    email_ids = email_id_string.split()
    email_addresses = get_emails(email_ids, 'unsubscribe')
    return(email_addresses)


def get_emails(email_ids, mailbox):
    imap_server = get_imap_server(mailbox)
    
    data = []
    for e_id in email_ids:
        _, response = imap_server.fetch(e_id, '(BODY[HEADER.FIELDS (FROM)])')
        from_line = response[0][1]
        #email_address = from_line[5:].strip()
        email_address = email.utils.parseaddr(from_line) 
        data.append(email_address[1])
    return data
    
# This works even when tuples contain lists.  Not fast but clear.  f2 from http://www.peterbe.com/plog/uniqifiers-benchmark    
def get_unique_items(seq):  
    # order preserving
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked
    
# from http://stackoverflow.com/questions/1214968/filtering-dictionaries-and-creating-sub-dictionaries-based-on-keys-values-in-pyth
#test_data = [{"key1":"value1", "key2":"value2"}, {"key1":"blabla"}, {"key1":"value1", "eh":"uh"}]
#list(filter_data(test_data, lambda k, v: k == "key1" and v == "value1"))    
def filter_dict(data, predicate=lambda k, v: True):
    for d in data:
         for k, v in d.items():
               if predicate(k, v):
                    yield d

def get_filtered_dict(data, predicate=lambda k, v: True):
    result = filter_dict(data, predicate)
    return(list(result))

def get_already_sent_emails(already_sent_filename):
    already_sent_rows = open(already_sent_filename, "r").readlines()
    already_sent_tuples = [row.split("\t") for row in already_sent_rows]
    emails = [email for (email, date, note) in already_sent_tuples]
    return(emails)
    
def get_one_row_per_email(rows):
    individual_rows = []
    for row in rows:
        for email in row["emails"]:
            new_row = row
            new_row["single_email"] = email
            individual_rows.append(new_row)
    return(individual_rows)

def email_not_in_already_sent(data, already_sent_filename):
    first_occurrence = []
    dups = []
    already_sent_emails = get_already_sent_emails(already_sent_filename)
    for row in data:
        if row["single_email"] in already_sent_emails:
            dups.append(row)
        else:
            first_occurrence.append(row)
    return(first_occurrence, dups)

def email_first_occurrence(data, randomize=True):
    if randomize:
        random.shuffle(data)
    already_found_emails = []
    first_occurrence = []
    dups = []
    for row in data:
        email = row["single_email"]
        if email in already_found_emails:
            dups.append(row)
        else:
            first_occurrence.append(row)
        already_found_emails.append(email)
    return(first_occurrence, dups)
      
def filter_unsubscribe_list(data):
    not_unsubscribe = []
    unsubscribe = []
    unsubscribe_emails = get_unsubscribe_emails()
    print(unsubscribe_emails)
    
    for row in data:
        email = row["single_email"]
        if email in unsubscribe_emails:
            unsubscribe.append(row)
        else:
            not_unsubscribe.append(row)
    return(not_unsubscribe, unsubscribe)

def get_exclude_emails(exclude_filename):
    exclude_rows = open(exclude_filename, "r").readlines()
    exclude_tuples = [row.split(",") for row in exclude_rows]
    emails = [row[-2] for row in exclude_tuples]
    return(emails)

def filter_exclude_list(data, exclude_filename):
    first_occurrence = []
    dups = []
    already_sent_emails = get_exclude_emails(exclude_filename)
    for row in data:
        if row["single_email"] in already_sent_emails:
            dups.append(row)
        else:
            first_occurrence.append(row)
    return(first_occurrence, dups)

    
def list_of_emails(rows):
    return([row["single_email"] for row in rows]) 
       
def do_all_filtering(data_file, sent_filename, exclude_filename, months, years):
    log.info("FILTERING with months=" + " ".join(months) + " and years=" + " ".join(years))
    log.info("for data file " + data_file)
    all_records = get_isi_all_fields(data_file)
    log.info("STARTING with n=" + str(len(all_records)))
    unique = get_unique_items(all_records)
    articles = get_filtered_dict(unique, lambda k, v: k == "type" and v == "Article")
    articles_of_months = get_filtered_dict(articles, lambda k, v: k == "data_month" and v in months)
    articles_of_years = get_filtered_dict(articles_of_months, lambda k, v: k == "year" and v in years)
    one_row_per_email = get_one_row_per_email(articles_of_years)
    log.info("AFTER FILTERING for months and years, n=" + str(len(one_row_per_email)))
    (first_occurrence, dupes) = email_first_occurrence(one_row_per_email, True)
    log.info("ELIMINATED because not first occurance, n=" + str(len(dupes)))
    log.info(list_of_emails(dupes))
    (first_occurrence2, dupes2) = email_not_in_already_sent(first_occurrence, sent_filename)
    log.info("ELIMINATED because already sent, n=" + str(len(dupes2)))
    log.info(list_of_emails(dupes2))
    (first_occurrence3, dupes3) = filter_unsubscribe_list(first_occurrence2)
    log.info("ELIMINATED because unsubscribe, n=" + str(len(dupes3)))
    log.info(list_of_emails(dupes3))
    (first_occurrence4, dupes4) = filter_exclude_list(first_occurrence3, exclude_filename)
    log.info("ELIMINATED because on exclude list, n=" + str(len(dupes4)))
    log.info(list_of_emails(dupes4))
    all_dupes = dupes + dupes2 + dupes3 + dupes4
    keepers = first_occurrence4
    log.info("KEEPING these, n=" + str(len(keepers)))
    log.debug(list_of_emails(keepers))
    return(keepers, all_dupes)