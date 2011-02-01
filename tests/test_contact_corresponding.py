#!/usr/bin/env python
# encoding: utf-8
"""
@author: Heather Piwowar
@contact:  hpiwowar@gmail.com
"""

from mylog import log

import sys
import os
import nose
from nose.tools import assert_equals
from tests import password, slow, online, notimplemented, acceptance, get_this_dir

import contact_corresponding

if __name__ == '__main__':
    nose.runmodule()

test_isi_data_path = os.path.join(get_this_dir(), "testdata", "isi_2010")
test_isi_data_file = os.path.join(get_this_dir(), "testdata", "isi_2010", "EVOLUTION.txt")
test_isi_data_file2 = os.path.join(get_this_dir(), "testdata", "isi_2010", "AM NAT.txt")
test_isi_data_file3 = os.path.join(get_this_dir(), "testdata", "isi_2010", "HEREDITY.txt")
test_isi_fake_data_path = os.path.join(get_this_dir(), "testdata", "isi_fake")
test_isi_fake_data_file = os.path.join(get_this_dir(), "testdata", "isi_fake", "SAMPLE JOURNAL.txt")

test_scopus_data_path = os.path.join(get_this_dir(), "testdata", "scopus_2010")
test_scopus_data_file = os.path.join(get_this_dir(), "testdata", "scopus_2010", "0003-0147.csv")
test_scopus_data_file2 = os.path.join(get_this_dir(), "testdata", "scopus_2010", "0003-3472.csv")
test_scopus_data_file3 = os.path.join(get_this_dir(), "testdata", "scopus_2010", "0006-3207.csv")

test_sent_file = os.path.join(get_this_dir(), "testdata", "sent.txt")

def get_wc_number_lines(filename):
    wc_response = os.popen("wc " + '"' + filename + '"').read()
    number_lines = int(wc_response.split()[0])
    return(number_lines)

class TestTesterFunctions(object):
    def test_get_wc_number_lines(self):
        response = get_wc_number_lines(test_isi_data_file)
        assert_equals(response, 288)
        assert_equals(response - 1, 287)
        
