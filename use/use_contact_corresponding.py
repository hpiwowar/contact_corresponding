#!/usr/bin/env python
# encoding: utf-8
"""
@author: Heather Piwowar
@contact:  hpiwowar@gmail.com
"""

import sys
import os
import nose
from nose.tools import assert_equals
import csv
import urllib
import time
import random
try:
    import contact_corresponding
    from contact_corresponding import contact_corresponding
except ImportError:
    import contact_corresponding
from mylog import log
from re import match
from urllib2 import urlopen, Request, HTTPError
from urllib import urlencode
from simplejson import loads

bitly_user = "hpiwowar"
bitly_apikey  = open("/Users/hpiwowar/Documents/Projects/JDAPsurvey/contact_corresponding/use/hpiwowar_bitly_api_key.txt", "r").read()

def get_this_dir(): 
    module = sys.modules[__name__]
    this_dir = os.path.dirname(os.path.abspath(module.__file__))
    return(this_dir)

isi_data_path = os.path.join(get_this_dir(), "data", "isi", "ISI_2011-10")
#isi_data_path = os.path.join(get_this_dir(), "data", "isi", "*")
scopus_data_path = os.path.join(get_this_dir(), "data", "scopus", "*")

isi_output_filename = os.path.join(get_this_dir(), "isi_output.csv")
scopus_output_filename = os.path.join(get_this_dir(), "scopus_output.csv")

sent_filename = os.path.join(get_this_dir(), "data", "sent.txt")
exclude_filename = os.path.join(get_this_dir(), "data", "no_reminder.csv")

email_template_initial = os.path.join(get_this_dir(), "email_template_initial.html")
email_template_followup = os.path.join(get_this_dir(), "email_template_followup.html")
        

def slow(f):
    f.slow = True
    return f

def runme(f):
    f.runme = True
    return f
        
class TestEmail(object):
    @slow
    def test_send_email(self):
        email_html_body_template = open(email_template_initial, "r").read()
        contact_dict = {"journal":"MY JOURNAL", "url":"http://thisurl.org"}
        email_body = contact_corresponding.get_email_text(email_html_body_template, contact_dict)
        response = contact_corresponding.send_email(email_body, "Invitation to Data Sharing Policy research study", ["hpiwowar@live.unc.edu"], [], ["hpiwowar+bcc1@gmail.com", "hpiwowar+bcc2@gmail.com"], "Heather Piwowar <hpiwowar@live.unc.edu>")
        assert_equals(response, "success")

