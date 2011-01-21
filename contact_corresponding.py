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
    
