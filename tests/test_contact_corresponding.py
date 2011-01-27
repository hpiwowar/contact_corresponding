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
from tests import slow, online, notimplemented, acceptance

import contact_corresponding

if __name__ == '__main__':
    nose.runmodule()

def get_this_dir():
    module = sys.modules[__name__]
    this_dir = os.path.dirname(os.path.abspath(module.__file__))
    return(this_dir)

test_data_path = os.path.join(get_this_dir(), "testdata")
test_isi_data_file = os.path.join(get_this_dir(), "testdata", "isi_2010", "EVOLUTION.txt")
test_isi_data_file2 = os.path.join(get_this_dir(), "testdata", "isi_2010", "AM NAT.txt")
test_isi_data_file3 = os.path.join(get_this_dir(), "testdata", "isi_2010", "HEREDITY.txt")

test_scopus_data_file = os.path.join(get_this_dir(), "testdata", "scopus_2010", "0003-0147.csv")
test_scopus_data_file2 = os.path.join(get_this_dir(), "testdata", "scopus_2010", "0003-3472.csv")
test_scopus_data_file3 = os.path.join(get_this_dir(), "testdata", "scopus_2010", "0006-3207.csv")

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
        assert_equals(response[1:5], [('Evolution', '2010', 'DEC', ['ohtsuki.h.aa@m.titech.ac.jp'], '64_12', 'Article'), ('Evolution', '2010', 'DEC', ['Goran.Arnqvist@ebc.uu.se'], '64_12', 'Article'), ('Evolution', '2010', 'DEC', ['montooth@indiana.edu', 'cmeiklej@mail.rochester.edu', 'david_rand@brown.edu'], '64_12', 'Article'), ('Evolution', '2010', 'DEC', ['ron.eytan@gmail.com'], '64_12', 'Article')])
        
        response = contact_corresponding.get_isi_fields(test_isi_data_file2)
        assert_equals(len(response), get_wc_number_lines(test_isi_data_file2) - 1)
        assert_equals(response[1:5], [('Am. Nat.', '2010', 'DEC', ['j.huisman@uva.nl'], '176_6', 'Article'), ('Am. Nat.', '2010', 'DEC', ['casey.terhorst@kbs.msu.edu'], '176_6', 'Article'), ('Am. Nat.', '2010', 'DEC', ['marjo.saastamoinen@helsinki.fi'], '176_6', 'Article'), ('Am. Nat.', '2010', 'DEC', ['rkarimi@notes.cc.sunysb.edu'], '176_6', 'Article')])

    def test_get_isi_all_fields(self):
        response = contact_corresponding.get_isi_all_fields(test_data_path)
        num_lines = get_wc_number_lines(test_isi_data_file) + get_wc_number_lines(test_isi_data_file2) + get_wc_number_lines(test_isi_data_file3) - 3
        assert_equals(len(response), num_lines)
        journals = [journal for (journal, year, month, email, volumeissue, articletype) in response]
        assert_equals(set(journals), set(['Heredity', 'Evolution', 'Am. Nat.']))
        months = [month for (journal, year, month, email, volumeissue, articletype) in response]
        assert_equals(set(months), set(['MAR', 'FEB', 'AUG', 'SEP', 'MAY', 'JUN', 'JUL', 'JAN', 'APR', 'NOV', 'DEC', 'OCT']))

class TestScopusScraping(object):
    def test_get_scopus_fields(self):    
        response = contact_corresponding.get_scopus_fields(test_scopus_data_file)
        assert_equals(len(response), get_wc_number_lines(test_scopus_data_file) - 1)
        assert_equals(response[1:5], [('American Naturalist', '2010', '', ['nigel.raine@rhul.ac.uk'], '176_6'), ('American Naturalist', '2010', '', ['marjo.saastamoinen@helsinki.fi'], '176_6'), ('American Naturalist', '2010', '', ['sonya.auer@email.ucr.edu'], '176_6'), ('American Naturalist', '2010', '', ['jbyoder@gmail.com'], '176_6')])

        response = contact_corresponding.get_scopus_fields(test_scopus_data_file2)
        assert_equals(len(response), get_wc_number_lines(test_scopus_data_file2) - 1)
        assert_equals(response[1:5], [('Animal Behaviour', '', '', ['patrick_zimmerman@hotmail.com'], '_'), ('Animal Behaviour', '', '', ['beckersom@unlserve.unl.edu'], '_'), ('Animal Behaviour', '', '', ['eleanor.cole@zoo.ox.ac.uk'], '_'), ('Animal Behaviour', '', '', ['bendantzer@gmail.com'], '_')])

    def test_get_scopus_all_fields(self):
        response = contact_corresponding.get_scopus_all_fields(test_data_path)
        num_lines = get_wc_number_lines(test_scopus_data_file) + get_wc_number_lines(test_scopus_data_file2) + get_wc_number_lines(test_scopus_data_file3) - 3
        assert_equals(len(response), num_lines)
        journals = [journal for (journal, year, month, email, volumeissue) in response]
        assert_equals(set(journals), set(['Animal Behaviour', 'American Naturalist', 'Biological Conservation']))
        months = [month for (journal, year, month, email, volumeissue) in response]
        assert_equals(set(months), set(['']))
    
class TestContactFilter(object):
    def test_contact_filter(self):
        response = contact_corresponding.get_isi_all_fields(test_data_path)
        # get only unique lines
        # filter for just research articles, just first occurances, just a month or season
        # make sure emails are lowercase
        pass

class TestMailMerge(object):
    def test_mail_merge(self):
        email_text = "Dear recent author in the $month $year issue of $journal.  Hello!  Sincerely, Us."
        contact_tuple = ("Journal Of Testing", "1988", "JAN", "555@dev.null")
        contact_dict = {"journal":contact_tuple[0], "year":contact_tuple[1], "month":contact_tuple[2], "email":contact_tuple[3]}
        response = contact_corresponding.get_email_text(email_text, contact_dict)
        assert_equals(response, 'Dear recent author in the JAN 1988 issue of Journal Of Testing.  Hello!  Sincerely, Us.')
        
class TestMailSend(object):
    def test_mail_send(self):
        email_html_body = '<b>Hi!</b><p><em>Good to see <a href="somewhere">you</a>.  <p>Bye!'
        #response = contact_corresponding.send_email(email_html_body, "The Subject", ["hpiwowar+to@gmail.com"], ["hpiwowar+cc@gmail.com"], ["hpiwowar+bcc@gmail.com"], "hpiwowar@email.unc.edu")
        #assert_equals(response, "success")

class TestMailCheck(object):
    def test_mail_check(self):
        response = contact_corresponding.get_unsubscribe_emails()
        assert_equals(response, ['Heather Piwowar <hpiwowar@gmail.com>'])
        