class TestParse(object):
    @slow    
    def test_get_all_isi(self):
        print(isi_data_path)
        response = contact_corresponding.get_isi_all_fields(isi_data_path)
        assert_equals(response[0:5], [{'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['m.rees@sheffield.ac.uk'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['j.huisman@uva.nl'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['casey.terhorst@kbs.msu.edu'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['marjo.saastamoinen@helsinki.fi'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['rkarimi@notes.cc.sunysb.edu'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}])
        
        journals = [d["journal"] for d in response]
        assert_equals(len(set(journals)), 48)

        years = [d["year"] for d in response]
        assert_equals(set(years), set(["2010"]))
        
        months = [d["data_month"] for d in response]
        assert_equals(set(months), set(['SUM', 'New Phytol.-186_2', 'DEC', 'OCT', 'SEP', 'SPR', 'JUN', 'JUL', 'FAL', 'New Phytol.-186_4', 'FEB', 'New Phytol.-186_3', 'AUG', 'New Phytol.-186_1', 'JAN', 'New Phytol.-185_2', 'New Phytol.-185_4', 'New Phytol.-185_1', 'MAR', 'MAY', 'WIN', 'New Phytol.-189_1', 'New Phytol.-188_4', 'APR', 'New Phytol.-188_1', 'New Phytol.-188_2', 'New Phytol.-188_3', 'NOV', 'New Phytol.-187_4', 'New Phytol.-187_3', 'New Phytol.-187_2', 'New Phytol.-187_1']))

        writer = csv.DictWriter(open(isi_output_filename, "w"), response[1].keys())
        writer.writerows(response)

    @slow
    def test_get_all_scopus(self):
        print(scopus_data_path)
        response = contact_corresponding.get_scopus_all_fields(scopus_data_path)
        assert_equals(response[0:5], [{'journal': 'American Naturalist', 'month': '', 'emails': ['dkikuchi@email.unc.edu'], 'volume_issue': '176_6', 'year': '2010'}, {'journal': 'American Naturalist', 'month': '', 'emails': ['nigel.raine@rhul.ac.uk'], 'volume_issue': '176_6', 'year': '2010'}, {'journal': 'American Naturalist', 'month': '', 'emails': ['marjo.saastamoinen@helsinki.fi'], 'volume_issue': '176_6', 'year': '2010'}, {'journal': 'American Naturalist', 'month': '', 'emails': ['sonya.auer@email.ucr.edu'], 'volume_issue': '176_6', 'year': '2010'}, {'journal': 'American Naturalist', 'month': '', 'emails': ['jbyoder@gmail.com'], 'volume_issue': '176_6', 'year': '2010'}])
        
        journals = [d["journal"] for d in response]
        assert_equals(len(set(journals)), 52)

        years = [d["year"] for d in response]
        assert_equals(set(years), set(["", "2010"]))
        
        #months = [month for (journal, year, month, email) in response]
        #assert_equals(set(months), set(['', 'MAR', 'FEB', 'AUG', 'SEP', 'MAY', 'WIN', 'SUM', 'JUN', 'JUL', 'JAN', 'APR', 'SPR', 'FAL', 'NOV', 'DEC', 'OCT']))

        #writer = csv.writer(open(scopus_output_filename, "w"))
        #writer.writerows(response)      

class TestFilter(object):
    @slow
    def test_filter(self):
        #(contact_list, not_included) = contact_corresponding.do_all_filtering(isi_data_path, sent_filename, exclude_filename, months=["OCT"], years=["2010"])
        #print len(contact_list)
        #assert_equals(len(contact_list), 846)
        
        #list_output_filename = os.path.join(get_this_dir(), "oct_2010_contact_list.csv")
        #writer = csv.DictWriter(open(list_output_filename, "w"), contact_list[1].keys())
        #writer.writerows(contact_list)

        #assert_equals(len(not_included), 156)
        #excluded_list_output_filename = os.path.join(get_this_dir(), "oct_2010_excluded_list.csv")
        #writer = csv.DictWriter(open(excluded_list_output_filename, "w"), not_included[1].keys())
        #writer.writerows(not_included)

        #(contact_list, not_included) = contact_corresponding.do_all_filtering(isi_data_path, sent_filename, exclude_filename, months=["NOV"], years=["2010"])
        #len(contact_list)
        #assert_equals(len(contact_list), 806)

        #(contact_list, not_included) = contact_corresponding.do_all_filtering(isi_data_path, sent_filename, exclude_filename, months=["DEC"], years=["2010"])
        #len(contact_list)
        #assert_equals(len(contact_list), 587)

        (contact_list, not_included) = contact_corresponding.do_reminder_filtering(sent_filename, exclude_filename, months=["NOV"], years=["2010"], reminder_string="Group:2010:NOV")
        len(contact_list)
        assert_equals(len(contact_list), 779)
        
# From http://segfault.in/2010/10/shorten-urls-using-python-and-bit-ly/
def shorten_url_with_bitly(url, user, apikey):
  try:
    params = urlencode({'longUrl': url, 'login': user, 'apiKey': apikey, 'format': 'json'})
    req = Request("http://api.bit.ly/v3/shorten?%s" % params)
    response = urlopen(req)
    j = loads(response.read())
    if j['status_code'] == 200:
      return j['data']['url']
    raise Exception('%s'%j['status_txt'])
  except HTTPError, e:
    raise('HTTP error%s'%e.read())

# From http://segfault.in/2010/10/shorten-urls-using-python-and-bit-ly/
def expand_bitly_url(url, user, apikey):
  try:
    params = urlencode({'shortUrl': url, 'login': user, 'apiKey': apikey, 'format': 'json'})
    req = Request("http://api.bit.ly/v3/expand?%s" % params)
    response = urlopen(req)
    j = loads(response.read())
    if j['status_code'] == 200:
      return j['data']['expand'][0]['long_url']
    raise Exception('%s'%j['status_txt'])
  except HTTPError, e:
    raise('HTTP Error%s'%e.read()) 
    
def get_survey_url(mydict):
    questionnaire_base = "https://uncodum.qualtrics.com/SE/?SID=SV_0AmHD05E1lghBpa"
    params = urllib.urlencode({"q":mydict["q"], "journal":mydict["journal"], "month":mydict["data_month"], "year":mydict["year"]})
    url_encoded = questionnaire_base + "&" + params
    url_shortened = shorten_url_with_bitly(url_encoded, bitly_user, bitly_apikey)
    return(url_encoded, url_shortened)
            
class TestSurveyMerge(object):
    @slow   
    def test_survey_url(self):
        test_dict = {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['hpiwowar@gmail.com'], 'pretty_month': 'OCT', 'year': '2010', 'type': 'Article', 'data_month': 'OCT'}
        test_dict["q"] = "1"
        (survey_url, shortened_url) = get_survey_url(test_dict)
        assert_equals(survey_url, "https://uncodum.qualtrics.com/SE/?SID=SV_0AmHD05E1lghBpa&q=1&journal=Am.+Nat.&year=2010&month=OCT")
        assert_equals(shortened_url, "http://bit.ly/lZBRqG")
        
    @slow   
    def test_prep_email(self):
        test_dict = {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['hpiwowar@gmail.com'], 'pretty_month': 'OCT', 'year': '2010', 'type': 'Article', 'data_month': 'OCT'}
        test_dict["q"] = "1"
        (survey_url, shortened_url) = get_survey_url(test_dict)
        test_dict["url"] = shortened_url
        email_html_body_template = open(email_template_initial, "r").read()
        email_body = contact_corresponding.get_email_text(email_html_body_template, test_dict)
        log.debug(email_body)
    
    @slow   
    def test_update_sent_file(self):
        test_bcc_list = ["researchremix@gmail.com", "hpiwowar@nescent.org"]
        update_sent_file(sent_filename, test_bcc_list, "TEST")
        # could check the length
        


def update_sent_file(sent_file, bcc_list, note):
    fh = open(sent_file, "a")
    for bcc in bcc_list:
        fh.write(bcc + "\t" + time.asctime() + "\t" + note + "\r\n")
    fh.close()

    
def send_to_contact_list(fake_or_real, contact_list, subject, email_template, q, years, contact_note_append=""):
    ### DOESN'T HANDLE FILTERING BY YEARS YET!!!    
    log.debug("SENDING EMAIL TO GROUPS")
    for journal in set([d["journal"] for d in contact_list]):
        log.debug("JOURNAL: " + journal)
        journals_records = contact_corresponding.get_filtered_dict(contact_list, lambda k, v: k == "journal" and v == journal)
        for month in set([d["data_month"] for d in contact_list]):
            log.debug("MONTH: " + month)
            month_records = contact_corresponding.get_filtered_dict(journals_records, lambda k, v: k == "data_month" and v == month)
            log.debug("n = " + str(len(month_records)))
            represetative_sample = month_records[0]
            represetative_sample["q"] = q
            (survey_url, shortened_url) = get_survey_url(represetative_sample)
            represetative_sample["url"] = shortened_url
            email_html_body_template = open(email_template, "r").read()
            email_body = contact_corresponding.get_email_text(email_html_body_template, represetative_sample)
            log.debug(email_body[0:200])
            bcc_list = [d["single_email"] for d in month_records]
            log.debug("Length of bcc list:" + str(len(bcc_list)))
            log.debug("BCC list:")
            log.debug(bcc_list)
            if fake_or_real == "REAL":
                #send_it_already(subject, email_body, bcc_list)
                #log.info("******* SENT FOR REAL ***********")
                pass
            else:
                send_it_already(subject, email_body, ["hpiwowar@nescent.org"])
                log.info("--- just sent it to myself--------")
            update_sent_file(sent_filename, bcc_list, "\t".join([" ".join(years), month, journal, contact_note_append]))
    
def send_to_email_groups(fake_or_real, months, years, sent_filename, exclude_filename, subject, email_template, q):
    random.seed(42)
    (contact_list, not_included) = contact_corresponding.do_all_filtering(isi_data_path, sent_filename, exclude_filename, months, years)
    send_to_contact_list(fake_or_real, contact_list, subject, email_template, q, years, "INITIAL")

def send_to_reminder_groups(fake_or_real, months, years, sent_filename, exclude_filename, subject, email_template, q):
    random.seed(42)
    (contact_list, not_included) = contact_corresponding.do_reminder_filtering(sent_filename, exclude_filename, months, years)
    send_to_contact_list(fake_or_real, contact_list, subject, email_template, q, years, "REMINDER")
   
                
def send_it_already(subject, email_body, bcc_list):
    to_list = ["hpiwowar@live.unc.edu"]
    cc_list = []
    from_email = "Heather Piwowar <hpiwowar@live.unc.edu>"
    response = contact_corresponding.send_email(email_body, subject, to_list, cc_list, bcc_list, from_email)
    assert_equals(response, "success")


def test_get_author_and_corresponding_author_info():
    months = ["OCT"]
    years = ["2010"]
    reminder_string = "Group 2010 10"
    (contacts_before_exclude, contacts_after_exclude, dupes1, dupes2) = contact_corresponding.do_reminder_filtering_part1(sent_filename, exclude_filename, months, years, reminder_string)
    assert_equals(len(contacts_after_exclude), 846)

    writer = csv.DictWriter(open(os.path.join(get_this_dir(), "contacted_OCT_2010.csv"), "w"), contacts_after_exclude[1].keys())
    writer.writerows(contacts_after_exclude)


### before sending an email, do these steps:
### Get updated info from ISI, if necessary.  Copy from Dropbox
### Get most recent prize list respondents
### Update the list to be initial/reminder with proper month and year
### Send fake ones, make sure they are fine, then send real one

### cd ~/Documents/Projects/JDAPsurvey/contact_corresponding
### nosy use/use_contact_corresponding.py -A runme

@runme
def test_dry_run():
    # send_to_email_groups("FAKE", ["OCT"], ["2010"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)    
    # send_to_email_groups("FAKE", ["OCT"], ["2010"], sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_email_groups("FAKE", ["NOV"], ["2010"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)

    #send_to_email_groups("FAKE", ["FAL"], ["2010"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)
    #send_to_email_groups("FAKE", ["DEC"], ["2010"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)

    #send_to_reminder_groups("FAKE", ["NOV"], ["2010"], "Group:2010:NOV", sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_reminder_groups("FAKE", ["FAL"], ["2010"], "Group:2010:FAL", sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    
    #send_to_reminder_groups("FAKE", ["DEC"], ["2010"], "Group:2010:DEC", sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_email_groups("FAKE", ["JAN"], ["2011"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)
    #send_to_reminder_groups("FAKE", ["JAN"], ["2011"], "Group:2011:JAN", sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #(contact_list, not_included) = contact_corresponding.do_all_filtering(isi_data_path, sent_filename, exclude_filename, ["FEB"], ["2011"])

    #send_to_email_groups("FAKE", ["FEB"], ["2011"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)
    #send_to_reminder_groups("FAKE", ["FEB"], ["2011"], "Group:2011:FEB", sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_email_groups("FAKE", ["MAR"], ["2011"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)
    #send_to_reminder_groups("FAKE", ["MAR"], ["2011"], "Group:2011:MAR", sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_email_groups("FAKE", ["APR"], ["2011"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)
    #send_to_reminder_groups("FAKE", ["APR"], ["2011"], "Group:2011:APR", sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_email_groups("FAKE", ["MAY"], ["2011"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)
    #send_to_reminder_groups("FAKE", ["MAY"], ["2011"], sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_email_groups("FAKE", ["JUN"], ["2011"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)
    #send_to_reminder_groups("FAKE", ["JUN"], ["2011"], sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_email_groups("FAKE", ["JUL"], ["2011"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)
    #send_to_reminder_groups("FAKE", ["JUL"], ["2011"], sent_filename, exclude_filename, "reminder: Invitation to Data Sharing Policy research study", email_template_followup, 2)    

    #send_to_email_groups("FAKE", ["AUG"], ["2011"], sent_filename, exclude_filename, "Invitation to Data Sharing Policy research study", email_template_initial, 1)

    ### DOESN'T HANDLE FILTERING BY YEARS YET!!!
    pass


     