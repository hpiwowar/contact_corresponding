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

import contact_corresponding

if __name__ == '__main__':
    nose.runmodule()

def get_this_dir(): 
    module = sys.modules[__name__]
    this_dir = os.path.dirname(os.path.abspath(module.__file__))
    return(this_dir)

data_path = os.path.join(get_this_dir(), "data")
isi_output_filename = os.path.join(get_this_dir(), "isi_output.csv")
scopus_output_filename = os.path.join(get_this_dir(), "scopus_output.csv")

email_template_initial = os.path.join(get_this_dir(), "email_template_initial.html")
email_template_followup = os.path.join(get_this_dir(), "email_template_followup.html")

class TestEmail(object):
    def test_send_email(self):
        email_html_body_template = open(email_template_initial, "r").read()
        contact_dict = {"JOURNAL":"MY JOURNAL", "URL":"http://thisurl.org"}
        email_body = contact_corresponding.get_email_text(email_html_body_template, contact_dict)
        response = contact_corresponding.send_email(email_body, "Invitation to Data Sharing Policy research study", ["hpiwowar@email.unc.edu"], [], ["hpiwowar+bcc1@gmail.com", "hpiwowar+bcc2@gmail.com"], "Heather Piwowar <hpiwowar@email.unc.edu>")
        assert_equals(response, "success")

class TestParse(object):
    def test_get_all_isi_journal_month_year_email(self):
        print(data_path)
        response = contact_corresponding.get_isi_all_fields(data_path)
        assert_equals(response[0:5], [('Am. Nat.', '2010', 'DEC', ['m.rees@sheffield.ac.uk'], '176_6', 'Article'), ('Am. Nat.', '2010', 'DEC', ['j.huisman@uva.nl'], '176_6', 'Article'), ('Am. Nat.', '2010', 'DEC', ['casey.terhorst@kbs.msu.edu'], '176_6', 'Article'), ('Am. Nat.', '2010', 'DEC', ['marjo.saastamoinen@helsinki.fi'], '176_6', 'Article'), ('Am. Nat.', '2010', 'DEC', ['rkarimi@notes.cc.sunysb.edu'], '176_6', 'Article')])
        
        journals = [journal for (journal, year, month, email, volumeissue, articletype) in response]
        assert_equals(len(set(journals)), 48)

        years = [year for (journal, year, month, email, volumeissue, articletype) in response]
        assert_equals(year, "2010")
        
        months = [month for (journal, year, month, email, volumeissue, articletype) in response]
        assert_equals(set(months), set(['SUM', 'New Phytol.-186_2', 'DEC', 'OCT', 'SEP', 'SPR', 'JUN', 'JUL', 'FAL', 'New Phytol.-186_4', 'FEB', 'New Phytol.-186_3', 'AUG', 'New Phytol.-186_1', 'JAN', 'New Phytol.-185_2', 'New Phytol.-185_4', 'New Phytol.-185_1', 'MAR', 'MAY', 'WIN', 'New Phytol.-189_1', 'New Phytol.-188_4', 'APR', 'New Phytol.-188_1', 'New Phytol.-188_2', 'New Phytol.-188_3', 'NOV', 'New Phytol.-187_4', 'New Phytol.-187_3', 'New Phytol.-187_2', 'New Phytol.-187_1']))

        writer = csv.writer(open(isi_output_filename, "w"))
        writer.writerows(response)

    def test_get_all_scopus_journal_month_year_email(self):
        print(data_path)
        response = contact_corresponding.get_scopus_all_fields(data_path)
        assert_equals(response[0:5], [('American Naturalist', '2010', '', ['dkikuchi@email.unc.edu'], '176_6'), ('American Naturalist', '2010', '', ['nigel.raine@rhul.ac.uk'], '176_6'), ('American Naturalist', '2010', '', ['marjo.saastamoinen@helsinki.fi'], '176_6'), ('American Naturalist', '2010', '', ['sonya.auer@email.ucr.edu'], '176_6'), ('American Naturalist', '2010', '', ['jbyoder@gmail.com'], '176_6')])
        
        journals = [journal for (journal, year, month, email, volumeissue) in response]
        assert_equals(len(set(journals)), 52)

        years = [year for (journal, year, month, email, volumeissue) in response]
        assert_equals(year, "2010")
        
        #months = [month for (journal, year, month, email) in response]
        #assert_equals(set(months), set(['', 'MAR', 'FEB', 'AUG', 'SEP', 'MAY', 'WIN', 'SUM', 'JUN', 'JUL', 'JAN', 'APR', 'SPR', 'FAL', 'NOV', 'DEC', 'OCT']))

        #writer = csv.writer(open(scopus_output_filename, "w"))
        #writer.writerows(response)        