class TestISIScraping(object):
    def test_get_isi_fields(self):
        response = contact_corresponding.get_isi_fields(test_isi_data_file)
        assert_equals(len(response), get_wc_number_lines(test_isi_data_file) - 1)
        assert_equals(response[1:5], [{'journal': 'Evolution', 'volume_issue': '64_12', 'emails': ['ohtsuki.h.aa@m.titech.ac.jp'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Evolution', 'volume_issue': '64_12', 'emails': ['Goran.Arnqvist@ebc.uu.se'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Evolution', 'volume_issue': '64_12', 'emails': ['montooth@indiana.edu', 'cmeiklej@mail.rochester.edu', 'david_rand@brown.edu'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Evolution', 'volume_issue': '64_12', 'emails': ['ron.eytan@gmail.com'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}])
        
        response = contact_corresponding.get_isi_fields(test_isi_data_file2)
        assert_equals(len(response), get_wc_number_lines(test_isi_data_file2) - 1)
        assert_equals(response[1:5], [{'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['j.huisman@uva.nl'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['casey.terhorst@kbs.msu.edu'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['marjo.saastamoinen@helsinki.fi'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}, {'journal': 'Am. Nat.', 'volume_issue': '176_6', 'emails': ['rkarimi@notes.cc.sunysb.edu'], 'pretty_month': 'DEC', 'year': '2010', 'type': 'Article', 'data_month': 'DEC'}])

    def test_get_isi_all_fields(self):
        response = contact_corresponding.get_isi_all_fields(test_isi_data_path)
        num_lines = get_wc_number_lines(test_isi_data_file) + get_wc_number_lines(test_isi_data_file2) + get_wc_number_lines(test_isi_data_file3) - 3
        assert_equals(len(response), num_lines)
        journals = [d["journal"] for d in response]
        assert_equals(set(journals), set(['Heredity', 'Evolution', 'Am. Nat.']))
        months = [d["data_month"] for d in response]
        assert_equals(set(months), set(['MAR', 'FEB', 'AUG', 'SEP', 'MAY', 'JUN', 'JUL', 'JAN', 'APR', 'NOV', 'DEC', 'OCT']))


class TestScopusScraping(object):
    def test_get_scopus_fields(self):    
        response = contact_corresponding.get_scopus_fields(test_scopus_data_file)
        assert_equals(len(response), get_wc_number_lines(test_scopus_data_file) - 1)
        assert_equals(response[1:5], [{'journal': 'American Naturalist', 'month': '', 'emails': ['nigel.raine@rhul.ac.uk'], 'volume_issue': '176_6', 'year': '2010'}, {'journal': 'American Naturalist', 'month': '', 'emails': ['marjo.saastamoinen@helsinki.fi'], 'volume_issue': '176_6', 'year': '2010'}, {'journal': 'American Naturalist', 'month': '', 'emails': ['sonya.auer@email.ucr.edu'], 'volume_issue': '176_6', 'year': '2010'}, {'journal': 'American Naturalist', 'month': '', 'emails': ['jbyoder@gmail.com'], 'volume_issue': '176_6', 'year': '2010'}])

        response = contact_corresponding.get_scopus_fields(test_scopus_data_file2)
        assert_equals(len(response), get_wc_number_lines(test_scopus_data_file2) - 1)
        assert_equals(response[1:5], [{'journal': 'Animal Behaviour', 'month': '', 'emails': ['patrick_zimmerman@hotmail.com'], 'volume_issue': '_', 'year': ''}, {'journal': 'Animal Behaviour', 'month': '', 'emails': ['beckersom@unlserve.unl.edu'], 'volume_issue': '_', 'year': ''}, {'journal': 'Animal Behaviour', 'month': '', 'emails': ['eleanor.cole@zoo.ox.ac.uk'], 'volume_issue': '_', 'year': ''}, {'journal': 'Animal Behaviour', 'month': '', 'emails': ['bendantzer@gmail.com'], 'volume_issue': '_', 'year': ''}])

    def test_get_scopus_all_fields(self):
        response = contact_corresponding.get_scopus_all_fields(test_scopus_data_path)
        num_lines = get_wc_number_lines(test_scopus_data_file) + get_wc_number_lines(test_scopus_data_file2) + get_wc_number_lines(test_scopus_data_file3) - 3
        assert_equals(len(response), num_lines)
        journals = [d["journal"] for d in response]
        assert_equals(set(journals), set(['Animal Behaviour', 'American Naturalist', 'Biological Conservation']))
        months = [d["month"] for d in response]
        assert_equals(set(months), set(['']))
  
    
class TestContactFilter(object):
    def test_get_unique_items(self):
        all = contact_corresponding.get_isi_fields(test_isi_fake_data_file)
        assert_equals(len(all), 35)
        unique = contact_corresponding.get_unique_items(all)
        assert_equals(len(unique), 31)

    def test_filter_research_articles(self):
        all = contact_corresponding.get_isi_fields(test_isi_fake_data_file)
        assert_equals(len(all), 35)
        all_types = [d["type"] for d in all]
        assert_equals(set(all_types), set(['Biographical-Item', 'Review', 'Letter', 'Editorial Material', 'Article', 'Correction']))
        
        result = contact_corresponding.get_filtered_dict(all, lambda k, v: k == "type" and v == "Article")
        assert_equals(len(result), 24)
        result_types = [d["type"] for d in result]
        assert_equals(set(result_types), set(['Article']))

    def test_filter_months(self):
        all = contact_corresponding.get_isi_fields(test_isi_fake_data_file)
        assert_equals(len(all), 35)
        all_months = [d["data_month"] for d in all]
        assert_equals(set(all_months), set(['NOV', 'DEC']))
        
        result = contact_corresponding.get_filtered_dict(all, lambda k, v: k == "data_month" and v in ["OCT", "NOV", "FAL"])
        assert_equals(len(result), 14)
        result_months = [d["data_month"] for d in result]
        assert_equals(set(result_months), set(['NOV']))

    def test_get_one_row_per_email(self):
        all = contact_corresponding.get_isi_fields(test_isi_fake_data_file)
        assert_equals(len(all), 35)
        response = contact_corresponding.get_one_row_per_email(all)
        assert_equals(len(response), 38)

    def test_email_not_in_already_sent(self):
        gold_has_one_row_per_email = [{'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'thorstenhorn@gmx.net', 'year': '2010', 'type': 'Review', 'emails': ['thorstenhorn@gmx.net']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'lrutledge@nrdpfc.ca', 'year': '2010', 'type': 'Editorial Material', 'emails': ['lrutledge@nrdpfc.ca']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'Deborah.Charlesworth@ed.ac.uk', 'year': '2010', 'type': 'Editorial Material', 'emails': ['Deborah.Charlesworth@ed.ac.uk']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'fgoyache@serida.org', 'year': '2010', 'type': 'Article', 'emails': ['fgoyache@serida.org']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'lrutledge@sdfsdfs.ca', 'year': '2010', 'type': 'Article', 'emails': ['lrutledge@nrdpfc.ca', 'lrutledge@sdfsdfs.ca']}]
        assert_equals(len(gold_has_one_row_per_email), 5)
        (first_occurrence, dupes) = contact_corresponding.email_not_in_already_sent(gold_has_one_row_per_email, test_sent_file)
        assert_equals(len(first_occurrence), 4)
        assert_equals(len(dupes), 1)
        assert_equals(dupes, [{'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'lrutledge@nrdpfc.ca', 'year': '2010', 'type': 'Editorial Material', 'emails': ['lrutledge@nrdpfc.ca']}])

    def test_email_first_occurrence(self):
        gold_has_one_row_per_email = [{'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'fgoyache@serida.org', 'year': '2010', 'type': 'Review', 'emails': ['fgoyache@serida.org']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'lrutledge@nrdpfc.ca', 'year': '2010', 'type': 'Editorial Material', 'emails': ['lrutledge@nrdpfc.ca']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'Deborah.Charlesworth@ed.ac.uk', 'year': '2010', 'type': 'Editorial Material', 'emails': ['Deborah.Charlesworth@ed.ac.uk']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'fgoyache@serida.org', 'year': '2010', 'type': 'Article', 'emails': ['fgoyache@serida.org']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'lrutledge@sdfsdfs.ca', 'year': '2010', 'type': 'Article', 'emails': ['lrutledge@nrdpfc.ca', 'lrutledge@sdfsdfs.ca']}]
        assert_equals(len(gold_has_one_row_per_email), 5)
        (first_occurrence, dupes) = contact_corresponding.email_first_occurrence(gold_has_one_row_per_email, False)
        assert_equals(len(first_occurrence), 4)
        assert_equals(len(dupes), 1)
        assert_equals(dupes, [{'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'fgoyache@serida.org', 'year': '2010', 'type': 'Article', 'emails': ['fgoyache@serida.org']}])

    def test_unique_emails_for_sending(self):
        all = contact_corresponding.get_isi_fields(test_isi_fake_data_file)
        assert_equals(len(all), 35)
        one_row_per_email = contact_corresponding.get_one_row_per_email(all)
        assert_equals(len(one_row_per_email), 38)
        (first_occurrence, dupes) = contact_corresponding.email_first_occurrence(one_row_per_email, True)
        assert_equals(len(first_occurrence), 27)
        assert_equals(len(dupes), 11)
        (first_occurrence2, dupes2) = contact_corresponding.email_not_in_already_sent(first_occurrence, test_sent_file)
        assert_equals(len(first_occurrence2), 24)
        assert_equals(len(dupes2), 3)

    def test_filter_unsubscribe_list(self):
        test_data = [{'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'thorstenhorn@gmx.net', 'year': '2010', 'type': 'Review', 'emails': ['thorstenhorn@gmx.net']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'hpiwowar@gmail.com', 'year': '2010', 'type': 'Editorial Material', 'emails': ['hpiwowar@gmail.com']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'Deborah.Charlesworth@ed.ac.uk', 'year': '2010', 'type': 'Editorial Material', 'emails': ['Deborah.Charlesworth@ed.ac.uk']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'fgoyache@serida.org', 'year': '2010', 'type': 'Article', 'emails': ['fgoyache@serida.org']}, {'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'lrutledge@sdfsdfs.ca', 'year': '2010', 'type': 'Article', 'emails': ['lrutledge@nrdpfc.ca', 'lrutledge@sdfsdfs.ca']}]
        (not_unsubscribe, unsubscribe) = contact_corresponding.filter_unsubscribe_list(test_data)
        assert_equals(len(not_unsubscribe), 4)
        assert_equals(unsubscribe, [{'journal': 'Heredity', 'volume_issue': '105_6', 'month': 'DEC', 'single_email': 'hpiwowar@gmail.com', 'year': '2010', 'type': 'Editorial Material', 'emails': ['hpiwowar@gmail.com']}])

    @password
    def test_get_emails_for_sending(self):
        all = contact_corresponding.get_isi_fields(test_isi_fake_data_file)
        assert_equals(len(all), 35)
        unique = contact_corresponding.get_unique_items(all)
        assert_equals(len(unique), 31)
        articles = contact_corresponding.get_filtered_dict(unique, lambda k, v: k == "type" and v == "Article")
        assert_equals(len(articles), 23)
        articles_of_months = contact_corresponding.get_filtered_dict(articles, lambda k, v: k == "data_month" and v in ["OCT", "NOV", "FAL"])
        assert_equals(len(articles_of_months), 12)
        one_row_per_email = contact_corresponding.get_one_row_per_email(articles_of_months)
        assert_equals(len(one_row_per_email), 14)
        (first_occurrence, dupes) = contact_corresponding.email_first_occurrence(one_row_per_email, True)
        assert_equals(len(first_occurrence), 10)
        assert_equals(len(dupes), 4)
        (first_occurrence2, dupes2) = contact_corresponding.email_not_in_already_sent(first_occurrence, test_sent_file)
        assert_equals(len(first_occurrence2), 9)
        assert_equals(len(dupes2), 1)
        (first_occurrence3, dupes3) = contact_corresponding.filter_unsubscribe_list(first_occurrence2)
        assert_equals(len(first_occurrence3), 8)
        assert_equals(len(dupes3), 1)

    @password
    def test_do_all_filtering(self):
        months = ["OCT", "NOV", "FAL"]
        years = ["2010"]
        (first_occurrence3, dupes3) = contact_corresponding.do_all_filtering(test_isi_fake_data_file, test_sent_file, months, years)
        assert_equals(len(first_occurrence3), 8)
        assert_equals(len(dupes3), 1)
        

class TestMailMerge(object):
    def test_mail_merge(self):
        email_text = "Dear recent author in the $pretty_month $year issue of $journal.  Hello!  Sincerely, Us."
        contact_tuple = ("Journal Of Testing", "1988", "JAN", "555@dev.null")
        contact_dict = {"journal":contact_tuple[0], "year":contact_tuple[1], "pretty_month":contact_tuple[2], "email":contact_tuple[3]}
        response = contact_corresponding.get_email_text(email_text, contact_dict)
        assert_equals(response, 'Dear recent author in the JAN 1988 issue of Journal Of Testing.  Hello!  Sincerely, Us.')
                
class TestMailSend(object):
    @password
    def test_mail_send(self):
        email_html_body = '<b>Hi!</b><p><em>Good to see <a href="somewhere">you</a>.  <p>Bye!'
        response = contact_corresponding.send_email(email_html_body, "The Subject", ["hpiwowar+to@gmail.com"], ["hpiwowar+cc@gmail.com"], ["hpiwowar+bcc@gmail.com"], "hpiwowar@email.unc.edu")
        assert_equals(response, "success")

class TestMailCheck(object):
    @password
    def test_mail_check(self):
        response = contact_corresponding.get_unsubscribe_emails()
        assert_equals(response, ['Heather Piwowar <hpiwowar@gmail.com>'])
        